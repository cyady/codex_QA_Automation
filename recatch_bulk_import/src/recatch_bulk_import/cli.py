from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence
from urllib.parse import quote, urlencode, urlparse

import vibium

from .auth import LoginCredential, ensure_recatch_login, is_leads_page_ready, parse_credential_file


PROJECT_ROOT = Path(__file__).resolve().parents[2]
LOG_FILE_PATH: Path | None = None
RUNTIME_ROOT = Path.cwd()
SCREENSHOT_DIR = Path.cwd() / "screenshots"

NEXT_LABEL = "다음"
UPLOAD_LABEL = "업로드"
CONFIRM_LABEL = "확인"
VALIDATION_OK_TEXT = "데이터에 에러가 없습니다"
UPLOAD_OK_TEXT = "업로드에 성공했습니다."
MAPPING_HINT_TEXT = "모든 필드를 연결하지 않아도"


@dataclass(frozen=True)
class FieldMapping:
    select_index: int
    query: str
    option_text: str
    name: str


MappingSpec = dict[str, dict[str, str]]


DEFAULT_FIELD_MAPPINGS: tuple[FieldMapping, ...] = (
    FieldMapping(select_index=1, query="성명", option_text="성명", name="contact:name"),
    FieldMapping(select_index=2, query="이메일", option_text="이메일", name="contact:email"),
    FieldMapping(select_index=3, query="회사명", option_text="회사명", name="company:name"),
)

KNOWN_HEADER_DEFAULTS: dict[str, tuple[str, str]] = {
    "lead:deal_name": ("제목", "제목"),
    "contact:name": ("이름", "이름"),
    "contact:email": ("이메일", "이메일"),
    "company:name": ("회사명", "회사명"),
}

PROMPT_SKIP_TOKEN = "-"


def parse_env_file(env_path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
            value = value[1:-1]
        values[key.strip()] = value
    return values


def load_env_file(raw_path: str | None) -> Path | None:
    candidate: Path | None = None
    if raw_path:
        candidate = Path(raw_path).expanduser()
        if not candidate.is_absolute():
            candidate = (Path.cwd() / candidate).resolve()
        if not candidate.exists():
            raise FileNotFoundError(f"env file not found: {candidate}")
    else:
        env_override = os.getenv("RECATCH_ENV_FILE", "").strip()
        if env_override:
            candidate = Path(env_override).expanduser()
            if not candidate.is_absolute():
                candidate = (Path.cwd() / candidate).resolve()
            if not candidate.exists():
                raise FileNotFoundError(f"env file not found: {candidate}")
        else:
            default_env = (Path.cwd() / ".env").resolve()
            if default_env.exists():
                candidate = default_env

    if candidate is None:
        return None

    for key, value in parse_env_file(candidate).items():
        os.environ.setdefault(key, value)
    return candidate


def env_flag(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on", "y"}


def env_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    return int(raw)


def env_float(name: str, default: float) -> float:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    return float(raw)


def set_runtime_paths(runtime_root: Path, screenshot_dir: Path) -> None:
    global RUNTIME_ROOT, SCREENSHOT_DIR
    RUNTIME_ROOT = runtime_root
    SCREENSHOT_DIR = screenshot_dir


def init_log_file(logs_dir: Path) -> None:
    global LOG_FILE_PATH
    ts = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    logs_dir.mkdir(parents=True, exist_ok=True)
    LOG_FILE_PATH = logs_dir / f"bulk-import-{ts}.log"


def log(message: str) -> None:
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{now}] {message}"
    try:
        print(line)
    except UnicodeEncodeError:
        enc = sys.stdout.encoding or "utf-8"
        safe = line.encode(enc, errors="replace").decode(enc, errors="replace")
        print(safe)
    if LOG_FILE_PATH:
        with open(LOG_FILE_PATH, "a", encoding="utf-8") as file:
            file.write(line + "\n")


def unwrap_eval(value: Any) -> Any:
    if isinstance(value, dict):
        if set(value.keys()) == {"type", "value"}:
            return unwrap_eval(value["value"])
        return {k: unwrap_eval(v) for k, v in value.items()}

    if isinstance(value, list):
        if all(
            isinstance(item, list)
            and len(item) == 2
            and isinstance(item[0], str)
            for item in value
        ):
            return {item[0]: unwrap_eval(item[1]) for item in value}
        return [unwrap_eval(item) for item in value]

    return value


def eval_js(session: "vibium.browser_sync.VibeSync", script: str) -> Any:
    return unwrap_eval(session.evaluate(script))


def wait_until(
    predicate,
    timeout_sec: float,
    interval_sec: float = 0.25,
) -> bool:
    end_at = time.time() + timeout_sec
    while time.time() < end_at:
        try:
            if predicate():
                return True
        except Exception:
            pass
        time.sleep(interval_sec)
    return False


def save_screenshot(session: "vibium.browser_sync.VibeSync", step_name: str) -> str:
    ts = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    safe_step = step_name.replace(" ", "_")
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    file_path = SCREENSHOT_DIR / f"shot-{ts}-{safe_step}.png"
    data = session.screenshot()
    with open(file_path, "wb") as file:
        file.write(data)
    return str(file_path.resolve())


def resolve_input_path(raw_path: str) -> Path:
    path = Path(raw_path).expanduser()
    if path.is_absolute():
        return path.resolve()

    candidates = [
        (RUNTIME_ROOT / path).resolve(),
        (Path.cwd() / path).resolve(),
        (PROJECT_ROOT / path).resolve(),
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0]


def resolve_output_path(raw_path: str) -> Path:
    path = Path(raw_path).expanduser()
    if path.is_absolute():
        return path.resolve()
    return (RUNTIME_ROOT / path).resolve()


def resolve_optional_input_path(raw_path: str | None) -> Path | None:
    if not raw_path:
        return None
    return resolve_input_path(raw_path)


def resolve_optional_output_path(raw_path: str | None) -> Path | None:
    if not raw_path:
        return None
    return resolve_output_path(raw_path)


def normalize_base_url(base_url: str) -> str:
    return base_url.rstrip("/")


def current_url(session: "vibium.browser_sync.VibeSync") -> str:
    return str(eval_js(session, "location.href"))


def visible_page_excerpt(session: "vibium.browser_sync.VibeSync", limit: int = 25) -> list[str]:
    result = eval_js(
        session,
        f"""
(() => {{
  return ((document.body && document.body.innerText) || "")
    .split("\\n")
    .map((line) => line.trim())
    .filter(Boolean)
    .slice(0, {limit});
}})()
""",
    )
    return result if isinstance(result, list) else []


def page_contains_text(session: "vibium.browser_sync.VibeSync", text: str) -> bool:
    result = eval_js(
        session,
        f"""
(() => {{
  const body = ((document.body && document.body.innerText) || "")
    .replace(/\\s+/g, " ")
    .trim();
  return body.includes({json.dumps(text, ensure_ascii=False)});
}})()
""",
    )
    return bool(result)


def ensure_import_page_ready(session: "vibium.browser_sync.VibeSync", import_url: str) -> None:
    session.go(import_url)
    ready = wait_until(
        lambda: bool(
            eval_js(
                session,
                """
(() => {
  const isVisible = (el) => {
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.display !== "none" && s.visibility !== "hidden";
  };
  return [...document.querySelectorAll("textarea")].some((el) => isVisible(el));
})()
""",
            )
        ),
        timeout_sec=20.0,
        interval_sec=0.25,
    )
    if not ready:
        raise RuntimeError(
            f"import page not ready: url={current_url(session)}, excerpt={visible_page_excerpt(session)}"
        )


def set_textarea_value(session: "vibium.browser_sync.VibeSync", text: str) -> dict[str, Any]:
    result = eval_js(
        session,
        f"""
(() => {{
  const csvText = {json.dumps(text, ensure_ascii=False)};
  const isVisible = (el) => {{
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.display !== "none" && s.visibility !== "hidden";
  }};

  const textarea = [...document.querySelectorAll("textarea")].find((el) => isVisible(el));
  if (!textarea) return {{ ok: false, reason: "textarea_not_found" }};

  const setter = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, "value")?.set;
  textarea.focus();
  if (setter) setter.call(textarea, csvText);
  else textarea.value = csvText;
  textarea.dispatchEvent(new Event("input", {{ bubbles: true }}));
  textarea.dispatchEvent(new Event("change", {{ bubbles: true }}));
  try {{
    const dt = new DataTransfer();
    dt.setData("text/plain", csvText);
    const pasteEvent = new ClipboardEvent("paste", {{
      bubbles: true,
      cancelable: true,
      clipboardData: dt,
    }});
    textarea.dispatchEvent(pasteEvent);
  }} catch (error) {{
    // Continue even if ClipboardEvent construction is restricted.
  }}
  try {{
    textarea.dispatchEvent(
      new InputEvent("input", {{
        bubbles: true,
        data: csvText,
        inputType: "insertFromPaste",
      }})
    );
  }} catch (error) {{
    textarea.dispatchEvent(new Event("input", {{ bubbles: true }}));
  }}
  textarea.dispatchEvent(new Event("change", {{ bubbles: true }}));

  return {{
    ok: true,
    length: textarea.value.length,
    lineCount: textarea.value.split(/\\r?\\n/).length,
  }};
}})()
""",
    )
    return result if isinstance(result, dict) else {"ok": False, "raw": result}


def button_state(session: "vibium.browser_sync.VibeSync", label: str) -> dict[str, Any]:
    result = eval_js(
        session,
        f"""
(() => {{
  const wanted = ((value) => (value || "").replace(/\\s+/g, " ").trim())({json.dumps(label, ensure_ascii=False)});
  const isVisible = (el) => {{
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.display !== "none" && s.visibility !== "hidden";
  }};
  const isDisabled = (el) =>
    !!el.disabled
    || el.getAttribute("aria-disabled") === "true"
    || el.classList.contains("recatch-ant-btn-disabled");

  const matches = [...document.querySelectorAll("button, [role='button'], a")]
    .filter((el) => isVisible(el))
    .map((el) => {{
      const rect = el.getBoundingClientRect();
      return {{
        text: (el.innerText || el.textContent || "").replace(/\\s+/g, " ").trim(),
        disabled: isDisabled(el),
        x: rect.left,
        y: rect.top,
        w: rect.width,
        h: rect.height,
      }};
    }})
    .filter((item) => item.text === wanted || item.text.includes(wanted))
    .sort((a, b) => Number(a.disabled) - Number(b.disabled) || a.y - b.y || b.w - a.w);

  if (!matches.length) {{
    return {{ exists: false, enabled: false, matches: [] }};
  }}

  return {{
    exists: true,
    enabled: !matches[0].disabled,
    matches: matches.slice(0, 5),
  }};
}})()
""",
    )
    return result if isinstance(result, dict) else {"exists": False, "enabled": False, "raw": result}


def click_button_by_text(session: "vibium.browser_sync.VibeSync", label: str) -> dict[str, Any]:
    result = eval_js(
        session,
        f"""
(() => {{
  const wanted = ((value) => (value || "").replace(/\\s+/g, " ").trim())({json.dumps(label, ensure_ascii=False)});
  const isVisible = (el) => {{
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.display !== "none" && s.visibility !== "hidden";
  }};
  const isDisabled = (el) =>
    !!el.disabled
    || el.getAttribute("aria-disabled") === "true"
    || el.classList.contains("recatch-ant-btn-disabled");

  const matches = [...document.querySelectorAll("button, [role='button'], a")]
    .filter((el) => isVisible(el) && !isDisabled(el))
    .map((el) => {{
      const rect = el.getBoundingClientRect();
      return {{
        el,
        text: (el.innerText || el.textContent || "").replace(/\\s+/g, " ").trim(),
        x: rect.left,
        y: rect.top,
        w: rect.width,
        h: rect.height,
      }};
    }})
    .filter((item) => item.text === wanted || item.text.includes(wanted))
    .sort((a, b) => a.y - b.y || b.w - a.w);

  const target = matches[0];
  if (!target) {{
    return {{ ok: false, reason: "button_not_found", wanted }};
  }}

  ["pointerdown", "mousedown", "mouseup", "click"].forEach((name) => {{
    target.el.dispatchEvent(new MouseEvent(name, {{ bubbles: true, cancelable: true, view: window }}));
  }});
  target.el.click();

  return {{
    ok: true,
    text: target.text,
    x: target.x,
    y: target.y,
  }};
}})()
""",
    )
    return result if isinstance(result, dict) else {"ok": False, "raw": result}


def mapping_page_state(session: "vibium.browser_sync.VibeSync") -> dict[str, Any]:
    result = eval_js(
        session,
        f"""
(() => {{
  const isVisible = (el) => {{
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.display !== "none" && s.visibility !== "hidden";
  }};
  const selectCount = [...document.querySelectorAll(".recatch-ant-select")]
    .filter((el) => isVisible(el)).length;
  const body = ((document.body && document.body.innerText) || "").replace(/\\s+/g, " ").trim();
  return {{
    ready: selectCount >= 4 || body.includes({json.dumps(MAPPING_HINT_TEXT, ensure_ascii=False)}),
    selectCount,
  }};
}})()
""",
    )
    return result if isinstance(result, dict) else {"ready": False, "raw": result}


def read_mapping_select_texts(session: "vibium.browser_sync.VibeSync") -> list[str]:
    result = eval_js(
        session,
        """
(() => {
  return [...document.querySelectorAll(".recatch-ant-select")]
    .map((el) => (el.innerText || el.textContent || "").replace(/\\s+/g, " ").trim());
})()
""",
    )
    return result if isinstance(result, list) else []


def visible_mapping_select_count(session: "vibium.browser_sync.VibeSync") -> int:
    return len(read_mapping_select_texts(session))


def prepare_select_query(
    session: "vibium.browser_sync.VibeSync",
    select_index: int,
    query: str,
) -> dict[str, Any]:
    result = eval_js(
        session,
        f"""
(() => {{
  const targetIndex = {select_index};
  const query = {json.dumps(query, ensure_ascii=False)};
  const setInputValue = (el, value) => {{
    const setter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, "value")?.set;
    if (setter) setter.call(el, value);
    else el.value = value;
    el.dispatchEvent(new Event("input", {{ bubbles: true }}));
    el.dispatchEvent(new Event("change", {{ bubbles: true }}));
  }};

  const selects = [...document.querySelectorAll(".recatch-ant-select")];
  const select = selects[targetIndex];
  if (!select) {{
    return {{
      ok: false,
      reason: "select_not_found",
      availableCount: selects.length,
      texts: selects.map((el) => (el.innerText || el.textContent || "").replace(/\\s+/g, " ").trim()),
    }};
  }}

  try {{
    select.scrollIntoView({{ block: "center", inline: "nearest" }});
  }} catch (error) {{
    // Continue. The click below may still succeed.
  }}

  ["pointerdown", "mousedown", "mouseup", "click"].forEach((name) => {{
    select.dispatchEvent(new MouseEvent(name, {{ bubbles: true, cancelable: true, view: window }}));
  }});
  select.click();

  const input = select.querySelector("input[type='search']");
  if (!input) {{
    return {{
      ok: false,
      reason: "search_input_not_found",
      selectText: (select.innerText || select.textContent || "").replace(/\\s+/g, " ").trim(),
    }};
  }}

  input.focus();
  setInputValue(input, "");
  setInputValue(input, query);

  return {{
    ok: true,
    inputId: input.id || "",
    selectText: (select.innerText || select.textContent || "").replace(/\\s+/g, " ").trim(),
  }};
}})()
""",
    )
    return result if isinstance(result, dict) else {"ok": False, "raw": result}


def locate_dropdown_option(
    session: "vibium.browser_sync.VibeSync",
    select_index: int,
    option_text: str,
) -> dict[str, Any]:
    result = eval_js(
        session,
        f"""
(() => {{
  const targetIndex = {select_index};
  const wanted = ({json.dumps(option_text, ensure_ascii=False)} || "").replace(/\\s+/g, " ").trim();
  const wantedParts = wanted.split(">").map((value) => value.trim()).filter(Boolean);
  const groupWanted = wantedParts.length > 1 ? wantedParts[0] : "";
  const leafWanted = wantedParts.length > 1 ? wantedParts[wantedParts.length - 1] : wanted;
  const normalize = (value) => (value || "").replace(/\\s+/g, " ").trim();
  const rectInfo = (rect) => ({{
    x: rect.left,
    y: rect.top,
    w: rect.width,
    h: rect.height,
  }});
  const inViewport = (rect) =>
    rect.width > 0
    && rect.height > 0
    && rect.bottom > 0
    && rect.right > 0
    && rect.left < window.innerWidth
    && rect.top < window.innerHeight;
  const scrollableAncestor = (el) => {{
    let current = el?.parentElement || null;
    while (current) {{
      const style = getComputedStyle(current);
      const overflowY = style.overflowY || "";
      const canScroll = ["auto", "scroll", "overlay"].includes(overflowY)
        || current.scrollHeight > current.clientHeight + 4;
      if (canScroll) return current;
      current = current.parentElement;
    }}
    const root = document.scrollingElement || document.documentElement;
    return root || null;
  }};
  const bringIntoView = (el) => {{
    const target =
      el.closest(".recatch-ant-select-item-option, [role='option'], .recatch-ant-collapse-header, [role='button']")
      || el;
    const before = target.getBoundingClientRect();
    try {{
      target.scrollIntoView({{ block: "nearest", inline: "nearest" }});
    }} catch (error) {{
      // Continue with manual scrolling below.
    }}
    let after = target.getBoundingClientRect();
    if (!inViewport(after)) {{
      try {{
        target.scrollIntoView({{ block: "center", inline: "nearest" }});
      }} catch (error) {{
        // Continue with manual scrolling below.
      }}
      after = target.getBoundingClientRect();
    }}
    if (!inViewport(after)) {{
      const scroller = scrollableAncestor(target);
      if (scroller && typeof scroller.scrollTop === "number") {{
        const scrollerRect = scroller.getBoundingClientRect();
        const delta = after.top - scrollerRect.top - (scrollerRect.height / 2 - after.height / 2);
        scroller.scrollTop += delta;
        after = target.getBoundingClientRect();
      }}
    }}
    return {{
      target,
      before,
      after,
      inViewport: inViewport(after),
      scrolled:
        Math.abs(before.top - after.top) > 1
        || Math.abs(before.left - after.left) > 1,
    }};
  }};
  const isVisible = (el) => {{
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.display !== "none" && s.visibility !== "hidden";
  }};
  const dropdown = [...document.querySelectorAll(".recatch-ant-select-dropdown")]
    .filter((el) => isVisible(el))
    .sort((a, b) => b.getBoundingClientRect().height - a.getBoundingClientRect().height)[0];
  if (!dropdown) {{
    return {{
      ok: false,
      reason: "dropdown_not_found",
      wanted,
    }};
  }}

  const selects = [...document.querySelectorAll(".recatch-ant-select")];
  const select = selects[targetIndex];
  if (select) {{
    try {{
      select.scrollIntoView({{ block: "center", inline: "nearest" }});
    }} catch (error) {{
      // Continue. We only use this for anchoring.
    }}
  }}
  const selectRect = select ? select.getBoundingClientRect() : null;

  if (groupWanted) {{
    const groups = [...dropdown.querySelectorAll(".recatch-ant-collapse-item")]
      .filter((el) => isVisible(el))
      .map((el) => {{
        const headerText = normalize(
          el.querySelector(".recatch-ant-collapse-header-text")?.innerText
          || el.querySelector(".recatch-ant-collapse-header")?.innerText
          || ""
        );
        return {{ el, headerText }};
      }});

    const group = groups.find((item) => item.headerText.includes(groupWanted));
    if (group) {{
      const candidateNodes = [...group.el.querySelectorAll("*")]
        .filter((el) => isVisible(el))
        .map((el) => {{
          const rect = el.getBoundingClientRect();
          return {{
            el,
            text: normalize(el.innerText || el.textContent || ""),
            x: rect.left,
            y: rect.top,
            w: rect.width,
            h: rect.height,
          }};
        }})
        .filter((item) => item.text)
        .filter((item) => !item.text.includes(group.headerText))
        .filter((item) => item.text === leafWanted || item.text === `${{leafWanted}}*` || item.text.includes(leafWanted))
        .filter((item) => item.w >= 40 && item.h >= 16)
        .sort((a, b) => {{
          const aExact = Number(a.text === leafWanted || a.text === `${{leafWanted}}*`);
          const bExact = Number(b.text === leafWanted || b.text === `${{leafWanted}}*`);
          return bExact - aExact || a.y - b.y || b.w - a.w;
        }});

      const picked = candidateNodes[0];
      if (picked) {{
        const focused = bringIntoView(picked.el);
        return {{
          ok: true,
          wanted,
          matchedText: picked.text,
          x: focused.after.left + focused.after.width / 2,
          y: focused.after.top + focused.after.height / 2,
          inViewport: focused.inViewport,
          scrolled: focused.scrolled,
          beforeRect: rectInfo(focused.before),
          afterRect: rectInfo(focused.after),
          topCandidates: candidateNodes.slice(0, 5).map((item) => ({{
            text: item.text,
            x: item.x,
            y: item.y,
            w: item.w,
            h: item.h,
          }})),
        }};
      }}
    }}
  }}

  const optionSelectors = [
    ".recatch-ant-select-dropdown .recatch-ant-select-item-option",
    ".recatch-ant-select-dropdown [role='option']",
    ".recatch-ant-select-item-option",
    "[role='option']",
  ];

  const explicitOptions = [...new Set(optionSelectors.flatMap((selector) => [...document.querySelectorAll(selector)]))]
    .filter((el) => isVisible(el))
    .map((el) => {{
      const rect = el.getBoundingClientRect();
      return {{
        el,
        text: normalize(el.innerText || el.textContent || ""),
        x: rect.left,
        y: rect.top,
        w: rect.width,
        h: rect.height,
      }};
    }})
    .filter((item) => item.text)
    .filter((item) => item.text === wanted || item.text === `${{wanted}}*` || item.text.includes(wanted));

  const fallbackOptions = [...dropdown.querySelectorAll("*")]
    .filter((el) => isVisible(el))
    .map((el) => {{
      const rect = el.getBoundingClientRect();
      return {{
        el,
        text: normalize(el.innerText || el.textContent || ""),
        x: rect.left,
        y: rect.top,
        w: rect.width,
        h: rect.height,
      }};
    }})
    .filter((item) => item.text)
    .filter((item) => item.text === wanted || item.text === `${{wanted}}*`)
    .filter((item) => item.w >= 80 && item.h >= 24)
    .filter((item) => !selectRect || item.y >= selectRect.top - 8);

  const candidates = (explicitOptions.length ? explicitOptions : fallbackOptions)
    .sort((a, b) => {{
      const aExact = Number(a.text === wanted || a.text === `${{wanted}}*`);
      const bExact = Number(b.text === wanted || b.text === `${{wanted}}*`);
      return bExact - aExact || a.y - b.y || b.w - a.w;
    }});

  const picked = candidates[0];
  if (!picked) {{
    return {{
      ok: false,
      reason: "dropdown_option_not_found",
      wanted,
      topCandidates: candidates.slice(0, 5),
    }};
  }}

  const focused = bringIntoView(picked.el);
  return {{
    ok: true,
    wanted,
    matchedText: picked.text,
    x: focused.after.left + focused.after.width / 2,
    y: focused.after.top + focused.after.height / 2,
    inViewport: focused.inViewport,
    scrolled: focused.scrolled,
    beforeRect: rectInfo(focused.before),
    afterRect: rectInfo(focused.after),
    topCandidates: candidates.slice(0, 5).map((item) => ({{
      text: item.text,
      x: item.x,
      y: item.y,
      w: item.w,
      h: item.h,
    }})),
  }};
}})()
""",
    )
    return result if isinstance(result, dict) else {"ok": False, "raw": result}


def click_at(session: "vibium.browser_sync.VibeSync", x: float, y: float) -> dict[str, Any]:
    result = eval_js(
        session,
        f"""
(() => {{
  const x = {x};
  const y = {y};
  const viewport = {{
    width: window.innerWidth,
    height: window.innerHeight,
  }};
  if (x < 0 || y < 0 || x > viewport.width || y > viewport.height) {{
    return {{
      ok: false,
      reason: "point_out_of_viewport",
      x,
      y,
      viewport,
    }};
  }}
  const el = document.elementFromPoint(x, y);
  if (!el) return {{ ok: false, reason: "element_not_found" }};

  ["pointerdown", "mousedown", "mouseup", "click"].forEach((name) => {{
    el.dispatchEvent(new MouseEvent(name, {{
      bubbles: true,
      cancelable: true,
      clientX: x,
      clientY: y,
      view: window,
    }}));
  }});
  if (typeof el.click === "function") {{
    el.click();
  }}

  return {{
    ok: true,
    tag: el.tagName,
    text: (el.innerText || el.textContent || "").replace(/\\s+/g, " ").trim().slice(0, 120),
  }};
}})()
""",
    )
    return result if isinstance(result, dict) else {"ok": False, "raw": result}


def selected_option_state(
    session: "vibium.browser_sync.VibeSync",
    select_index: int,
    option_text: str,
) -> dict[str, Any]:
    result = eval_js(
        session,
        f"""
(() => {{
  const targetIndex = {select_index};
  const wanted = ({json.dumps(option_text, ensure_ascii=False)} || "").replace(/\\s+/g, " ").trim();
  const leafWanted = wanted.split(">").slice(-1)[0].trim();
  const normalize = (value) => (value || "").replace(/\\s+/g, " ").trim();
  const selects = [...document.querySelectorAll(".recatch-ant-select")];
  const select = selects[targetIndex];
  if (!select) return {{ selected: false, reason: "select_not_found" }};

  const text = normalize(
    select.querySelector(".recatch-ant-select-selection-item")?.innerText
    || select.innerText
    || select.textContent
    || ""
  );

  return {{
    selected: text.includes(wanted) || (leafWanted && text.includes(leafWanted)),
    text,
  }};
}})()
""",
    )
    return result if isinstance(result, dict) else {"selected": False, "raw": result}


def mapping_variants(mapping: FieldMapping) -> list[tuple[str, str]]:
    if mapping.name == "contact:name":
        return [
            ("성명", "연락처 > 성명"),
            ("연락처", "연락처 > 성명"),
            ("성명", "성명"),
        ]
    if mapping.name == "contact:email":
        return [
            ("이메일", "연락처 > 이메일"),
            ("연락처", "연락처 > 이메일"),
            ("이메일", "이메일"),
        ]
    if mapping.name == "company:name":
        return [
            ("회사명", "회사 > 회사명"),
            ("회사", "회사 > 회사명"),
            ("회사명", "회사명"),
        ]
    return [(mapping.query, mapping.option_text)]


def map_field(
    session: "vibium.browser_sync.VibeSync",
    mapping: FieldMapping,
) -> dict[str, Any]:
    last_detail: dict[str, Any] = {"ok": False, "reason": "not_started"}
    attempt = 0
    for query, option_text in mapping_variants(mapping):
        for _ in range(2):
            attempt += 1
            prepared = prepare_select_query(session, mapping.select_index, query)
            if not prepared.get("ok"):
                last_detail = {
                    "attempt": attempt,
                    "stage": "prepare",
                    "query": query,
                    "option_text": option_text,
                    "detail": prepared,
                }
                time.sleep(0.3)
                continue

            time.sleep(0.5)
            located = locate_dropdown_option(session, mapping.select_index, option_text)
            if not located.get("ok"):
                last_detail = {
                    "attempt": attempt,
                    "stage": "locate",
                    "query": query,
                    "option_text": option_text,
                    "detail": located,
                }
                time.sleep(0.3)
                continue

            clicked = click_at(session, float(located["x"]), float(located["y"]))
            if not clicked.get("ok"):
                last_detail = {
                    "attempt": attempt,
                    "stage": "click",
                    "query": query,
                    "option_text": option_text,
                    "prepared": prepared,
                    "located": located,
                    "clicked": clicked,
                }
                time.sleep(0.3)
                continue
            selected = wait_until(
                lambda: bool(selected_option_state(session, mapping.select_index, option_text).get("selected")),
                timeout_sec=4.0,
                interval_sec=0.15,
            )
            state = selected_option_state(session, mapping.select_index, option_text)
            if selected:
                return {
                    "ok": True,
                    "attempt": attempt,
                    "query": query,
                    "option_text": option_text,
                    "prepared": prepared,
                    "located": located,
                    "clicked": clicked,
                    "state": state,
                }
            last_detail = {
                "attempt": attempt,
                "stage": "verify",
                "query": query,
                "option_text": option_text,
                "prepared": prepared,
                "located": located,
                "clicked": clicked,
                "state": state,
            }
            time.sleep(0.3)

    return {"ok": False, "mapping": mapping.name, "detail": last_detail}


def apply_mappings(
    session: "vibium.browser_sync.VibeSync",
    mappings: Sequence[FieldMapping],
    part_label: str,
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    total = len(mappings)
    for index, mapping in enumerate(mappings, start=1):
        log(
            f"[{part_label}] mapping ({index}/{total}): "
            f"{mapping.name} -> {mapping.option_text}"
        )
        result = map_field(session, mapping)
        results.append(result)
        if not result.get("ok"):
            raise RuntimeError(f"mapping failed for {mapping.name}: {result}")
    return results


def wait_for_enabled_button(
    session: "vibium.browser_sync.VibeSync",
    label: str,
    timeout_sec: float,
) -> dict[str, Any]:
    found = wait_until(
        lambda: bool(button_state(session, label).get("enabled")),
        timeout_sec=timeout_sec,
        interval_sec=0.2,
    )
    state = button_state(session, label)
    if not found:
        raise RuntimeError(
            f"button not enabled: label={label}, state={state}, excerpt={visible_page_excerpt(session)}"
        )
    return state


def click_enabled_button(
    session: "vibium.browser_sync.VibeSync",
    label: str,
    timeout_sec: float,
) -> dict[str, Any]:
    wait_for_enabled_button(session, label, timeout_sec)
    result = click_button_by_text(session, label)
    if not result.get("ok"):
        raise RuntimeError(f"button click failed: label={label}, result={result}")
    return result


def count_csv_rows(csv_text: str) -> int:
    lines = [line for line in csv_text.splitlines() if line.strip()]
    if not lines:
        return 0
    return max(len(lines) - 1, 0)


def read_csv_headers(csv_path: Path) -> list[str]:
    with open(csv_path, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.reader(file)
        try:
            header = next(reader)
        except StopIteration as exc:
            raise ValueError(f"csv file is empty: {csv_path}") from exc
    headers = [value.strip() for value in header]
    if not any(headers):
        raise ValueError(f"csv header is empty: {csv_path}")
    return headers


def split_source_csv(
    source_csv_path: Path,
    output_dir: Path,
    file_prefix: str,
    split_size: int,
) -> tuple[list[str], list[Path]]:
    if split_size < 1:
        raise ValueError(f"split size must be >= 1: {split_size}")

    output_dir.mkdir(parents=True, exist_ok=True)
    part_paths: list[Path] = []

    with open(source_csv_path, "r", encoding="utf-8-sig", newline="") as src_file:
        reader = csv.reader(src_file)
        try:
            header = next(reader)
        except StopIteration as exc:
            raise ValueError(f"csv file is empty: {source_csv_path}") from exc

        headers = [value.strip() for value in header]
        if not any(headers):
            raise ValueError(f"csv header is empty: {source_csv_path}")

        part_number = 0
        rows: list[list[str]] = []
        for row in reader:
            if not any(cell.strip() for cell in row):
                continue
            rows.append(row)
            if len(rows) >= split_size:
                part_number += 1
                part_path = write_split_csv(output_dir, file_prefix, part_number, header, rows)
                part_paths.append(part_path)
                rows = []

        if rows or part_number == 0:
            part_number += 1
            part_path = write_split_csv(output_dir, file_prefix, part_number, header, rows)
            part_paths.append(part_path)

    return headers, part_paths


def write_split_csv(
    output_dir: Path,
    file_prefix: str,
    part_number: int,
    header: Sequence[str],
    rows: Sequence[Sequence[str]],
) -> Path:
    part_path = output_dir / f"{file_prefix}{part_number:03d}.csv"
    with open(part_path, "w", encoding="utf-8", newline="") as dst_file:
        writer = csv.writer(dst_file)
        writer.writerow(header)
        writer.writerows(rows)
    return part_path


def parse_mapping_value(raw_value: str) -> tuple[str, str]:
    if "|" not in raw_value:
        normalized = raw_value.strip()
        return normalized, normalized

    query, option_text = raw_value.split("|", 1)
    query = query.strip()
    option_text = option_text.strip()
    if not query or not option_text:
        raise ValueError("mapping value must be `field` or `query|option_text`")
    return query, option_text


def load_mapping_spec(mapping_path: Path) -> MappingSpec:
    payload = json.loads(mapping_path.read_text(encoding="utf-8"))
    if isinstance(payload, dict) and "columns" in payload:
        payload = payload["columns"]

    if isinstance(payload, list):
        normalized: MappingSpec = {}
        for item in payload:
            if not isinstance(item, dict):
                raise ValueError(f"mapping file has invalid item: {item!r}")
            header = str(item.get("csv_header", "")).strip()
            query = str(item.get("query", "")).strip()
            option_text = str(item.get("option_text", "")).strip()
            if not header:
                raise ValueError(f"mapping item missing csv_header: {item!r}")
            if query and option_text:
                normalized[header] = {"query": query, "option_text": option_text}
        return normalized

    if not isinstance(payload, dict):
        raise ValueError("mapping file must be an object or a columns array")

    normalized: MappingSpec = {}
    for header, value in payload.items():
        if value in (None, "", False):
            continue
        if isinstance(value, str):
            query, option_text = parse_mapping_value(value)
        elif isinstance(value, dict):
            query = str(value.get("query", "")).strip()
            option_text = str(value.get("option_text", "")).strip()
        else:
            raise ValueError(f"mapping value must be string/object: {header!r}")

        if not query or not option_text:
            raise ValueError(f"mapping entry is incomplete: {header!r}")
        normalized[str(header).strip()] = {"query": query, "option_text": option_text}
    return normalized


def save_mapping_spec(mapping_path: Path, mapping_spec: MappingSpec) -> None:
    mapping_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "columns": [
            {
                "csv_header": header,
                "query": entry["query"],
                "option_text": entry["option_text"],
            }
            for header, entry in mapping_spec.items()
        ]
    }
    mapping_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def prompt_mapping_spec(headers: Sequence[str]) -> MappingSpec:
    total = len(headers)
    print()
    print("CSV -> Re:catch field mapping")
    print("  blank : use default if available, otherwise skip")
    print(f"  {PROMPT_SKIP_TOKEN} : skip this column")
    print("  value : use the same search text and option text")
    print("  query|option : search with `query`, click exact `option`")
    print()

    mapping_spec: MappingSpec = {}
    for index, header in enumerate(headers, start=1):
        default_value = KNOWN_HEADER_DEFAULTS.get(header)
        default_option = default_value[1] if default_value else None

        while True:
            prompt = f"[{index}/{total}] {header}"
            if default_option:
                prompt += f" [Enter={default_option}, {PROMPT_SKIP_TOKEN}=skip]"
            else:
                prompt += f" [{PROMPT_SKIP_TOKEN}=skip]"
            prompt += ": "

            raw_value = input(prompt).strip()
            if not raw_value:
                if default_value:
                    mapping_spec[header] = {
                        "query": default_value[0],
                        "option_text": default_value[1],
                    }
                break
            if raw_value == PROMPT_SKIP_TOKEN:
                break

            try:
                query, option_text = parse_mapping_value(raw_value)
            except ValueError as exc:
                print(f"  invalid mapping: {exc}")
                continue

            mapping_spec[header] = {"query": query, "option_text": option_text}
            break

    return mapping_spec


def build_mappings_from_spec(
    headers: Sequence[str],
    mapping_spec: MappingSpec,
) -> list[FieldMapping]:
    mappings: list[FieldMapping] = []
    for select_index, header in enumerate(headers):
        entry = mapping_spec.get(header)
        if not entry:
            continue
        mappings.append(
            FieldMapping(
                select_index=select_index,
                query=entry["query"],
                option_text=entry["option_text"],
                name=header,
            )
        )
    return mappings


def import_csv_part(
    session: "vibium.browser_sync.VibeSync",
    import_url: str,
    csv_path: Path,
    upload_timeout_sec: float,
    mappings: Sequence[FieldMapping],
    expected_select_count: int,
    part_label: str,
) -> dict[str, Any]:
    csv_text = csv_path.read_text(encoding="utf-8")
    row_count = count_csv_rows(csv_text)

    ensure_import_page_ready(session, import_url)
    paste_result = set_textarea_value(session, csv_text)
    if not paste_result.get("ok"):
        raise RuntimeError(f"csv paste failed for {csv_path.name}: {paste_result}")

    click_enabled_button(session, NEXT_LABEL, timeout_sec=20.0)

    mapping_ready = wait_until(
        lambda: bool(mapping_page_state(session).get("ready")),
        timeout_sec=20.0,
        interval_sec=0.2,
    )
    if not mapping_ready:
        raise RuntimeError(
            f"mapping page not ready for {csv_path.name}: excerpt={visible_page_excerpt(session)}"
        )

    required_select_count = max(expected_select_count, 1)
    mapping_selects_ready = wait_until(
        lambda: visible_mapping_select_count(session) >= required_select_count,
        timeout_sec=10.0,
        interval_sec=0.2,
    )
    if not mapping_selects_ready:
        raise RuntimeError(
            "mapping selects not ready for "
            f"{csv_path.name}: expected>={required_select_count}, "
            f"actual={visible_mapping_select_count(session)}, "
            f"excerpt={visible_page_excerpt(session)}"
    )

    mapping_selects = read_mapping_select_texts(session)
    mapping_results = apply_mappings(session, mappings, part_label) if mappings else []

    click_enabled_button(session, NEXT_LABEL, timeout_sec=20.0)
    validation_ok = wait_until(
        lambda: page_contains_text(session, VALIDATION_OK_TEXT),
        timeout_sec=30.0,
        interval_sec=0.2,
    )
    if not validation_ok:
        raise RuntimeError(
            f"validation step failed for {csv_path.name}: excerpt={visible_page_excerpt(session)}"
        )

    click_enabled_button(session, NEXT_LABEL, timeout_sec=20.0)
    click_enabled_button(session, UPLOAD_LABEL, timeout_sec=30.0)

    upload_ok = wait_until(
        lambda: page_contains_text(session, UPLOAD_OK_TEXT),
        timeout_sec=upload_timeout_sec,
        interval_sec=0.5,
    )
    if not upload_ok:
        raise RuntimeError(
            f"upload success text not found for {csv_path.name}: excerpt={visible_page_excerpt(session)}"
        )

    click_enabled_button(session, CONFIRM_LABEL, timeout_sec=20.0)
    leads_ready = wait_until(
        lambda: is_leads_page_ready(session),
        timeout_sec=20.0,
        interval_sec=0.25,
    )
    if not leads_ready:
        raise RuntimeError(
            f"did not return to leads page after {csv_path.name}: url={current_url(session)}"
        )

    return {
        "ok": True,
        "file": csv_path.name,
        "rowCount": row_count,
        "pasteResult": paste_result,
        "mappingSelects": mapping_selects,
        "mappingResults": mapping_results,
    }


def build_default_url(base_url: str, path: str) -> str:
    return f"{base_url}{path}"


def build_leads_path(team_slug: str) -> str:
    query: dict[str, str] = {}
    if team_slug:
        query["teamSlug"] = team_slug
    return "/leads" + (f"?{urlencode(query, quote_via=quote)}" if query else "")


def build_login_url(base_url: str, team_slug: str) -> str:
    query: dict[str, str] = {"redirect": build_leads_path(team_slug)}
    if team_slug:
        query["teamSlug"] = team_slug
    return build_default_url(base_url, f"/login?{urlencode(query, quote_via=quote)}")


def build_leads_url(base_url: str, team_slug: str) -> str:
    return build_default_url(base_url, build_leads_path(team_slug))


def build_import_url(base_url: str, team_slug: str, record_type_id: int) -> str:
    query: dict[str, str | int] = {"recordTypeId": record_type_id}
    if team_slug:
        query["teamSlug"] = team_slug
    return build_default_url(
        base_url,
        f"/leads/import?{urlencode(query, quote_via=quote)}",
    )


def default_state_path(base_url: str, team_slug: str, logs_dir: Path) -> Path:
    logs_dir.mkdir(parents=True, exist_ok=True)
    host = urlparse(base_url).netloc.replace(".", "_").replace(":", "_")
    slug = team_slug or "default"
    return logs_dir / f"bulk-import-state-{host}-{slug}.json"


def load_completed_parts(state_path: Path) -> set[int]:
    if not state_path.exists():
        return set()
    payload = json.loads(state_path.read_text(encoding="utf-8"))
    raw_parts = payload.get("completed_parts", [])
    return {int(part) for part in raw_parts}


def write_state_file(
    state_path: Path,
    base_url: str,
    team_slug: str,
    record_type_id: int,
    start: int,
    end: int,
    completed_parts: set[int],
) -> None:
    state_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "updated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "base_url": base_url,
        "team_slug": team_slug,
        "record_type_id": record_type_id,
        "start": start,
        "end": end,
        "completed_parts": sorted(completed_parts),
    }
    state_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def determine_runtime_root(env_file: Path | None) -> Path:
    if env_file is not None:
        return env_file.parent.resolve()
    return Path.cwd().resolve()


def determine_file_prefix(file_prefix: str, source_csv_path: Path | None) -> str:
    normalized = file_prefix.strip()
    if normalized:
        return normalized
    if source_csv_path is not None:
        return f"{source_csv_path.stem}_part_"
    return "part_"


def resolve_part_range(start: int, end: int, total_parts: int) -> tuple[int, int]:
    if start < 1:
        raise ValueError(f"start must be >= 1: {start}")
    actual_end = total_parts if end <= 0 else end
    if actual_end < start:
        raise ValueError(f"invalid part range: {start}..{actual_end}")
    if actual_end > total_parts:
        raise ValueError(f"end exceeds available parts: {actual_end} > {total_parts}")
    return start, actual_end


def discover_existing_parts(csv_dir: Path, file_prefix: str) -> list[tuple[int, Path]]:
    parts: list[tuple[int, Path]] = []
    for csv_path in sorted(csv_dir.glob(f"{file_prefix}*.csv")):
        suffix = csv_path.stem[len(file_prefix) :]
        if not suffix.isdigit():
            continue
        parts.append((int(suffix), csv_path))
    return sorted(parts, key=lambda item: item[0])


def build_default_mapping_spec(headers: Sequence[str]) -> MappingSpec:
    mapping_spec: MappingSpec = {}
    for header in headers:
        default_value = KNOWN_HEADER_DEFAULTS.get(header)
        if not default_value:
            continue
        mapping_spec[header] = {
            "query": default_value[0],
            "option_text": default_value[1],
        }
    return mapping_spec


def resolve_runtime_mappings(
    headers: Sequence[str],
    source_csv_path: Path | None,
    mapping_path: Path | None,
    prompt_mapping: bool,
) -> list[FieldMapping]:
    if source_csv_path is None and mapping_path is None and not prompt_mapping:
        mapping_spec = {
            mapping.name: {
                "query": mapping.query,
                "option_text": mapping.option_text,
            }
            for mapping in DEFAULT_FIELD_MAPPINGS
        }
        log("mapping prompt skipped; using built-in hardcoded defaults")
        return list(DEFAULT_FIELD_MAPPINGS)

    mapping_spec: MappingSpec
    should_prompt = prompt_mapping or (
        source_csv_path is not None
        and sys.stdin.isatty()
        and (mapping_path is None or not mapping_path.exists())
    )

    if mapping_path is not None and mapping_path.exists():
        mapping_spec = load_mapping_spec(mapping_path)
        log(f"mapping file loaded: {mapping_path}")
    elif should_prompt:
        mapping_spec = prompt_mapping_spec(headers)
        if mapping_path is not None:
            save_mapping_spec(mapping_path, mapping_spec)
            log(f"mapping file saved: {mapping_path}")
    else:
        mapping_spec = build_default_mapping_spec(headers)
        log("mapping prompt skipped; using built-in defaults where available")

    return build_mappings_from_spec(headers, mapping_spec)


def prepare_part_jobs_and_mappings(
    args: argparse.Namespace,
    base_url: str,
    log_dir: Path,
) -> dict[str, Any]:
    source_csv_path = resolve_optional_input_path(args.source_csv)
    file_prefix = determine_file_prefix(args.file_prefix, source_csv_path)
    csv_dir = (
        resolve_output_path(args.csv_dir)
        if source_csv_path is not None
        else resolve_input_path(args.csv_dir)
    )
    mapping_path = resolve_optional_output_path(args.mapping_file)
    state_path = resolve_optional_output_path(args.state_file) or default_state_path(
        base_url,
        args.team_slug,
        log_dir,
    )

    if source_csv_path is not None:
        headers, generated_part_paths = split_source_csv(
            source_csv_path=source_csv_path,
            output_dir=csv_dir,
            file_prefix=file_prefix,
            split_size=args.split_size,
        )
        start_part, end_part = resolve_part_range(args.start, args.end, len(generated_part_paths))
        part_jobs = [
            (part_number, generated_part_paths[part_number - 1])
            for part_number in range(start_part, end_part + 1)
        ]
    else:
        existing_parts = discover_existing_parts(csv_dir, file_prefix)
        if not existing_parts:
            raise FileNotFoundError(f"no csv files found in {csv_dir} with prefix {file_prefix!r}")
        part_lookup = {part_number: csv_path for part_number, csv_path in existing_parts}
        start_part, end_part = resolve_part_range(args.start, args.end, max(part_lookup))
        missing_parts = [part for part in range(start_part, end_part + 1) if part not in part_lookup]
        if missing_parts:
            preview = ", ".join(f"{part:03d}" for part in missing_parts[:10])
            raise FileNotFoundError(f"missing csv part(s): {preview}")
        part_jobs = [(part_number, part_lookup[part_number]) for part_number in range(start_part, end_part + 1)]
        headers = read_csv_headers(part_jobs[0][1])

    mappings = resolve_runtime_mappings(
        headers=headers,
        source_csv_path=source_csv_path,
        mapping_path=mapping_path,
        prompt_mapping=args.prompt_mapping,
    )

    return {
        "source_csv_path": source_csv_path,
        "file_prefix": file_prefix,
        "csv_dir": csv_dir,
        "mapping_path": mapping_path,
        "state_path": state_path,
        "headers": headers,
        "mappings": mappings,
        "part_jobs": part_jobs,
        "actual_start": part_jobs[0][0],
        "actual_end": part_jobs[-1][0],
    }


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    bootstrap = argparse.ArgumentParser(add_help=False)
    bootstrap.add_argument("--env-file")
    bootstrap_args, _ = bootstrap.parse_known_args(argv)
    loaded_env_file = load_env_file(bootstrap_args.env_file)

    parser = argparse.ArgumentParser(
        description="Bulk import lead CSV files into Re:catch with Vibium."
    )
    parser.add_argument("--env-file", default=str(loaded_env_file) if loaded_env_file else None)
    parser.add_argument("--base-url", default=os.getenv("RECATCH_BASE_URL", ""))
    parser.add_argument(
        "--team-slug",
        default=os.getenv("RECATCH_TEAM_SLUG", ""),
        help="optional team slug for routes that use ?teamSlug=...",
    )
    parser.add_argument(
        "--record-type-id",
        type=int,
        default=env_int("RECATCH_RECORD_TYPE_ID", 0),
    )
    parser.add_argument("--login-url", default=os.getenv("RECATCH_LOGIN_URL", ""))
    parser.add_argument("--leads-url", default=os.getenv("RECATCH_LEADS_URL", ""))
    parser.add_argument("--import-url", default=os.getenv("RECATCH_IMPORT_URL", ""))
    parser.add_argument(
        "--source-csv",
        default=os.getenv("RECATCH_SOURCE_CSV", ""),
        help="single source CSV file to split before import",
    )
    parser.add_argument(
        "--csv-dir",
        default=os.getenv("RECATCH_CSV_DIR", "data/csv_split"),
        help="directory that contains split CSV files or receives generated split files",
    )
    parser.add_argument(
        "--file-prefix",
        default=os.getenv("RECATCH_FILE_PREFIX", ""),
        help="file prefix before the 3-digit part number; blank means auto-detect",
    )
    parser.add_argument(
        "--split-size",
        type=int,
        default=env_int("RECATCH_SPLIT_SIZE", 1000),
        help="rows per generated CSV chunk when --source-csv is used",
    )
    parser.add_argument(
        "--mapping-file",
        default=os.getenv("RECATCH_MAPPING_FILE", ""),
        help="JSON mapping file to load/save by CSV header name",
    )
    parser.add_argument(
        "--prompt-mapping",
        action=argparse.BooleanOptionalAction,
        default=env_flag("RECATCH_PROMPT_MAPPING", False),
        help="prompt for CSV header mappings before import",
    )
    parser.add_argument("--start", type=int, default=env_int("RECATCH_START", 1))
    parser.add_argument(
        "--end",
        type=int,
        default=env_int("RECATCH_END", 0),
        help="last part number to process; 0 means auto-detect last part",
    )
    parser.add_argument(
        "--credential-file",
        default=os.getenv("RECATCH_CREDENTIAL_FILE", "credentials/recatch_login.txt"),
    )
    parser.add_argument(
        "--manual-login-fallback",
        action=argparse.BooleanOptionalAction,
        default=env_flag("RECATCH_MANUAL_LOGIN_FALLBACK", False),
    )
    parser.add_argument(
        "--headless",
        action=argparse.BooleanOptionalAction,
        default=env_flag("RECATCH_HEADLESS", False),
    )
    parser.add_argument(
        "--keep-open",
        action=argparse.BooleanOptionalAction,
        default=env_flag("RECATCH_KEEP_OPEN", False),
    )
    parser.add_argument(
        "--skip-completed",
        action=argparse.BooleanOptionalAction,
        default=env_flag("RECATCH_SKIP_COMPLETED", False),
    )
    parser.add_argument(
        "--delay-between-parts",
        type=float,
        default=env_float("RECATCH_DELAY_BETWEEN_PARTS", 0.0),
    )
    parser.add_argument(
        "--upload-timeout-sec",
        type=float,
        default=env_float("RECATCH_UPLOAD_TIMEOUT_SEC", 300.0),
    )
    parser.add_argument("--state-file", default=os.getenv("RECATCH_STATE_FILE", ""))
    parser.add_argument("--log-dir", default=os.getenv("RECATCH_LOG_DIR", "logs"))
    parser.add_argument(
        "--screenshot-dir",
        default=os.getenv("RECATCH_SCREENSHOT_DIR", "screenshots"),
    )
    args = parser.parse_args(argv)

    if not args.base_url:
        parser.error("--base-url or RECATCH_BASE_URL is required")
    if args.start < 1:
        parser.error("--start/--end range is invalid")
    if args.end < 0:
        parser.error("--end must be >= 0")
    if args.split_size < 1:
        parser.error("--split-size must be >= 1")

    args.loaded_env_file = loaded_env_file
    return args


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)

    runtime_root = determine_runtime_root(args.loaded_env_file)
    bootstrap_screenshot_dir = Path(args.screenshot_dir).expanduser()
    if not bootstrap_screenshot_dir.is_absolute():
        bootstrap_screenshot_dir = (runtime_root / bootstrap_screenshot_dir).resolve()
    else:
        bootstrap_screenshot_dir = bootstrap_screenshot_dir.resolve()
    set_runtime_paths(runtime_root=runtime_root, screenshot_dir=bootstrap_screenshot_dir)
    log_dir = resolve_output_path(args.log_dir)
    screenshot_dir = resolve_output_path(args.screenshot_dir)
    set_runtime_paths(runtime_root=runtime_root, screenshot_dir=screenshot_dir)
    init_log_file(log_dir)

    base_url = normalize_base_url(args.base_url)
    login_url = args.login_url or build_login_url(base_url, args.team_slug)
    leads_url = args.leads_url or build_leads_url(base_url, args.team_slug)
    import_url = args.import_url or build_import_url(base_url, args.team_slug, args.record_type_id)
    credential_path = resolve_optional_input_path(args.credential_file)

    session: vibium.browser_sync.VibeSync | None = None

    try:
        prepared = prepare_part_jobs_and_mappings(args, base_url, log_dir)
        source_csv_path = prepared["source_csv_path"]
        file_prefix = prepared["file_prefix"]
        csv_dir = prepared["csv_dir"]
        mapping_path = prepared["mapping_path"]
        state_path = prepared["state_path"]
        headers = prepared["headers"]
        mappings = prepared["mappings"]
        part_jobs = prepared["part_jobs"]
        actual_start = prepared["actual_start"]
        actual_end = prepared["actual_end"]

        log(f"log file: {LOG_FILE_PATH}")
        log(f"env file: {args.loaded_env_file or '(not used)'}")
        log(f"runtime root: {runtime_root}")
        log(f"base url: {base_url}")
        log(f"team slug: {args.team_slug}")
        log(f"login url: {login_url}")
        log(f"leads url: {leads_url}")
        log(f"import url: {import_url}")
        log(f"source csv: {source_csv_path or '(not used)'}")
        log(f"csv dir: {csv_dir}")
        log(f"file prefix: {file_prefix}")
        log(f"split size: {args.split_size}")
        log(f"mapping file: {mapping_path or '(not used)'}")
        log(f"log dir: {log_dir}")
        log(f"screenshot dir: {screenshot_dir}")
        log(f"part range: {actual_start}..{actual_end}")
        log(f"selected parts: {len(part_jobs)}")
        log(f"csv headers: {headers}")
        if mappings:
            mapping_summary = [f"{mapping.name}->{mapping.option_text}" for mapping in mappings]
            log(f"active mappings ({len(mappings)}): {mapping_summary}")
        else:
            log("active mappings: [] (all columns skipped or left as auto-mapped)")
        log(f"state file: {state_path}")

        credential: LoginCredential | None = None
        if credential_path is not None:
            try:
                credential = parse_credential_file(credential_path)
                log(f"credential file loaded: {credential_path}")
            except Exception as exc:
                if not args.manual_login_fallback:
                    raise RuntimeError(f"credential file load failed: {exc}") from exc
                log(f"credential file load failed, manual fallback enabled: {exc}")

        completed_parts = load_completed_parts(state_path) if state_path.exists() else set()
        if completed_parts:
            log(f"loaded completed parts from state: {sorted(completed_parts)}")

        manager = vibium.browser_sync()
        session = manager.launch(headless=args.headless)

        ensure_recatch_login(
            session=session,
            login_url=login_url,
            leads_url=leads_url,
            credential=credential,
            manual_login_fallback=args.manual_login_fallback,
            log=log,
        )

        total_jobs = len(part_jobs)
        for job_index, (part, csv_path) in enumerate(part_jobs, start=1):
            part_label = f"part {job_index}/{total_jobs}"

            if args.skip_completed and part in completed_parts:
                log(f"[{part_label}] skipped by state file: {csv_path.name}")
                continue

            log(f"[{part_label}] start: {csv_path.name} (part {part:03d})")
            result = import_csv_part(
                session=session,
                import_url=import_url,
                csv_path=csv_path,
                upload_timeout_sec=args.upload_timeout_sec,
                mappings=mappings,
                expected_select_count=len(headers),
                part_label=part_label,
            )
            log(f"[{part_label}] done: {result}")

            completed_parts.add(part)
            write_state_file(
                state_path=state_path,
                base_url=base_url,
                team_slug=args.team_slug,
                record_type_id=args.record_type_id,
                start=actual_start,
                end=actual_end,
                completed_parts=completed_parts,
            )

            if args.delay_between_parts > 0 and job_index != total_jobs:
                time.sleep(args.delay_between_parts)

        log(f"completed all requested parts: {sorted(completed_parts)}")
        return 0
    except KeyboardInterrupt:
        log("interrupted by user")
        return 130
    except Exception as exc:
        log(f"bulk import failed: {exc}")
        if session is not None:
            screenshot = save_screenshot(session, "bulk-import-error")
            log(f"error screenshot: {screenshot}")
            log(f"current url: {current_url(session)}")
            log(f"page excerpt: {visible_page_excerpt(session)}")
        return 1
    finally:
        if session is None:
            pass
        elif args.keep_open:
            log("browser kept open")
        else:
            session.quit()
            log("browser closed")


if __name__ == "__main__":
    sys.exit(main())
