import streamlit as st
import streamlit.components.v1 as components
from Agent.graph import Agent
import uuid
import re

# ──────────────────────────────────────────────────
#  Page config
# ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Scout — College Assistant",
    page_icon="🎓",
    layout="wide",
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
.stApp {
    background: linear-gradient(180deg, #ffffff 0%, #fffafa 100%);
}
.stApp::before {
    content: '';
    position: fixed;
    top: -140px;
    left: -140px;
    width: 520px;
    height: 520px;
    background: radial-gradient(circle, rgba(239,68,68,0.14) 0%, transparent 68%);
    border-radius: 50%;
    animation: float1 18s ease-in-out infinite;
    z-index: 0;
    pointer-events: none;
}
.stApp::after {
    content: '';
    position: fixed;
    bottom: -120px;
    right: -120px;
    width: 620px;
    height: 620px;
    background: radial-gradient(circle, rgba(239,68,68,0.10) 0%, transparent 70%);
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
    background: rgba(254,226,226,0.95) !important;
    border-left: 3px solid #7f1d1d !important;
    color: #1f1f1f !important;
}

/* Assistant messages */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    background: rgba(255,247,237,0.95) !important;
    border-left: 3px solid #991b1b !important;
    color: #1f1f1f !important;
}

/* ── Chat input ── */
.stChatInput > div {
    border-radius: 16px !important;
    border: 1px solid rgba(112,24,24,0.35) !important;
    background: rgba(112,24,24,0.95) !important;
    color: #f8fafc !important;
    backdrop-filter: blur(8px);
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
}
.stChatInput > div:focus-within {
    border-color: #7f1d1d !important;
    box-shadow: 0 0 0 2px rgba(112,24,24,0.18) !important;
}

/* ── Markdown text on white pages ── */
.stMarkdown,
.stMarkdown h1,
.stMarkdown h2,
.stMarkdown h3,
.stMarkdown h4,
.stMarkdown h5,
.stMarkdown p,
.stMarkdown li,
.stMarkdown span {
    color: #1f1f1f !important;
}

/* ── Sidebar (Compact Production-Ready) ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(135deg, #7f1d1d 0%, #991b1b 60%, #b91c1c 100%) !important;
    border-right: 1px solid rgba(112,24,24,0.5);
    width: 280px !important;
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
}

/* Sidebar title styling */
section[data-testid="stSidebar"] .stMarkdown h2 {
    color: #ffffff !important;
    font-size: 18px !important;
    font-weight: 700 !important;
    margin: 0 0 8px 0 !important;
    letter-spacing: 0.3px;
}

/* Sidebar headings */
section[data-testid="stSidebar"] .stMarkdown h4 {
    color: #ffffff !important;
    font-size: 12px !important;
    font-weight: 700 !important;
    margin: 12px 0 8px 0 !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    opacity: 0.95;
}

/* Sidebar body text */
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] .stMarkdown li {
    color: #fecaca !important;
    font-size: 12px !important;
    line-height: 1.5 !important;
    margin: 4px 0 !important;
}

/* Sidebar bold text */
section[data-testid="stSidebar"] .stMarkdown strong,
section[data-testid="stSidebar"] .stMarkdown b {
    color: #fca5a5 !important;
    font-weight: 600;
}

/* Sidebar list items compacting */
section[data-testid="stSidebar"] .stMarkdown li {
    margin-left: 16px;
    margin-bottom: 2px;
}

/* Sidebar buttons - compact style */
section[data-testid="stSidebar"] button {
    font-size: 12px !important;
    padding: 8px 12px !important;
    margin: 4px 0 !important;
    border-radius: 12px !important;
    font-weight: 500 !important;
    transition: all 0.2s ease;
}

section[data-testid="stSidebar"] button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

/* Sidebar container spacing optimization */
section[data-testid="stSidebar"] > div:first-child {
    padding: 20px 16px !important;
}

/* Reduce all margins in sidebar */
section[data-testid="stSidebar"] .stMarkdown {
    margin: 0 !important;
}

/* Responsive: Tablet and below */
@media (max-width: 1024px) {
    section[data-testid="stSidebar"] {
        width: 240px !important;
    }
    
    section[data-testid="stSidebar"] .stMarkdown h2 {
        font-size: 16px !important;
    }
    
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown li,
    section[data-testid="stSidebar"] button {
        font-size: 11px !important;
    }
}

/* Main content area optimization */
.stMainBlockContainer {
    max-width: 900px;
    margin: 0 auto;
}

/* Responsive: Tablet and below */
@media (max-width: 640px) {
    section[data-testid="stSidebar"] {
        width: 220px !important;
        padding: 12px 8px !important;
    }
    
    section[data-testid="stSidebar"] > div:first-child {
        padding: 12px 8px !important;
    }
    
    section[data-testid="stSidebar"] .stMarkdown h2 {
        font-size: 14px !important;
    }
    
    section[data-testid="stSidebar"] .stMarkdown h4 {
        font-size: 11px !important;
        margin-top: 8px !important;
    }
    
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown li {
        font-size: 10px !important;
        line-height: 1.4 !important;
    }
    
    section[data-testid="stSidebar"] button {
        font-size: 10px !important;
        padding: 6px 10px !important;
        margin: 3px 0 !important;
    }
    
    .stMainBlockContainer {
        max-width: 100%;
    }
}

/* ── Quick-question pills (Compact Production) ── */
.quick-q {
    display: inline-block;
    padding: 6px 12px;
    margin: 3px;
    border-radius: 18px;
    font-size: 11px;
    font-weight: 500;
    color: #7f1d1d;
    background: rgba(254,226,226,0.85);
    border: 1px solid rgba(112,24,24,0.2);
    cursor: pointer;
    transition: all 0.2s ease;
    backdrop-filter: blur(4px);
}
.quick-q:hover {
    background: rgba(254,226,226,0.95);
    border-color: rgba(112,24,24,0.4);
    transform: translateY(-1px);
    box-shadow: 0 3px 8px rgba(0,0,0,0.1);
}

/* ── Status badge (Compact Production) ── */
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 5px 10px;
    border-radius: 18px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.3px;
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
}
.status-online {
    background: rgba(254,226,226,0.9);
    color: #7f1d1d;
    border: 1px solid rgba(220,38,38,0.3);
    box-shadow: 0 4px 12px rgba(220,38,38,0.15);
}

/* ── Divider (Compact) ── */
.glow-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(254,226,226,0.35), transparent);
    border: none;
    margin: 10px 0;
}

/* ── Welcome card ── */
.welcome-card {
    background: #ffffff;
    border: 1px solid rgba(220,38,38,0.25);
    box-shadow: 0 24px 80px rgba(220,38,38,0.08);
    border-radius: 24px;
    padding: 32px 32px;
    text-align: center;
    margin-bottom: 24px;
}
.welcome-card h2 {
    margin: 0 0 12px 0;
    font-size: 32px;
    color: #b91c1c;
}
.welcome-card p {
    color: #1f2937;
    font-size: 15px;
    margin: 0 auto;
    max-width: 760px;
}
.welcome-card strong,
.welcome-card b {
    color: #991b1b;
}

/* ── Tool activity expander ── */
.tool-activity {
    background: rgba(254,226,226,0.85);
    border: 1px solid rgba(220,38,38,0.18);
    border-radius: 12px;
    padding: 10px 14px;
    margin: 8px 0;
    font-size: 13px;
    color: #7f1d1d;
}
.tool-name {
    color: #dc2626;
    font-weight: 600;
    font-family: 'JetBrains Mono', monospace;
}

/* ── Option pill buttons ── */
div[data-testid="stHorizontalBlock"] .option-pill-container button {
    border-radius: 24px !important;
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
    Your AI assistant for **Thapar Institute**.

    **Topics:**
    - 📋 Admissions (UG, PG, PhD, Diploma)
    - 💰 Fees & Charges
    - 🏠 Hostel Facilities
    - 🎓 Scholarships
    - 🌍 International Programs
    - 🏫 College Information
    """)

    st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)

    st.markdown("#### 💡 Quick Questions")
    quick_questions = [
        "B.Tech fees?",
        "Admission process?",
        "Scholarships?",
        "International programs?",
        "Hostel charges?",
    ]
    
    cols = st.columns(2)
    for i, q in enumerate(quick_questions):
        col = cols[i % 2]
        if col.button(q, key=f"qq_{q}", use_container_width=True):
            st.session_state.pending_question = {
                "B.Tech fees?": "What is the B.Tech fee structure?",
                "Admission process?": "How do I apply for admission?",
                "Scholarships?": "What scholarships are available?",
                "International programs?": "Tell me about international exchange programs",
                "Hostel charges?": "What are the hostel charges?",
            }.get(q, q)

    st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)

    if st.button("🔄 New Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.thread_id = str(uuid.uuid4())
        st.rerun()

    st.markdown(
        '<div style="position:fixed; bottom:16px; font-size:10px; color:#fecaca; opacity:0.8;">'
        'Powered by PageIndex & LangGraph'
        '</div>',
        unsafe_allow_html=True,
    )

# ──────────────────────────────────────────────────

# ──────────────────────────────────────────────────

# Welcome card (shown when no messages)

# ──────────────────────────────────────────────────

if not st.session_state.messages:
    st.markdown(
        """
        ## 🎓 Welcome to THAPAR Institute of Engineering & Technology

        ### Your AI Campus Companion is ready.

        **Scout AI** helps you find the best of Thapar:
        - Admissions and application guidance
        - Scholarship options and fee details
        - Hostel life, mess, and campus facilities
        - Academics, placements, and student activities

        > Start your journey with a warm Thapar welcome.

        🏛️ 70 Years of Excellence • 🚀 AI-powered college support • 🌍 Built for TIET students
        """
    )

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

    # Save to history
    st.session_state.messages.append({
        "role": "assistant",
        "content": full_content,
        "display_text": display_text,
        "options": options,
        "tool_calls": tool_calls_log,
    })
