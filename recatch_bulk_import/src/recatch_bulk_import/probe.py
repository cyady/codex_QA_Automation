from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import time
from pathlib import Path
from typing import Any, Sequence

import vibium

from .auth import ensure_recatch_login, parse_credential_file
from .cli import (
    NEXT_LABEL,
    build_import_url,
    build_leads_url,
    build_login_url,
    click_at,
    click_enabled_button,
    current_url,
    determine_runtime_root,
    ensure_import_page_ready,
    env_flag,
    env_int,
    eval_js,
    load_env_file,
    locate_dropdown_option,
    mapping_select_timeout_sec,
    mapping_page_state,
    normalize_base_url,
    prepare_select_query,
    read_mapping_select_texts,
    resolve_input_path,
    resolve_optional_input_path,
    resolve_output_path,
    selected_option_state,
    set_runtime_paths,
    set_textarea_value,
    visible_page_excerpt,
    wait_until,
)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    bootstrap = argparse.ArgumentParser(add_help=False)
    bootstrap.add_argument("--env-file")
    bootstrap_args, _ = bootstrap.parse_known_args(argv)
    loaded_env_file = load_env_file(bootstrap_args.env_file)

    parser = argparse.ArgumentParser(
        description="Probe a single field mapping option without completing the bulk import."
    )
    parser.add_argument("--env-file", default=str(loaded_env_file) if loaded_env_file else None)
    parser.add_argument("--base-url", default=os.getenv("RECATCH_BASE_URL", ""))
    parser.add_argument("--team-slug", default=os.getenv("RECATCH_TEAM_SLUG", ""))
    parser.add_argument(
        "--record-type-id",
        type=int,
        default=env_int("RECATCH_RECORD_TYPE_ID", 0),
    )
    parser.add_argument("--login-url", default=os.getenv("RECATCH_LOGIN_URL", ""))
    parser.add_argument("--leads-url", default=os.getenv("RECATCH_LEADS_URL", ""))
    parser.add_argument("--import-url", default=os.getenv("RECATCH_IMPORT_URL", ""))
    parser.add_argument(
        "--credential-file",
        default=os.getenv("RECATCH_CREDENTIAL_FILE", "credentials/recatch_login.txt"),
    )
    parser.add_argument(
        "--source-csv",
        required=True,
        help="source CSV to copy a sample row from",
    )
    parser.add_argument(
        "--artifact-dir",
        default="logs/probe",
        help="directory to store the generated probe CSV, screenshot, and JSON result",
    )
    parser.add_argument(
        "--screenshot-dir",
        default=os.getenv("RECATCH_SCREENSHOT_DIR", "screenshots"),
    )
    parser.add_argument("--extra-column-name", default="QA_TEST")
    parser.add_argument("--extra-value", default="qa.mapping.test@yopmail.com")
    parser.add_argument("--mapping-query", required=True)
    parser.add_argument("--mapping-option-text", default="")
    parser.add_argument(
        "--group-label",
        default="",
        help="optional dropdown group label to expand before locating the option",
    )
    parser.add_argument(
        "--select-index",
        type=int,
        default=None,
        help="0-based mapping select index; defaults to the last column after appending the probe column",
    )
    parser.add_argument(
        "--headless",
        action=argparse.BooleanOptionalAction,
        default=env_flag("RECATCH_HEADLESS", False),
    )
    parser.add_argument(
        "--keep-open",
        action=argparse.BooleanOptionalAction,
        default=False,
    )
    parser.set_defaults(loaded_env_file=loaded_env_file)
    return parser.parse_args(argv)


def count_visible_selects(session: "vibium.browser_sync.VibeSync") -> int:
    value = eval_js(
        session,
        """
(() => {
  const isVisible = (el) => {
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.display !== "none" && s.visibility !== "hidden";
  };
  return [...document.querySelectorAll(".recatch-ant-select")]
    .filter((el) => isVisible(el))
    .length;
})()
""",
    )
    return int(value or 0)


def wait_for_dropdown(session: "vibium.browser_sync.VibeSync", timeout_sec: float) -> bool:
    return wait_until(
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
  return [...document.querySelectorAll(".recatch-ant-select-dropdown")]
    .some((el) => isVisible(el));
})()
""",
            )
        ),
        timeout_sec=timeout_sec,
        interval_sec=0.15,
    )


def dropdown_text_dump(session: "vibium.browser_sync.VibeSync", limit: int = 80) -> dict[str, Any]:
    result = eval_js(
        session,
        f"""
(() => {{
  const normalize = (value) => (value || "").replace(/\\s+/g, " ").trim();
  const isVisible = (el) => {{
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.display !== "none" && s.visibility !== "hidden";
  }};
  const dropdown = [...document.querySelectorAll(".recatch-ant-select-dropdown")]
    .filter((el) => isVisible(el))
    .sort((a, b) => b.getBoundingClientRect().height - a.getBoundingClientRect().height)[0];
  if (!dropdown) return {{ ok: false, reason: "dropdown_not_found" }};

  const texts = [...dropdown.querySelectorAll("*")]
    .filter((el) => isVisible(el))
    .map((el) => normalize(el.innerText || el.textContent || ""))
    .filter(Boolean);

  return {{
    ok: true,
    texts: [...new Set(texts)].slice(0, {limit}),
  }};
}})()
""",
    )
    return result if isinstance(result, dict) else {"ok": False, "raw": result}


def expand_dropdown_group(
    session: "vibium.browser_sync.VibeSync",
    group_label: str,
) -> dict[str, Any]:
    result = eval_js(
        session,
        f"""
(() => {{
  const wanted = ({json.dumps(group_label, ensure_ascii=False)} || "").replace(/\\s+/g, " ").trim();
  const normalize = (value) => (value || "").replace(/\\s+/g, " ").trim();
  const escapeRegExp = (value) => value.replace(/[.*+?^${{}}()|[\\]\\\\]/g, "\\\\$&");
  const isVisible = (el) => {{
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.display !== "none" && s.visibility !== "hidden";
  }};
  const dropdown = [...document.querySelectorAll(".recatch-ant-select-dropdown")]
    .filter((el) => isVisible(el))
    .sort((a, b) => b.getBoundingClientRect().height - a.getBoundingClientRect().height)[0];
  if (!dropdown) return {{ ok: false, reason: "dropdown_not_found" }};

  const re = new RegExp(`^${{escapeRegExp(wanted)}}(?:\\\\s+\\\\d+)?$`);
  const candidates = [...dropdown.querySelectorAll("*")]
    .filter((el) => isVisible(el))
    .map((el) => {{
      const rect = el.getBoundingClientRect();
      const text = normalize(el.innerText || el.textContent || "");
      return {{
        el,
        text,
        x: rect.left,
        y: rect.top,
        w: rect.width,
        h: rect.height,
      }};
    }})
    .filter((item) => item.text && re.test(item.text))
    .sort((a, b) => a.text.length - b.text.length || a.y - b.y || a.x - b.x);

  const candidate = candidates[0];
  if (!candidate) {{
    return {{ ok: false, reason: "group_not_found", wanted }};
  }}

  const target =
    candidate.el.closest(".recatch-ant-collapse-header")
    || candidate.el.closest("[aria-expanded]")
    || candidate.el.closest("[role='button']")
    || candidate.el;

  ["pointerdown", "mousedown", "mouseup", "click"].forEach((name) => {{
    target.dispatchEvent(new MouseEvent(name, {{
      bubbles: true,
      cancelable: true,
      view: window,
    }}));
  }});
  if (typeof target.click === "function") {{
    target.click();
  }}

  return {{
    ok: true,
    text: normalize(target.innerText || target.textContent || ""),
    ariaExpanded: target.getAttribute("aria-expanded") || "",
  }};
}})()
""",
    )
    return result if isinstance(result, dict) else {"ok": False, "raw": result}


def write_probe_csv(
    source_csv: Path,
    output_csv: Path,
    extra_column_name: str,
    extra_value: str,
) -> list[str]:
    with source_csv.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        first_row = next(reader)
        fieldnames = list(reader.fieldnames or [])

    fieldnames.append(extra_column_name)
    first_row[extra_column_name] = extra_value

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(first_row)

    return fieldnames


def save_probe_artifacts(
    session: "vibium.browser_sync.VibeSync",
    screenshot_path: Path,
    result_path: Path,
    payload: dict[str, Any],
) -> None:
    screenshot_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.parent.mkdir(parents=True, exist_ok=True)
    screenshot_path.write_bytes(session.screenshot())
    result_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    runtime_root = determine_runtime_root(args.loaded_env_file)
    bootstrap_screenshot_dir = Path(args.screenshot_dir).expanduser()
    if not bootstrap_screenshot_dir.is_absolute():
        bootstrap_screenshot_dir = (runtime_root / bootstrap_screenshot_dir).resolve()
    else:
        bootstrap_screenshot_dir = bootstrap_screenshot_dir.resolve()
    set_runtime_paths(runtime_root=runtime_root, screenshot_dir=bootstrap_screenshot_dir)

    artifact_dir = resolve_output_path(args.artifact_dir)
    screenshot_dir = resolve_output_path(args.screenshot_dir)
    set_runtime_paths(runtime_root=runtime_root, screenshot_dir=screenshot_dir)

    base_url = normalize_base_url(args.base_url)
    login_url = args.login_url or build_login_url(base_url, args.team_slug)
    leads_url = args.leads_url or build_leads_url(base_url, args.team_slug)
    import_url = args.import_url or build_import_url(base_url, args.team_slug, args.record_type_id)
    source_csv = resolve_input_path(args.source_csv)
    credential_path = resolve_optional_input_path(args.credential_file)
    if credential_path is None:
        raise FileNotFoundError("credential file is required")
    credential = parse_credential_file(credential_path)

    ts = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    probe_csv_path = artifact_dir / f"probe-input-{ts}.csv"
    screenshot_path = screenshot_dir / f"probe-mapping-{ts}.png"
    result_path = artifact_dir / f"probe-result-{ts}.json"

    fieldnames = write_probe_csv(
        source_csv=source_csv,
        output_csv=probe_csv_path,
        extra_column_name=args.extra_column_name,
        extra_value=args.extra_value,
    )
    target_select_index = args.select_index if args.select_index is not None else len(fieldnames) - 1
    mapping_option_text = args.mapping_option_text or args.mapping_query

    manager = vibium.browser_sync()
    session = manager.launch(headless=args.headless)
    payload: dict[str, Any] = {
        "ok": False,
        "baseUrl": base_url,
        "loginUrl": login_url,
        "leadsUrl": leads_url,
        "importUrl": import_url,
        "sourceCsv": str(source_csv),
        "probeCsv": str(probe_csv_path),
        "credentialFile": str(credential_path),
        "extraColumnName": args.extra_column_name,
        "mappingQuery": args.mapping_query,
        "mappingOptionText": mapping_option_text,
        "groupLabel": args.group_label,
        "selectIndex": target_select_index,
        "artifactResult": str(result_path),
        "artifactScreenshot": str(screenshot_path),
    }

    try:
        ensure_recatch_login(
            session=session,
            login_url=login_url,
            leads_url=leads_url,
            credential=credential,
            manual_login_fallback=False,
            log=lambda _: None,
        )

        ensure_import_page_ready(session, import_url)
        csv_text = probe_csv_path.read_text(encoding="utf-8")
        payload["paste"] = set_textarea_value(session, csv_text)
        click_enabled_button(session, NEXT_LABEL, timeout_sec=20.0)

        payload["mappingReady"] = wait_until(
            lambda: bool(mapping_page_state(session).get("ready")),
            timeout_sec=20.0,
            interval_sec=0.2,
        )
        select_timeout_sec = mapping_select_timeout_sec(target_select_index + 1)
        payload["mappingSelectsReady"] = wait_until(
            lambda: count_visible_selects(session) >= target_select_index + 1,
            timeout_sec=select_timeout_sec,
            interval_sec=0.2,
        )
        payload["mappingSelectTimeoutSec"] = select_timeout_sec
        payload["visibleSelectCount"] = count_visible_selects(session)
        payload["mappingSelectsBefore"] = read_mapping_select_texts(session)

        payload["prepared"] = prepare_select_query(session, target_select_index, args.mapping_query)
        payload["dropdownReady"] = wait_for_dropdown(session, timeout_sec=5.0)
        time.sleep(0.6)
        payload["dropdownBefore"] = dropdown_text_dump(session)

        if args.group_label:
            payload["groupExpand"] = expand_dropdown_group(session, args.group_label)
            time.sleep(0.6)
            payload["dropdownAfterGroup"] = dropdown_text_dump(session)

        payload["located"] = locate_dropdown_option(session, target_select_index, mapping_option_text)
        if payload["located"].get("ok"):
            payload["clicked"] = click_at(
                session,
                float(payload["located"]["x"]),
                float(payload["located"]["y"]),
            )
            payload["selectedWait"] = wait_until(
                lambda: bool(selected_option_state(session, target_select_index, mapping_option_text).get("selected")),
                timeout_sec=4.0,
                interval_sec=0.15,
            )
            payload["selectedState"] = selected_option_state(session, target_select_index, mapping_option_text)
            payload["mappingSelectsAfter"] = read_mapping_select_texts(session)
            payload["ok"] = bool(payload["selectedState"].get("selected"))
        else:
            payload["selectedState"] = selected_option_state(session, target_select_index, mapping_option_text)

        payload["currentUrl"] = current_url(session)
        payload["pageExcerpt"] = visible_page_excerpt(session, limit=25)
        save_probe_artifacts(session, screenshot_path, result_path, payload)
        print(json.dumps(payload, ensure_ascii=False))
        return 0 if payload.get("ok") else 1
    except Exception as exc:
        payload["error"] = f"{type(exc).__name__}: {exc}"
        payload["currentUrl"] = current_url(session)
        payload["pageExcerpt"] = visible_page_excerpt(session, limit=25)
        save_probe_artifacts(session, screenshot_path, result_path, payload)
        print(json.dumps(payload, ensure_ascii=False))
        return 1
    finally:
        if not args.keep_open:
            session.quit()


if __name__ == "__main__":
    raise SystemExit(main())
