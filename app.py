import streamlit as st
from Agent.graph import Agent
import uuid
import re

# ──────────────────────────────────────────────────
#  Page config
# ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Scout — College Assistant",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────
#  Custom CSS
# ──────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Import Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* { font-family: 'Inter', sans-serif; }

/* ── Animated gradient background orbs ── */
.stApp::before {
    content: '';
    position: fixed;
    top: -120px;
    left: -120px;
    width: 450px;
    height: 450px;
    background: radial-gradient(circle, rgba(59,130,246,0.12) 0%, transparent 70%);
    border-radius: 50%;
    animation: float1 18s ease-in-out infinite;
    z-index: 0;
    pointer-events: none;
}
.stApp::after {
    content: '';
    position: fixed;
    bottom: -100px;
    right: -100px;
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, rgba(139,92,246,0.10) 0%, transparent 70%);
    border-radius: 50%;
    animation: float2 22s ease-in-out infinite;
    z-index: 0;
    pointer-events: none;
}

@keyframes float1 {
    0%, 100% { transform: translate(0, 0) scale(1); }
    33% { transform: translate(60px, 80px) scale(1.1); }
    66% { transform: translate(-40px, 40px) scale(0.95); }
}
@keyframes float2 {
    0%, 100% { transform: translate(0, 0) scale(1); }
    33% { transform: translate(-70px, -50px) scale(1.05); }
    66% { transform: translate(50px, -80px) scale(0.9); }
}

/* ── Hide default Streamlit branding ── */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }

/* ── Chat message styling ── */
.stChatMessage {
    border-radius: 16px !important;
    padding: 12px 16px !important;
    margin-bottom: 8px !important;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.04) !important;
    animation: fadeSlideIn 0.35s ease-out;
}

@keyframes fadeSlideIn {
    from { opacity: 0; transform: translateY(12px); }
    to { opacity: 1; transform: translateY(0); }
}

/* User messages */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background: linear-gradient(135deg, rgba(59,130,246,0.10), rgba(59,130,246,0.04)) !important;
    border-left: 3px solid #3b82f6 !important;
}

/* Assistant messages */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    background: linear-gradient(135deg, rgba(139,92,246,0.08), rgba(139,92,246,0.02)) !important;
    border-left: 3px solid #8b5cf6 !important;
}

/* ── Chat input ── */
.stChatInput > div {
    border-radius: 16px !important;
    border: 1px solid rgba(59,130,246,0.25) !important;
    background: rgba(17,24,39,0.8) !important;
    backdrop-filter: blur(8px);
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
}
.stChatInput > div:focus-within {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 2px rgba(59,130,246,0.15) !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1321 0%, #111827 100%) !important;
    border-right: 1px solid rgba(59,130,246,0.08);
}

section[data-testid="stSidebar"] .stMarkdown h1,
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3 {
    background: linear-gradient(135deg, #3b82f6, #8b5cf6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* ── Quick-question pills ── */
.quick-q {
    display: inline-block;
    padding: 8px 16px;
    margin: 4px;
    border-radius: 24px;
    font-size: 13px;
    font-weight: 500;
    color: #c4b5fd;
    background: rgba(139,92,246,0.10);
    border: 1px solid rgba(139,92,246,0.20);
    cursor: pointer;
    transition: all 0.25s ease;
}
.quick-q:hover {
    background: rgba(139,92,246,0.22);
    border-color: rgba(139,92,246,0.45);
    transform: translateY(-1px);
}

/* ── Status badge ── */
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
}
.status-online {
    background: rgba(34,197,94,0.12);
    color: #4ade80;
    border: 1px solid rgba(34,197,94,0.25);
}

/* ── Divider ── */
.glow-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(59,130,246,0.3), transparent);
    border: none;
    margin: 16px 0;
}

/* ── Welcome card ── */
.welcome-card {
    background: linear-gradient(135deg, rgba(59,130,246,0.08), rgba(139,92,246,0.06));
    border: 1px solid rgba(59,130,246,0.12);
    border-radius: 20px;
    padding: 32px 28px;
    text-align: center;
    margin-bottom: 24px;
    backdrop-filter: blur(10px);
}
.welcome-card h2 {
    margin: 0 0 8px 0;
    font-size: 28px;
    background: linear-gradient(135deg, #60a5fa, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.welcome-card p {
    color: #94a3b8;
    font-size: 15px;
    margin: 0;
}

/* ── Tool activity expander ── */
.tool-activity {
    background: rgba(59,130,246,0.05);
    border: 1px solid rgba(59,130,246,0.12);
    border-radius: 12px;
    padding: 10px 14px;
    margin: 8px 0;
    font-size: 13px;
    color: #94a3b8;
}
.tool-name {
    color: #60a5fa;
    font-weight: 600;
    font-family: 'JetBrains Mono', monospace;
}

/* ── Option pill buttons ── */
div[data-testid="stHorizontalBlock"] .option-pill-container button {
    border-radius: 24px !important;
}

div.option-pills-wrapper {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 12px;
    margin-bottom: 4px;
}
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────
#  Helpers: parse [OPTIONS] blocks
# ──────────────────────────────────────────────────
OPTIONS_PATTERN = re.compile(r"\[OPTIONS\]\s*\n(.*?)\n\s*\[/OPTIONS\]", re.DOTALL)


def parse_options(text: str):
    """
    Extract option lists from [OPTIONS]...[/OPTIONS] blocks in agent output.
    Returns (clean_text, list_of_options) where clean_text has the blocks removed.
    """
    match = OPTIONS_PATTERN.search(text)
    if not match:
        return text, []

    options_raw = match.group(1).strip()
    options = [opt.strip("- •").strip() for opt in options_raw.splitlines() if opt.strip()]

    # Remove the [OPTIONS] block from the display text
    clean_text = text[: match.start()].rstrip()
    trailing = text[match.end() :].strip()
    if trailing:
        clean_text += "\n\n" + trailing

    return clean_text, options


# ──────────────────────────────────────────────────
#  Session state initialisation
# ──────────────────────────────────────────────────
if "agent" not in st.session_state:
    st.session_state.agent = Agent(name="Scout")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

# ──────────────────────────────────────────────────
#  Sidebar
# ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎓 Scout")
    st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)

    st.markdown(
        '<span class="status-badge status-online">● Online</span>',
        unsafe_allow_html=True,
    )

    st.markdown("""
    Your AI assistant for **Thapar Institute of Engineering & Technology**.

    Ask me about:
    - 📋 **Admissions** — UG, PG, PhD, Diploma
    - 💰 **Fees** — tuition, semester, hostel charges
    - 🏠 **Hostel** — rooms, mess, rules
    - 🎓 **Scholarships** — merit, financial aid
    - 🌍 **International Programs** — exchanges, tie-ups
    - 🏫 **College Info** — departments, campus, history
    """)

    st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)

    st.markdown("#### 💡 Try asking")
    quick_questions = [
        "What is the B.Tech fee structure?",
        "How do I apply for admission?",
        "What scholarships are available?",
        "Tell me about international exchange programs",
        "What are the hostel charges?",
    ]
    for q in quick_questions:
        if st.button(q, key=f"qq_{q}", use_container_width=True):
            st.session_state.pending_question = q

    st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)

    if st.button("🔄 New Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.thread_id = str(uuid.uuid4())
        st.rerun()

    st.markdown(
        '<div style="position:fixed; bottom:16px; font-size:11px; color:#475569;">'
        'Powered by PageIndex & LangGraph'
        '</div>',
        unsafe_allow_html=True,
    )

# ──────────────────────────────────────────────────
#  Welcome card (shown when no messages)
# ──────────────────────────────────────────────────
if not st.session_state.messages:
    st.markdown("""
    <div class="welcome-card">
        <h2>👋 Welcome to Scout</h2>
        <p>Your intelligent assistant for all TIET queries.<br>
        Type a question below or pick one from the sidebar to get started.</p>
    </div>
    """, unsafe_allow_html=True)

# ──────────────────────────────────────────────────
#  Render chat history
# ──────────────────────────────────────────────────
for idx, msg in enumerate(st.session_state.messages):
    avatar = "🎓" if msg["role"] == "assistant" else "👤"
    with st.chat_message(msg["role"], avatar=avatar):
        # Show tool activity if present
        if msg.get("tool_calls"):
            with st.expander("🔧 Tool activity", expanded=False):
                for tc in msg["tool_calls"]:
                    st.markdown(
                        f'<div class="tool-activity">'
                        f'Called <span class="tool-name">{tc["name"]}</span>'
                        f'(<code>{tc["args"]}</code>)'
                        f'</div>',
                        unsafe_allow_html=True,
                    )
        # Display message text (without [OPTIONS] block)
        display_text = msg.get("display_text", msg["content"])
        if display_text:
            st.markdown(display_text)

        # Render option buttons if this is the LAST assistant message with options
        options = msg.get("options", [])
        is_last_assistant = (
            msg["role"] == "assistant"
            and idx == len(st.session_state.messages) - 1
        )
        if options and is_last_assistant:
            cols = st.columns(min(len(options), 3))
            for i, opt in enumerate(options):
                col = cols[i % min(len(options), 3)]
                if col.button(
                    f"👉 {opt}",
                    key=f"opt_{idx}_{i}",
                    use_container_width=True,
                ):
                    st.session_state.pending_question = opt

# ──────────────────────────────────────────────────
#  Handle input (typed or sidebar quick-question)
# ──────────────────────────────────────────────────
user_input = st.chat_input("Ask me anything about TIET...")

# Check if a sidebar button or option pill was pressed
if "pending_question" in st.session_state:
    user_input = st.session_state.pending_question
    del st.session_state.pending_question

if user_input:
    # Display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)

    # Get agent response
    with st.chat_message("assistant", avatar="🎓"):
        with st.spinner("Thinking..."):
            result = st.session_state.agent.invoke(
                user_input,
                config={"configurable": {"thread_id": st.session_state.thread_id}},
            )

            # Extract tool calls and final response
            tool_calls_log = []
            final_content = ""

            for msg in result["messages"]:
                if msg.type == "ai":
                    if hasattr(msg, "tool_calls") and msg.tool_calls:
                        for tc in msg.tool_calls:
                            tool_calls_log.append({
                                "name": tc["name"],
                                "args": tc["args"].get("query", str(tc["args"])),
                            })
                    if msg.content:
                        final_content = msg.content

            # Show tool activity
            if tool_calls_log:
                with st.expander("🔧 Tool activity", expanded=False):
                    for tc in tool_calls_log:
                        st.markdown(
                            f'<div class="tool-activity">'
                            f'Called <span class="tool-name">{tc["name"]}</span>'
                            f'(<code>{tc["args"]}</code>)'
                            f'</div>',
                            unsafe_allow_html=True,
                        )

            # Parse options from agent response
            display_text, options = parse_options(final_content)

            # Show the text part
            st.markdown(display_text)

            # Show option pills as buttons
            if options:
                cols = st.columns(min(len(options), 3))
                for i, opt in enumerate(options):
                    col = cols[i % min(len(options), 3)]
                    if col.button(
                        f"👉 {opt}",
                        key=f"new_opt_{i}",
                        use_container_width=True,
                    ):
                        st.session_state.pending_question = opt

    # Save to history (store both raw content and parsed display)
    st.session_state.messages.append({
        "role": "assistant",
        "content": final_content,
        "display_text": display_text,
        "options": options,
        "tool_calls": tool_calls_log,
    })
