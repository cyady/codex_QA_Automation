from __future__ import annotations

from typing import Any

from .browser import current_url, visible_page_excerpt, visible_text_exists, wait_until


def is_import_page_ready(session: "vibium.browser_sync.VibeSync") -> bool:
    return visible_text_exists(session, "딜을 업로드할 때에는 '제목, 단계' 열을 반드시 추가해주세요.")


def inspect_import_page(session: "vibium.browser_sync.VibeSync", import_url: str) -> dict[str, Any]:
    session.go(import_url)
    ready = wait_until(lambda: is_import_page_ready(session), timeout_sec=20.0, interval_sec=0.3)
    if not ready:
        raise RuntimeError(f"import page not ready: excerpt={visible_page_excerpt(session)}")
    return {
        "ok": True,
        "url": current_url(session),
        "excerpt": visible_page_excerpt(session),
        "required_headers_hint": "제목, 단계",
    }
