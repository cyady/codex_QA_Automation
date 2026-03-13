from __future__ import annotations

import json
import socket
from pathlib import Path
from urllib.parse import urlencode

import streamlit as st
import streamlit.components.v1 as components

APP_ROOT = Path(__file__).resolve().parent
TEMPLATE_PATH = APP_ROOT / "src" / "recatch_bulk_import_withui" / "templates" / "journey_test.html"
CSS_PATH = APP_ROOT / "src" / "recatch_bulk_import_withui" / "static" / "journey_test.css"
JS_PATH = APP_ROOT / "src" / "recatch_bulk_import_withui" / "static" / "journey_test.js"

WORKFLOW_BASE_URL = "https://test.recatch.cc/workflows/klsfjjtnhz"
DEFAULT_UTM = {
    "utm_source": "local1",
    "utm_medium": "local2",
    "utm_campaign": "local3",
    "utm_content": "local4",
    "utm_term": "local5",
}
STREAMLIT_PORT = 8501


def best_effort_lan_ip() -> str:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(("8.8.8.8", 80))
        return sock.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        sock.close()


def current_utm_params() -> dict[str, str]:
    params = DEFAULT_UTM.copy()
    for key, value in st.query_params.to_dict().items():
        if key in params and isinstance(value, str) and value.strip():
            params[key] = value.strip()
    return params


def workflow_url(utm_params: dict[str, str]) -> str:
    return f"{WORKFLOW_BASE_URL}?{urlencode(utm_params)}"


def streamlit_share_path(utm_params: dict[str, str]) -> str:
    return f"/?{urlencode(utm_params)}"


def load_streamlit_html(utm_params: dict[str, str]) -> str:
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    css = CSS_PATH.read_text(encoding="utf-8")
    js = JS_PATH.read_text(encoding="utf-8")

    iframe_src = workflow_url(utm_params)
    virtual_path = f"/journey-test?{urlencode(utm_params)}"
    utm_note = (
        "테스트 UTM: "
        + ", ".join(f"{key}={value}" for key, value in utm_params.items())
    )
    history_patch = f"""
    <script>
      (function () {{
        try {{
          history.replaceState({{}}, "", {json.dumps(virtual_path)});
        }} catch (error) {{
          console.warn("Failed to apply virtual path", error);
        }}
      }})();
    </script>
    """

    template = template.replace(
        "<link rel=\"stylesheet\" href=\"{{ url_for('static', filename='journey_test.css') }}\">",
        f"{history_patch}\n    <style>\n{css}\n    </style>",
    )
    template = template.replace(
        "<script src=\"{{ url_for('static', filename='journey_test.js') }}\"></script>",
        f"<script>\n{js}\n</script>",
    )
    template = template.replace(
        "https://test.recatch.cc/workflows/klsfjjtnhz?utm_source=local1&utm_medium=local2&utm_campaign=local3&utm_content=local4&utm_term=local5",
        iframe_src,
    )
    template = template.replace(
        "테스트 UTM: `utm_source=local1`, `utm_medium=local2`, `utm_campaign=local3`,\n            `utm_content=local4`, `utm_term=local5`",
        utm_note,
    )
    return template


def app() -> None:
    st.set_page_config(page_title="Re:catch Journey Test Share", layout="wide")
    st.markdown(
        """
        <style>
          [data-testid="stHeader"],
          [data-testid="stToolbar"],
          [data-testid="stDecoration"],
          #MainMenu,
          footer {
            visibility: hidden;
            height: 0;
          }
          .block-container {
            padding-top: 1.2rem;
            padding-bottom: 1.5rem;
            max-width: 100%;
          }
          .stCodeBlock pre {
            white-space: pre-wrap;
          }
        </style>
        """,
        unsafe_allow_html=True,
    )

    utm_params = current_utm_params()
    share_path = streamlit_share_path(utm_params)
    lan_ip = best_effort_lan_ip()
    share_url = f"http://{lan_ip}:{STREAMLIT_PORT}{share_path}"

    st.title("Re:catch Journey Test")
    st.caption("공유용 Streamlit 래퍼입니다. URL의 UTM 값을 읽어 iframe 임베드에도 그대로 전달합니다.")

    left, right = st.columns([3, 2])
    with left:
        st.code(share_url, language="text")
    with right:
        st.write("현재 UTM")
        st.json(utm_params, expanded=False)

    st.info(
        "같은 네트워크 사용자는 위 URL로 접속할 수 있습니다. 외부 인터넷 공유가 필요하면 별도 터널이 필요합니다."
    )

    components.html(load_streamlit_html(utm_params), height=2300, scrolling=True)


if __name__ == "__main__":
    app()
