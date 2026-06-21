"""Streamlit chat UI — run from project root: streamlit run apps/chat_app.py"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

_root = Path(__file__).parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from utils.config import MODELS, get_client, estimate_cost
from utils.helpers import mock_chat_response

MOCK   = os.getenv("MOCK", "0") == "1"
SYSTEM = "You are a helpful assistant for Indian professionals."

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="OpenAI Chat", page_icon="💬", layout="wide")

# ── Terminal CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Base font & background */
html, body, [class*="css"] {
    font-family: 'Courier New', Courier, monospace !important;
}

/* Remove default Streamlit header padding */
.block-container { padding-top: 1.5rem; }

/* Chat message bubbles */
[data-testid="stChatMessage"] {
    background: #111111;
    border: 1px solid #00ff41;
    border-radius: 4px;
    margin-bottom: 0.6rem;
    padding: 0.6rem 1rem;
}

/* User bubble — dimmer green tint */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    border-color: #005c18;
    background: #0a1a0d;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0a0a0a;
    border-right: 1px solid #005c18;
}

/* Input box */
[data-testid="stChatInput"] textarea {
    background: #0a0a0a !important;
    color: #00ff41 !important;
    border: 1px solid #00ff41 !important;
    font-family: 'Courier New', monospace !important;
    caret-color: #00ff41;
}

/* Buttons */
.stButton > button {
    background: #0a0a0a;
    color: #00ff41;
    border: 1px solid #00ff41;
    border-radius: 2px;
    font-family: 'Courier New', monospace;
}
.stButton > button:hover {
    background: #00ff41;
    color: #0a0a0a;
}

/* Selectbox & text area */
.stSelectbox div[data-baseweb="select"] > div,
.stTextArea textarea {
    background: #111111 !important;
    color: #00ff41 !important;
    border-color: #005c18 !important;
    font-family: 'Courier New', monospace !important;
}

/* Metric value */
[data-testid="stMetricValue"] { color: #00ff41 !important; }

/* Blinking cursor appended to last assistant message */
@keyframes blink {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0; }
}
.terminal-cursor::after {
    content: "█";
    animation: blink 1s step-start infinite;
    color: #00ff41;
    margin-left: 2px;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0a0a0a; }
::-webkit-scrollbar-thumb { background: #005c18; border-radius: 2px; }
</style>
""", unsafe_allow_html=True)

# ── Client ────────────────────────────────────────────────────────────────────
try:
    client = get_client()
except ValueError as e:
    st.error(str(e))
    st.stop()

# ── Session state init ────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM}]
if "total_cost" not in st.session_state:
    st.session_state.total_cost = 0.0
if "model" not in st.session_state:
    st.session_state.model = MODELS["chat"]

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")

    # Model picker — only text models
    model_labels = {
        f"{k} ({v})": v
        for k, v in MODELS.items()
        if k in ("chat", "frontier", "nano")
    }
    selected_label = st.selectbox(
        "Model",
        options=list(model_labels.keys()),
        index=0,
        help="gpt-5.4-mini is cheap & fast; use gpt-5.5 (frontier) sparingly.",
    )
    st.session_state.model = model_labels[selected_label]

    st.divider()

    # Editable system prompt
    new_system = st.text_area(
        "System prompt",
        value=st.session_state.messages[0]["content"],
        height=110,
    )
    if st.button("Apply", use_container_width=True):
        st.session_state.messages[0]["content"] = new_system
        st.toast("System prompt updated.")

    st.divider()

    # Cost & token counters
    st.metric("Session cost (USD)", f"${st.session_state.total_cost:.5f}")
    msg_count = len(st.session_state.messages) - 1  # exclude system msg
    st.caption(f"{msg_count} message(s) | model: `{st.session_state.model}` | MOCK={MOCK}")

    st.divider()

    if st.button("🗑️  New chat", use_container_width=True):
        st.session_state.messages   = [{"role": "system", "content": new_system}]
        st.session_state.total_cost = 0.0
        st.rerun()

# ── ASCII header ─────────────────────────────────────────────────────────────
st.markdown("""
<pre style="color:#00ff41;font-size:0.72rem;line-height:1.3;margin-bottom:0;">
 ██████╗ ██████╗ ███████╗███╗   ██╗ █████╗ ██╗      ██████╗██╗  ██╗ █████╗ ████████╗
██╔═══██╗██╔══██╗██╔════╝████╗  ██║██╔══██╗██║     ██╔════╝██║  ██║██╔══██╗╚══██╔══╝
██║   ██║██████╔╝█████╗  ██╔██╗ ██║███████║██║     ██║     ███████║███████║   ██║
██║   ██║██╔═══╝ ██╔══╝  ██║╚██╗██║██╔══██║██║     ██║     ██╔══██║██╔══██║   ██║
╚██████╔╝██║     ███████╗██║ ╚████║██║  ██║███████╗╚██████╗██║  ██║██║  ██║   ██║
 ╚═════╝ ╚═╝     ╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   v2.0
</pre>
<p style="color:#005c18;font-size:0.78rem;margin-top:0.2rem;">
  [ SESSION 2 ]  Multi-turn Chat Completions API  |  type your query below ▼
</p>
""", unsafe_allow_html=True)

# ── Replay history (index 0 is the system message — skip it) ─────────────────
visible = st.session_state.messages[1:]
for i, msg in enumerate(visible):
    with st.chat_message(msg["role"]):
        is_last_assistant = (
            msg["role"] == "assistant" and i == len(visible) - 1
        )
        if is_last_assistant:
            st.markdown(
                f'<span class="terminal-cursor">{msg["content"]}</span>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(msg["content"])

# ── Chat input ────────────────────────────────────────────────────────────────
prompt = st.chat_input("Ask me anything…")

if prompt:
    # 1. Show and store the user turn
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Stream the assistant reply
    with st.chat_message("assistant"):
        if MOCK:
            mock_resp   = mock_chat_response(prompt)
            reply       = mock_resp.choices[0].message.content
            usage       = mock_resp.usage
            st.markdown(reply)
        else:
            try:
                stream = client.chat.completions.create(
                    model=st.session_state.model,
                    messages=st.session_state.messages,
                    stream=True,
                    stream_options={"include_usage": True},  # get token counts at end
                )

                _state = {"usage": None}

                def _token_stream():
                    """Yield content chunks; capture usage from the final chunk."""
                    for chunk in stream:
                        if chunk.usage:
                            _state["usage"] = chunk.usage
                        if chunk.choices and chunk.choices[0].delta.content:
                            yield chunk.choices[0].delta.content

                reply  = st.write_stream(_token_stream())
                usage  = _state["usage"]

            except Exception as exc:
                st.error(f"API error: {exc}")
                st.stop()

    # 3. Persist assistant turn and update cost
    st.session_state.messages.append({"role": "assistant", "content": reply})
    if usage:
        st.session_state.total_cost += estimate_cost(usage, st.session_state.model)

    # 4. Rerun so the sidebar cost metric refreshes
    st.rerun()
