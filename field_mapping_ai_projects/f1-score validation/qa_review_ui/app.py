from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import re
import subprocess
import sys

import altair as alt
import streamlit as st


APP_DIR = Path(__file__).resolve().parent
DATA_DIR = APP_DIR / "data"
DECISIONS_ROOT_DIR = DATA_DIR / "decisions"
DECISIONS_ROOT_DIR.mkdir(parents=True, exist_ok=True)
LAST_INPUTS_PATH = DATA_DIR / "last_inputs.json"
PRELINKED_DECISION_INDEX_RANGE = range(1, 51)
WS_RE = re.compile(r"\s+")
CURRENT_DECISION_SOURCE = "__current__"


def read_json(path: str) -> Any:
    p = Path(path)
    return json.loads(p.read_text(encoding="utf-8-sig"))


def read_json_or_jsonl(path: str) -> Any:
    p = Path(path)
    text = p.read_text(encoding="utf-8-sig").strip()
    if not text:
        return None
    # Prefer extension-aware parsing first.
    if p.suffix.lower() == ".jsonl":
        return [json.loads(line) for line in text.splitlines() if line.strip()]
    # Fallback: try JSON, then JSONL (for mislabeled files).
    try:
        if text.startswith("{") or text.startswith("["):
            return json.loads(text)
    except json.JSONDecodeError:
        pass
    return [json.loads(line) for line in text.splitlines() if line.strip()]


def _hangul_count(s: str) -> int:
    return sum(1 for ch in s if "\uac00" <= ch <= "\ud7a3")


def _latin_noise_count(s: str) -> int:
    return sum(1 for ch in s if "\u00c0" <= ch <= "\u024f")


def fix_mojibake_text(s: str) -> str:
    if not isinstance(s, str) or not s:
        return s
    try:
        repaired = s.encode("latin1").decode("utf-8")
    except Exception:
        return s
    before_score = _hangul_count(s) - _latin_noise_count(s)
    after_score = _hangul_count(repaired) - _latin_noise_count(repaired)
    return repaired if after_score > before_score else s


def fix_mojibake_obj(v: Any) -> Any:
    if isinstance(v, str):
        return fix_mojibake_text(v)
    if isinstance(v, list):
        return [fix_mojibake_obj(x) for x in v]
    if isinstance(v, dict):
        return {k: fix_mojibake_obj(val) for k, val in v.items()}
    return v


def flatten_model_output(payload: Any) -> list[dict[str, Any]]:
    if payload is None:
        return []
    if isinstance(payload, dict):
        return [payload]
    if isinstance(payload, list):
        out: list[dict[str, Any]] = []
        for x in payload:
            if isinstance(x, dict):
                out.append(x)
            elif isinstance(x, list):
                out.extend(flatten_model_output(x))
        return out
    return []


def load_candidate_pool(path: str) -> dict[str, Any]:
    payload = read_json_or_jsonl(path)
    if isinstance(payload, list):
        if not payload:
            return {"memo_id": "UNKNOWN", "candidates": []}
        return payload[0]
    return payload


def load_fn_candidates(path: str) -> list[dict[str, Any]]:
    payload = read_json_or_jsonl(path)
    if isinstance(payload, list):
        return payload
    return [payload]


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def get_field_map(effective_schema: dict[str, Any]) -> dict[str, dict[str, Any]]:
    fields = effective_schema.get("effective_fields", [])
    return {str(f.get("id")): fix_mojibake_obj(f) for f in fields}


def option_value_to_label_map(field_def: dict[str, Any]) -> dict[str, str]:
    attrs = field_def.get("attributes") or {}
    opts = attrs.get("options") if isinstance(attrs, dict) else None
    if not isinstance(opts, list):
        return {}
    out: dict[str, str] = {}
    for o in opts:
        if not isinstance(o, dict):
            continue
        ov = o.get("value")
        label = o.get("label")
        if ov is None:
            continue
        out[str(ov)] = fix_mojibake_text(str(label)) if label is not None else str(ov)
    return out


def format_extracted_value(item: dict[str, Any], field_map: dict[str, dict[str, Any]]) -> str:
    fd = fix_mojibake_obj(item.get("field_definition") or {})
    extracted = fix_mojibake_obj(item.get("extracted_value"))
    field_id = str(fd.get("id")) if fd.get("id") is not None else ""
    field_type = str(fd.get("type") or "")

    ref_def = field_map.get(field_id, {})
    ov_map = option_value_to_label_map(fd)
    if not ov_map and ref_def:
        ov_map = option_value_to_label_map(ref_def)

    if field_type in ("select", "multi-select"):
        labels: list[str] = []
        if isinstance(extracted, list):
            for x in extracted:
                if isinstance(x, dict) and "value" in x:
                    key = str(x["value"])
                    labels.append(f"{ov_map.get(key, key)} ({key})")
                else:
                    key = str(x)
                    labels.append(f"{ov_map.get(key, key)} ({key})")
        elif isinstance(extracted, dict) and "value" in extracted:
            key = str(extracted["value"])
            labels.append(f"{ov_map.get(key, key)} ({key})")
        else:
            key = str(extracted)
            labels.append(f"{ov_map.get(key, key)} ({key})")
        return ", ".join(labels)

    return json.dumps(extracted, ensure_ascii=False, indent=2) if isinstance(extracted, (list, dict)) else str(extracted)


def char_to_line_no(text: str, char_idx: Any) -> int | None:
    if not isinstance(char_idx, int):
        return None
    if char_idx < 0:
        return None
    if char_idx > len(text):
        char_idx = len(text)
    return text.count("\n", 0, char_idx) + 1


def get_line_text(text: str, line_no: int | None) -> str | None:
    if line_no is None:
        return None
    lines = text.splitlines()
    if line_no <= 0 or line_no > len(lines):
        return None
    return lines[line_no - 1]


def field_option_label(field_id: str, field_map: dict[str, dict[str, Any]]) -> str:
    if not field_id:
        return "(unassigned)"
    f = field_map.get(str(field_id)) or {}
    label = fix_mojibake_text(str(f.get("label") or "UNKNOWN"))
    ftype = str(f.get("type") or "-")
    return f"{field_id} | {label} | {ftype}"


def suggest_fn_output_path(candidate_pool_path: str) -> str:
    p = Path(candidate_pool_path)
    stem = p.stem
    return str(Path("schema_generator/output") / f"{stem}_fn_review_input.json")


def _path_ok(path_str: str) -> bool:
    s = (path_str or "").strip()
    return bool(s) and Path(s).exists()


def _sanitize_user_key(v: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9._@:-]+", "_", (v or "").strip())
    return s[:120] if s else "local_default"


def detect_user_key() -> str:
    # Best-effort identifier for per-user persistence across devices.
    try:
        ctx = st.context
    except Exception:
        return "local_default"

    ip = getattr(ctx, "ip_address", None)
    if ip:
        return _sanitize_user_key(f"ip:{ip}")

    headers_obj = getattr(ctx, "headers", None)
    if headers_obj:
        try:
            headers = {str(k).lower(): str(v) for k, v in dict(headers_obj).items()}
        except Exception:
            headers = {}
        for key in ("x-forwarded-for", "x-real-ip", "cf-connecting-ip", "remote_addr"):
            if headers.get(key):
                return _sanitize_user_key(f"ip:{headers[key].split(',')[0].strip()}")
        ua = headers.get("user-agent")
        if ua:
            return _sanitize_user_key(f"ua:{ua[:64]}")
    return "local_default"


def load_last_inputs(user_key: str | None = None) -> dict[str, str]:
    if not LAST_INPUTS_PATH.exists():
        return {}
    try:
        data = json.loads(LAST_INPUTS_PATH.read_text(encoding="utf-8-sig"))
        if not isinstance(data, dict):
            return {}
        # New format: per-user profiles.
        if isinstance(data.get("profiles"), dict):
            key = _sanitize_user_key(user_key or str(data.get("active_user") or "local_default"))
            raw_profile = data["profiles"].get(key, {})
            if isinstance(raw_profile, dict):
                return {str(k): str(v) for k, v in raw_profile.items()}
            return {}
        # Backward compatibility: single global profile.
        return {str(k): str(v) for k, v in data.items()}
    except Exception:
        pass
    return {}


def save_last_inputs(data: dict[str, str], user_key: str) -> None:
    key = _sanitize_user_key(user_key)
    LAST_INPUTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload: dict[str, Any] = {"profiles": {}, "active_user": key}
    if LAST_INPUTS_PATH.exists():
        try:
            existing = json.loads(LAST_INPUTS_PATH.read_text(encoding="utf-8-sig"))
            if isinstance(existing, dict) and isinstance(existing.get("profiles"), dict):
                payload["profiles"] = existing["profiles"]
            elif isinstance(existing, dict):
                # Migrate legacy flat structure into a default profile.
                payload["profiles"] = {"local_default": {str(k): str(v) for k, v in existing.items()}}
        except Exception:
            pass
    payload["profiles"][key] = {str(k): str(v) for k, v in data.items()}
    payload["active_user"] = key
    LAST_INPUTS_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def list_decision_sources() -> list[tuple[str, str, Path]]:
    DECISIONS_ROOT_DIR.mkdir(parents=True, exist_ok=True)
    sources: list[tuple[str, str, Path]] = [(CURRENT_DECISION_SOURCE, "current (decisions/)", DECISIONS_ROOT_DIR)]
    for p in sorted(DECISIONS_ROOT_DIR.iterdir()):
        if p.is_dir():
            sources.append((p.name, p.name, p))
    return sources


def resolve_decisions_dir(source_key: str) -> Path:
    if source_key == CURRENT_DECISION_SOURCE:
        return DECISIONS_ROOT_DIR
    candidate = DECISIONS_ROOT_DIR / str(source_key)
    if candidate.is_dir():
        return candidate
    return DECISIONS_ROOT_DIR


def decision_file(memo_id: str, decisions_dir: Path) -> Path:
    return decisions_dir / f"{memo_id}.json"


def _extract_index_from_name(name: str, pattern: str) -> int | None:
    m = re.search(pattern, name, flags=re.IGNORECASE)
    if not m:
        return None
    try:
        return int(m.group(1))
    except Exception:
        return None


def derive_decision_key(memo_text_path: str, model_output_path: str, fn_rows: list[dict[str, Any]]) -> tuple[str, list[str]]:
    memo_name = Path(memo_text_path).name
    model_name = Path(model_output_path).name
    memo_idx = _extract_index_from_name(memo_name, r"memo_w(\d+)\.txt$")
    model_idx = _extract_index_from_name(model_name, r"bc(\d+)_model_output\.json$")

    notes: list[str] = []
    if memo_idx is not None and model_idx is not None:
        if memo_idx == model_idx:
            return f"M-W{memo_idx}", notes
        notes.append(
            "memo_text와 model_output 인덱스가 다릅니다. "
            f"(memo_w{memo_idx} vs bc{model_idx})"
        )
        return f"M-W{memo_idx}__BC{model_idx}", notes
    if memo_idx is not None:
        return f"M-W{memo_idx}", notes

    fn_memo_id = fn_rows[0].get("memo_id") if fn_rows else None
    if fn_memo_id:
        notes.append("memo_text 파일명에서 memo_id를 추출하지 못해 FN input의 memo_id를 사용합니다.")
        return str(fn_memo_id), notes
    notes.append("memo_id를 자동 추출하지 못해 UNKNOWN 키를 사용합니다.")
    return "UNKNOWN", notes


def base_memo_id_from_key(memo_key: str) -> str:
    return str(memo_key).split("__BC", 1)[0]


def memo_widget_key(memo_id: str, suffix: str) -> str:
    safe_memo_id = "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in str(memo_id))
    return f"{safe_memo_id}__{suffix}"


def extract_memo_index_from_context(memo_text_path: str, model_output_path: str, memo_id: str | None = None) -> int | None:
    memo_name = Path(memo_text_path or "").name
    model_name = Path(model_output_path or "").name
    memo_idx = _extract_index_from_name(memo_name, r"memo_w(\d+)\.txt$")
    if memo_idx is not None:
        return memo_idx
    model_idx = _extract_index_from_name(model_name, r"bc(\d+)_model_output\.json$")
    if model_idx is not None:
        return model_idx
    if memo_id:
        key_idx = _extract_index_from_name(str(memo_id), r"M-W(\d+)")
        if key_idx is not None:
            return key_idx
    return None


def replace_index_in_path(path_str: str, new_idx: int) -> str:
    s = str(path_str or "")
    patterns = [
        (r"memo_w(\d+)\.txt$", f"memo_w{new_idx}.txt"),
        (r"bc(\d+)_model_output\.json$", f"bc{new_idx}_model_output.json"),
        (r"bc(\d+)_fn_review_input\.json$", f"bc{new_idx}_fn_review_input.json"),
        (r"w(\d+)_fn_review_input\.json$", f"w{new_idx}_fn_review_input.json"),
        (r"bc(\d+)\.json$", f"bc{new_idx}.json"),
        (r"([/\\\\])w(\d+)([/\\\\])candidate_pool\.jsonl$", rf"\\1w{new_idx}\\3candidate_pool.jsonl"),
    ]
    for pattern, repl in patterns:
        if re.search(pattern, s, flags=re.IGNORECASE):
            return re.sub(pattern, repl, s, flags=re.IGNORECASE)
    return s


def available_decision_indices(decisions_dir: Path) -> list[int]:
    out: list[int] = []
    for p in decisions_dir.glob("M-W*.json"):
        idx = _extract_index_from_name(p.name, r"M-W(\d+)\.json$")
        if idx is not None:
            out.append(idx)
    return sorted(set(out))


def navigation_decision_indices(prelinked_start: int, prelinked_end: int, decisions_dir: Path) -> list[int]:
    lo = max(1, int(prelinked_start))
    hi = max(1, int(prelinked_end))
    if lo > hi:
        lo, hi = hi, lo
    prelinked = set(range(lo, hi + 1))
    return sorted(prelinked.union(available_decision_indices(decisions_dir)))


def current_choice(key: str, default: str, allowed: list[str]) -> str:
    value = st.session_state.get(key, default)
    if value not in allowed:
        return default
    return value


def _norm_text(v: Any) -> str:
    if v is None:
        return ""
    return WS_RE.sub(" ", str(v)).strip()


def fn_row_signature(row: dict[str, Any]) -> str:
    ev = row.get("evidence") or {}
    parts = [
        _norm_text(row.get("semantic_type")),
        _norm_text(row.get("value_type")),
        _norm_text(row.get("raw_text")),
        _norm_text(ev.get("exact_quote")),
    ]
    return "|".join(parts)


def fn_decision_signature(row: dict[str, Any]) -> str:
    parts = [
        _norm_text(row.get("semantic_type")),
        _norm_text(row.get("value_type")),
        _norm_text(row.get("raw_text")),
        _norm_text(row.get("evidence_quote")),
    ]
    return "|".join(parts)


def load_existing_decisions(
    memo_id: str,
    decisions_dir: Path,
    fallback_memo_ids: list[str] | None = None,
) -> dict[str, Any]:
    probe_ids = [memo_id]
    if fallback_memo_ids:
        probe_ids.extend([x for x in fallback_memo_ids if x and x not in probe_ids])
    for probe_id in probe_ids:
        fp = decision_file(probe_id, decisions_dir)
        if fp.exists():
            return json.loads(fp.read_text(encoding="utf-8-sig"))
    return {"memo_id": memo_id, "updated_at": None, "model_decisions": [], "fn_decisions": []}


def save_decisions(payload: dict[str, Any], decisions_dir: Path) -> None:
    decisions_dir.mkdir(parents=True, exist_ok=True)
    fp = decision_file(payload["memo_id"], decisions_dir)
    fp.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def aggregate_counts(
    decisions_dir: Path,
    field_map: dict[str, dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    counts: dict[str, dict[str, Any]] = {}
    field_map = field_map or {}
    for fp in decisions_dir.glob("*.json"):
        try:
            data = json.loads(fp.read_text(encoding="utf-8-sig"))
        except Exception:
            continue
        for row in data.get("model_decisions", []):
            field_id = str(row.get("field_id") or "UNASSIGNED")
            default_label = ""
            if field_id in field_map:
                default_label = fix_mojibake_text(str(field_map[field_id].get("label") or ""))
            elif row.get("field_label"):
                default_label = fix_mojibake_text(str(row.get("field_label")))
            bucket = counts.setdefault(
                field_id, {"field_id": field_id, "label": default_label, "tp": 0, "fp": 0, "fn": 0}
            )
            if not bucket.get("label"):
                bucket["label"] = default_label
            decision = row.get("decision")
            if decision == "TP":
                bucket["tp"] += 1
            elif decision == "FP":
                bucket["fp"] += 1
        for row in data.get("fn_decisions", []):
            if row.get("decision") != "FN":
                continue
            field_id = str(row.get("assigned_field_id") or "UNASSIGNED")
            default_label = ""
            if field_id in field_map:
                default_label = fix_mojibake_text(str(field_map[field_id].get("label") or ""))
            bucket = counts.setdefault(
                field_id, {"field_id": field_id, "label": default_label, "tp": 0, "fp": 0, "fn": 0}
            )
            if not bucket.get("label"):
                bucket["label"] = default_label
            bucket["fn"] += 1
    return sorted(
        counts.values(),
        key=lambda x: (-(x["tp"] + x["fp"] + x["fn"]), x["field_id"]),
    )


def app() -> None:
    st.set_page_config(page_title="QA Review UI", layout="wide")
    st.title("QA Review UI")
    st.caption("Review memo + model_output + FN candidates in one place, and track field TP/FP/FN.")

    detected_user_key = detect_user_key()
    if "reviewer_id" not in st.session_state:
        st.session_state["reviewer_id"] = detected_user_key
    reviewer_id = _sanitize_user_key(st.session_state.get("reviewer_id", detected_user_key))
    prev_active_user = st.session_state.get("active_profile_user")
    profile_switched = prev_active_user is not None and prev_active_user != reviewer_id
    st.session_state["active_profile_user"] = reviewer_id

    remembered = load_last_inputs(reviewer_id)
    path_defaults = {
        "memo_text_path": remembered.get("memo_text_path", "agent_a/data_w/memo_w1.txt"),
        "candidate_pool_path": remembered.get("candidate_pool_path", "agent_a/outputs/runs_merged/w1/candidate_pool.jsonl"),
        "model_output_path": remembered.get("model_output_path", "agent_a/model_output/w1_model_output.json"),
        "fn_input_path_input": remembered.get("fn_input_path_input", "schema_generator/output/w1_fn_review_input.json"),
        "effective_schema_path_input": remembered.get("effective_schema_path_input", "schema_generator/output/effective_schema_566552.json"),
        "deal_id_for_schema": remembered.get("deal_id_for_schema", "566552"),
        "decision_source": remembered.get("decision_source", CURRENT_DECISION_SOURCE),
    }
    for k, v in path_defaults.items():
        if profile_switched or k not in st.session_state:
            st.session_state[k] = v
    if profile_switched:
        st.session_state["loaded"] = False

    decision_sources = list_decision_sources()
    decision_source_keys = [k for k, _, _ in decision_sources]
    decision_source_labels = {k: label for k, label, _ in decision_sources}
    if st.session_state.get("decision_source") not in decision_source_keys:
        st.session_state["decision_source"] = CURRENT_DECISION_SOURCE

    if "pending_effective_schema_path" in st.session_state:
        st.session_state["effective_schema_path_input"] = st.session_state.pop("pending_effective_schema_path")
    if "pending_fn_input_path" in st.session_state:
        st.session_state["fn_input_path_input"] = st.session_state.pop("pending_fn_input_path")
    if "pending_nav_paths" in st.session_state:
        pending_nav = st.session_state.pop("pending_nav_paths") or {}
        for k, v in pending_nav.items():
            st.session_state[k] = v

    with st.sidebar:
        st.subheader("Input Files")
        st.text_input(
            "Reviewer ID (per-user last inputs)",
            key="reviewer_id",
            help="Different Reviewer ID keeps separate last input paths.",
        )
        st.caption(f"Detected user key: `{detected_user_key}`")
        decision_source = st.selectbox(
            "Decision build version",
            options=decision_source_keys,
            index=decision_source_keys.index(st.session_state.get("decision_source", CURRENT_DECISION_SOURCE)),
            format_func=lambda x: decision_source_labels.get(x, x),
            key="decision_source",
        )
        decisions_dir = resolve_decisions_dir(decision_source)
        st.caption(f"Decision path: `{decisions_dir}`")
        memo_text_path = st.text_input("Memo text (.txt)", key="memo_text_path")
        candidate_pool_path = st.text_input("candidate_pool (.json/.jsonl)", key="candidate_pool_path")
        model_output_path = st.text_input("model_output (.json/.jsonl)", key="model_output_path")
        fn_input_path = st.text_input("FN review input (.json/.jsonl)", key="fn_input_path_input")
        effective_schema_path = st.text_input("effective_schema (.json)", key="effective_schema_path_input")
        st.caption("Decision Key Navigation Range")
        nav_range_col1, nav_range_col2 = st.columns(2)
        with nav_range_col1:
            prelinked_start = int(
                st.number_input(
                    "Start",
                    min_value=1,
                    value=PRELINKED_DECISION_INDEX_RANGE.start,
                    step=1,
                )
            )
        with nav_range_col2:
            prelinked_end = int(
                st.number_input(
                    "End",
                    min_value=1,
                    value=PRELINKED_DECISION_INDEX_RANGE.stop - 1,
                    step=1,
                )
            )
        memo_idx_now = extract_memo_index_from_context(
            memo_text_path,
            model_output_path,
            st.session_state.get("memo_id"),
        )
        idxs = navigation_decision_indices(prelinked_start, prelinked_end, decisions_dir)
        if memo_idx_now is not None:
            st.caption(f"Current Memo Index: `{memo_idx_now}`")
        if idxs:
            st.caption(f"Decision Range: `{idxs[0]} ~ {idxs[-1]}`")
        prev_disabled = (memo_idx_now is None) or (not idxs) or (memo_idx_now <= idxs[0])
        next_disabled = (memo_idx_now is None) or (not idxs) or (memo_idx_now >= idxs[-1])
        nav_col1, nav_col2 = st.columns(2)
        with nav_col1:
            if st.button("← Prev", disabled=prev_disabled):
                target = (memo_idx_now or 0) - 1
                st.session_state["pending_nav_paths"] = {
                    "memo_text_path": replace_index_in_path(st.session_state.get("memo_text_path", ""), target),
                    "candidate_pool_path": replace_index_in_path(
                        st.session_state.get("candidate_pool_path", ""), target
                    ),
                    "model_output_path": replace_index_in_path(
                        st.session_state.get("model_output_path", ""), target
                    ),
                    "fn_input_path_input": replace_index_in_path(
                        st.session_state.get("fn_input_path_input", ""), target
                    ),
                }
                st.rerun()
        with nav_col2:
            if st.button("Next →", disabled=next_disabled):
                target = (memo_idx_now or 0) + 1
                st.session_state["pending_nav_paths"] = {
                    "memo_text_path": replace_index_in_path(st.session_state.get("memo_text_path", ""), target),
                    "candidate_pool_path": replace_index_in_path(
                        st.session_state.get("candidate_pool_path", ""), target
                    ),
                    "model_output_path": replace_index_in_path(
                        st.session_state.get("model_output_path", ""), target
                    ),
                    "fn_input_path_input": replace_index_in_path(
                        st.session_state.get("fn_input_path_input", ""), target
                    ),
                }
                st.rerun()

        memo_ok = _path_ok(memo_text_path)
        cp_ok = _path_ok(candidate_pool_path)
        mo_ok = _path_ok(model_output_path)
        es_ok = _path_ok(effective_schema_path)

        st.markdown("---")
        st.subheader("Required Inputs")
        st.caption("memo_text / candidate_pool / model_output are required for this workflow.")
        st.write(f"- memo_text: {'OK' if memo_ok else 'MISSING'}")
        st.write(f"- candidate_pool: {'OK' if cp_ok else 'MISSING'}")
        st.write(f"- model_output: {'OK' if mo_ok else 'MISSING'}")
        st.write(f"- effective_schema: {'OK' if es_ok else 'MISSING'}")

        st.markdown("---")
        st.subheader("Auto Generate effective_schema")
        deal_id_for_schema = st.text_input("deal_id", key="deal_id_for_schema")
        api_token = st.text_input("Bearer token (RECATCH_FB_TOKEN)", value="", type="password", key="api_token")
        generate_schema_btn = st.button(
            "Generate effective_schema from deal_id",
            help="Validates required inputs when clicked, then runs schema generation.",
        )

        st.markdown("---")
        st.subheader("Auto Generate fn_review_input")
        top_k_for_fn = st.number_input("Suggested fields top-k", min_value=1, max_value=20, value=5, step=1)
        generate_fn_btn = st.button(
            "Generate fn_review_input from candidate_pool",
            help="Validates required inputs when clicked, then runs FN input generation.",
        )
        st.caption(
            "top-k controls how many suggested fields are attached to each FN candidate. "
            "Higher values increase recall but add review noise."
        )
        auto_reload_files = st.checkbox("Auto reload files", value=True)
        load_btn = st.button("Load", type="primary")

        if generate_schema_btn:
            missing = []
            if not memo_ok:
                missing.append("memo_text path")
            if not cp_ok:
                missing.append("candidate_pool path")
            if not mo_ok:
                missing.append("model_output path")
            deal_id_text = (deal_id_for_schema or "").strip()
            if missing:
                st.error(f"Missing/invalid required inputs: {', '.join(missing)}")
            elif not deal_id_text.isdigit():
                st.error("deal_id must be numeric.")
            elif not api_token.strip():
                st.error("Enter Bearer token.")
            else:
                out_path = f"schema_generator/output/effective_schema_{deal_id_text}.json"
                cmd = [
                    sys.executable,
                    "schema_generator/build_effective_schema_from_deal.py",
                    "--deal-id",
                    deal_id_text,
                    "--token",
                    api_token.strip(),
                    "--output",
                    out_path,
                ]
                try:
                    proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
                    st.session_state["pending_effective_schema_path"] = out_path
                    st.success(f"Generated: {out_path}")
                    if proc.stdout.strip():
                        st.caption(proc.stdout.strip())
                    st.rerun()
                except subprocess.CalledProcessError as e:
                    st.error("effective_schema generation failed.")
                    msg = (e.stderr or "") + ("\n" if e.stderr and e.stdout else "") + (e.stdout or "")
                    st.code(msg if msg.strip() else "no error output")

        if generate_fn_btn:
            cp = (candidate_pool_path or "").strip()
            mo = (model_output_path or "").strip()
            es = (effective_schema_path or "").strip()
            missing = []
            if not memo_ok:
                missing.append("memo_text path")
            if not cp or not Path(cp).exists():
                missing.append("candidate_pool path")
            if not mo or not Path(mo).exists():
                missing.append("model_output path")
            if not es or not Path(es).exists():
                missing.append("effective_schema path")

            if missing:
                st.error(f"Missing/invalid required inputs: {', '.join(missing)}")
            else:
                out_path = suggest_fn_output_path(cp)
                cmd = [
                    sys.executable,
                    "schema_generator/build_fn_review_input.py",
                    "--candidate-pool",
                    cp,
                    "--model-output",
                    mo,
                    "--effective-schema",
                    es,
                    "--output",
                    out_path,
                    "--top-k",
                    str(int(top_k_for_fn)),
                ]
                try:
                    proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
                    st.session_state["pending_fn_input_path"] = out_path
                    st.success(f"Generated: {out_path}")
                    if proc.stdout.strip():
                        st.caption(proc.stdout.strip())
                    st.rerun()
                except subprocess.CalledProcessError as e:
                    st.error("fn_review_input generation failed.")
                    if e.stderr:
                        st.code(e.stderr)
                    elif e.stdout:
                        st.code(e.stdout)

    save_last_inputs(
        {
            "memo_text_path": st.session_state.get("memo_text_path", ""),
            "candidate_pool_path": st.session_state.get("candidate_pool_path", ""),
            "model_output_path": st.session_state.get("model_output_path", ""),
            "fn_input_path_input": st.session_state.get("fn_input_path_input", ""),
            "effective_schema_path_input": st.session_state.get("effective_schema_path_input", ""),
            "deal_id_for_schema": st.session_state.get("deal_id_for_schema", ""),
            "decision_source": st.session_state.get("decision_source", CURRENT_DECISION_SOURCE),
        },
        user_key=_sanitize_user_key(st.session_state.get("reviewer_id", detected_user_key)),
    )

    if "loaded" not in st.session_state:
        st.session_state.loaded = False

    if load_btn or (not st.session_state.loaded) or auto_reload_files:
        try:
            memo_text = Path(memo_text_path).read_text(encoding="utf-8-sig")
            model_output = fix_mojibake_obj(flatten_model_output(read_json_or_jsonl(model_output_path)))
            fn_rows = load_fn_candidates(fn_input_path)
            effective_schema = read_json(effective_schema_path)
            memo_id, memo_id_notes = derive_decision_key(memo_text_path, model_output_path, fn_rows)
            expected_memo_id = base_memo_id_from_key(memo_id)
            fn_notes: list[str] = []
            fn_row_memo_ids = sorted({str(x.get("memo_id")) for x in fn_rows if isinstance(x, dict) and x.get("memo_id")})
            if fn_row_memo_ids:
                matched_rows = [x for x in fn_rows if str(x.get("memo_id")) == expected_memo_id]
                if len(matched_rows) != len(fn_rows):
                    fn_notes.append(
                        "FN review input memo_id가 현재 Decision key와 일부/전체 불일치하여 "
                        f"`{expected_memo_id}` rows만 표시합니다. (input memo_ids={fn_row_memo_ids})"
                    )
                fn_rows = matched_rows
            field_map = get_field_map(effective_schema)
            st.session_state.loaded = True
            st.session_state.memo_text = memo_text
            st.session_state.model_output = model_output
            st.session_state.fn_rows = fn_rows
            st.session_state.effective_schema = effective_schema
            st.session_state.memo_id = memo_id
            st.session_state.memo_id_notes = memo_id_notes
            st.session_state.fn_input_notes = fn_notes
            st.session_state.field_map = field_map
        except Exception as e:
            st.error(f"Load failed: {e}")
            st.stop()

    memo_text = st.session_state.memo_text
    model_output = st.session_state.model_output
    fn_rows = fix_mojibake_obj(st.session_state.fn_rows)
    field_map = st.session_state.field_map
    memo_id = st.session_state.memo_id
    memo_notes = st.session_state.get("memo_id_notes", [])
    if memo_notes:
        for note in memo_notes:
            st.warning(note)
    fn_input_notes = st.session_state.get("fn_input_notes", [])
    if fn_input_notes:
        for note in fn_input_notes:
            st.warning(note)
    st.caption(f"Decision key: `{memo_id}`")
    fallback_ids = []
    if "__BC" in memo_id:
        fallback_ids.append(memo_id.split("__BC", 1)[0])
    existing = load_existing_decisions(memo_id, decisions_dir, fallback_memo_ids=fallback_ids)

    bad_signals = 0
    for x in model_output:
        fd = x.get("field_definition") or {}
        txt = " ".join([str(fd.get("label", "")), str(x.get("reasoning", ""))])
        if "??" in txt:
            bad_signals += 1
    if bad_signals > 0:
        st.warning(
            f"Detected {bad_signals} suspicious mojibake signals in model_output text. "
            "UI-level repair is limited if source data is already broken."
        )

    st.subheader("Memo Text")
    st.text_area("memo", memo_text, height=260)

    st.subheader("Field TP/FP/FN Aggregate")
    agg = aggregate_counts(decisions_dir=decisions_dir, field_map=field_map)
    agg_display = [
        {
            "field_id": x.get("field_id", ""),
            "label": x.get("label", ""),
            "tp": x.get("tp", 0),
            "fp": x.get("fp", 0),
            "fn": x.get("fn", 0),
            "precision": round(
                (x.get("tp", 0) / (x.get("tp", 0) + x.get("fp", 0)))
                if (x.get("tp", 0) + x.get("fp", 0)) > 0
                else 0.0,
                4,
            ),
            "recall": round(
                (x.get("tp", 0) / (x.get("tp", 0) + x.get("fn", 0)))
                if (x.get("tp", 0) + x.get("fn", 0)) > 0
                else 0.0,
                4,
            ),
            "f1_score": round(
                (
                    (
                        2
                        * (
                            (x.get("tp", 0) / (x.get("tp", 0) + x.get("fp", 0)))
                            if (x.get("tp", 0) + x.get("fp", 0)) > 0
                            else 0.0
                        )
                        * (
                            (x.get("tp", 0) / (x.get("tp", 0) + x.get("fn", 0)))
                            if (x.get("tp", 0) + x.get("fn", 0)) > 0
                            else 0.0
                        )
                    )
                    / (
                        (
                            (x.get("tp", 0) / (x.get("tp", 0) + x.get("fp", 0)))
                            if (x.get("tp", 0) + x.get("fp", 0)) > 0
                            else 0.0
                        )
                        + (
                            (x.get("tp", 0) / (x.get("tp", 0) + x.get("fn", 0)))
                            if (x.get("tp", 0) + x.get("fn", 0)) > 0
                            else 0.0
                        )
                    )
                )
                if (
                    (
                        (x.get("tp", 0) / (x.get("tp", 0) + x.get("fp", 0)))
                        if (x.get("tp", 0) + x.get("fp", 0)) > 0
                        else 0.0
                    )
                    + (
                        (x.get("tp", 0) / (x.get("tp", 0) + x.get("fn", 0)))
                        if (x.get("tp", 0) + x.get("fn", 0)) > 0
                        else 0.0
                    )
                )
                > 0
                else 0.0,
                4,
            ),
        }
        for x in agg
    ]
    st.dataframe(agg_display, use_container_width=True, height=220)
    show_agg_chart = st.checkbox("Show aggregate bar chart", value=False)
    if show_agg_chart:
        min_support_n = int(st.number_input("Chart min support N (TP+FP+FN)", min_value=1, max_value=500, value=4, step=1))
        filtered_rows = [
            row
            for row in agg_display
            if (int(row.get("tp", 0)) + int(row.get("fp", 0)) + int(row.get("fn", 0))) >= min_support_n
        ]
        sorted_rows = sorted(
            filtered_rows,
            key=lambda x: x.get("f1_score", 0.0),
            reverse=True,
        )
        if not sorted_rows:
            st.info(f"No fields match support >= {min_support_n}. Lower the threshold or save more decisions.")
        else:
            chart_rows: list[dict[str, Any]] = []
            for row in sorted_rows:
                field_name = f"{row.get('field_id', '')} | {row.get('label', '')}"
                support = int(row.get("tp", 0)) + int(row.get("fp", 0)) + int(row.get("fn", 0))
                chart_rows.append(
                    {
                        "field_name": field_name,
                        "support": support,
                        "metric": "precision",
                        "value": float(row.get("precision", 0.0)),
                    }
                )
                chart_rows.append(
                    {
                        "field_name": field_name,
                        "support": support,
                        "metric": "recall",
                        "value": float(row.get("recall", 0.0)),
                    }
                )
                chart_rows.append(
                    {
                        "field_name": field_name,
                        "support": support,
                        "metric": "f1",
                        "value": float(row.get("f1_score", 0.0)),
                    }
                )

            max_value = max((r["value"] for r in chart_rows), default=0.0)
            if max_value <= 0:
                st.warning("All precision/recall/f1 values are 0. Bars may look empty until TP/FP/FN decisions accumulate.")
            chart = (
                alt.Chart(alt.Data(values=chart_rows))
                .mark_bar()
                .encode(
                    x=alt.X(
                        "value:Q",
                        title="Score",
                        scale=alt.Scale(domain=[0, 1]),
                        axis=alt.Axis(format=".2f", tickCount=6),
                    ),
                    y=alt.Y("field_name:N", sort="-x", title="Field"),
                    yOffset=alt.YOffset("metric:N"),
                    color=alt.Color(
                        "metric:N",
                        scale=alt.Scale(
                            domain=["precision", "recall", "f1"],
                            range=["#2E8B57", "#4C78A8", "#F28E2B"],
                        ),
                    ),
                    tooltip=[
                        alt.Tooltip("field_name:N", title="Field"),
                        alt.Tooltip("support:Q", title="Support"),
                        alt.Tooltip("metric:N", title="Metric"),
                        alt.Tooltip("value:Q", title="Score", format=".4f"),
                    ],
                )
                .properties(height=max(220, 22 * max(1, len(sorted_rows))))
            )
            st.altair_chart(chart, use_container_width=True)

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Model Output Review (TP/FP)")
        prev_model_by_idx = {(x.get("item_idx")): x for x in existing.get("model_decisions", [])}
        prev_model_by_field_id = {
            str(x.get("field_id")): x
            for x in existing.get("model_decisions", [])
            if x.get("field_id") is not None
        }
        model_decisions: list[dict[str, Any]] = []

        for i, item in enumerate(model_output):
            fd = fix_mojibake_obj(item.get("field_definition") or {})
            field_id = str(fd.get("id")) if fd.get("id") is not None else None
            field_label = fix_mojibake_text(str(fd.get("label") or ""))
            prev = (
                prev_model_by_field_id.get(str(field_id))
                if field_id is not None
                else prev_model_by_idx.get(i, {})
            )
            if not prev:
                prev = prev_model_by_idx.get(i, {})
            decision_key = memo_widget_key(memo_id, f"model_decision_{field_id if field_id is not None else i}_{i}")
            note_key = memo_widget_key(memo_id, f"model_note_{field_id if field_id is not None else i}_{i}")
            decision_preview = current_choice(decision_key, prev.get("decision", "SKIP"), ["SKIP", "TP", "FP"])
            with st.expander(f"[{i}][{decision_preview}] {field_id} | {field_label}", expanded=False):
                st.write("type:", fd.get("type"), "| category:", fd.get("category"))
                st.write("extracted_value:", format_extracted_value(item, field_map))
                st.write("reasoning:", fix_mojibake_text(str(item.get("reasoning") or "")))
                decision = st.selectbox(
                    "Decision",
                    ["SKIP", "TP", "FP"],
                    index=["SKIP", "TP", "FP"].index(prev.get("decision", "SKIP")),
                    key=decision_key,
                )
                note = st.text_input(
                    "Note",
                    value=prev.get("note", ""),
                    key=note_key,
                )
                model_decisions.append(
                    {
                        "item_idx": i,
                        "field_id": field_id,
                        "field_label": field_label,
                        "decision": decision,
                        "note": note,
                    }
                )

    with col2:
        st.subheader("FN Candidate Review (FN/NOT_FN)")
        prev_fn_by_cid = {str(x.get("candidate_id")): x for x in existing.get("fn_decisions", []) if x.get("candidate_id")}
        prev_fn_by_sig: dict[str, dict[str, Any]] = {}
        for x in existing.get("fn_decisions", []):
            sig = fn_decision_signature(x)
            if sig and sig not in prev_fn_by_sig:
                prev_fn_by_sig[sig] = x
        fn_decisions: list[dict[str, Any]] = []

        all_field_ids = sorted(field_map.keys(), key=lambda x: (len(x), x))
        for i, row in enumerate(fn_rows):
            cid = row.get("candidate_id")
            row_sig = fn_row_signature(row)
            prev = prev_fn_by_cid.get(str(cid), {}) if cid is not None else {}
            if not prev:
                prev = prev_fn_by_sig.get(row_sig, {})
            fn_decision_key = memo_widget_key(memo_id, f"fn_decision_{cid}")
            fn_default_decision = prev.get("decision", "NOT_FN")
            fn_decision_preview = current_choice(
                fn_decision_key, fn_default_decision, ["SKIP", "FN", "NOT_FN"]
            )
            with st.expander(
                f"[{i}][{fn_decision_preview}] {cid} | {row.get('semantic_type')} | {row.get('raw_text')}",
                expanded=False,
            ):
                ev = row.get("evidence") or {}
                st.write("evidence:", fix_mojibake_text(str(ev.get("exact_quote") or "")))
                st.write("section:", ev.get("section_path"))
                st.write("offset:", ev.get("start_char"), "~", ev.get("end_char"))
                line_no = char_to_line_no(memo_text, ev.get("start_char"))
                line_text = get_line_text(memo_text, line_no)
                st.write("line:", line_no if line_no is not None else "-")
                if line_text:
                    st.code(line_text, language="text")
                st.write("suggested_fields:", row.get("suggested_fields"))

                decision = st.selectbox(
                    "Decision",
                    ["SKIP", "FN", "NOT_FN"],
                    index=["SKIP", "FN", "NOT_FN"].index(fn_default_decision),
                    key=fn_decision_key,
                )

                suggested = [x.get("field_id") for x in (row.get("suggested_fields") or []) if x.get("field_id")]
                default_field = str(prev.get("assigned_field_id")) if prev.get("assigned_field_id") else ""
                field_options = [""] + list(dict.fromkeys(suggested + all_field_ids))
                if default_field not in field_options and default_field:
                    field_options.append(default_field)
                assigned_field_id = st.selectbox(
                    "Assign field_id",
                    field_options,
                    index=field_options.index(default_field) if default_field in field_options else 0,
                    format_func=lambda x: field_option_label(x, field_map),
                    key=memo_widget_key(memo_id, f"fn_field_{cid}"),
                )
                note = st.text_input(
                    "Note",
                    value=prev.get("note", ""),
                    key=memo_widget_key(memo_id, f"fn_note_{cid}"),
                )
                assigned_field_label = None
                if assigned_field_id:
                    assigned_field_label = fix_mojibake_text(
                        str((field_map.get(str(assigned_field_id)) or {}).get("label") or "")
                    )
                fn_decisions.append(
                    {
                        "candidate_id": cid,
                        "semantic_type": row.get("semantic_type"),
                        "value_type": row.get("value_type"),
                        "raw_text": row.get("raw_text"),
                        "normalized": row.get("normalized"),
                        "evidence_segment_id": ev.get("segment_id"),
                        "evidence_section_path": ev.get("section_path"),
                        "evidence_quote": ev.get("exact_quote"),
                        "start_char": ev.get("start_char"),
                        "end_char": ev.get("end_char"),
                        "line_no": line_no,
                        "line_text": line_text,
                        "suggested_fields_snapshot": row.get("suggested_fields"),
                        "decision": decision,
                        "assigned_field_id": assigned_field_id or None,
                        "assigned_field_label": assigned_field_label,
                        "note": note,
                    }
                )

    model_counts = {"TP": 0, "FP": 0, "SKIP": 0}
    for row in model_decisions:
        d = row.get("decision", "SKIP")
        if d in model_counts:
            model_counts[d] += 1
    fn_counts = {"FN": 0, "NOT_FN": 0, "SKIP": 0}
    for row in fn_decisions:
        d = row.get("decision", "SKIP")
        if d in fn_counts:
            fn_counts[d] += 1
    st.markdown(
        " | ".join(
            [
                f"Model TP `{model_counts['TP']}`",
                f"Model FP `{model_counts['FP']}`",
                f"Model SKIP `{model_counts['SKIP']}`",
                f"FN `{fn_counts['FN']}`",
                f"NOT_FN `{fn_counts['NOT_FN']}`",
                f"FN SKIP `{fn_counts['SKIP']}`",
            ]
        )
    )

    if st.button("Save Decisions", type="primary"):
        payload = {
            "memo_id": memo_id,
            "updated_at": utc_now_iso(),
            "model_decisions": model_decisions,
            "fn_decisions": fn_decisions,
        }
        save_decisions(payload, decisions_dir)
        st.success(f"Saved: {decision_file(memo_id, decisions_dir)}")
        st.rerun()


if __name__ == "__main__":
    app()
