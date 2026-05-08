import streamlit as st
import streamlit.components.v1 as components
from Agent.graph import Agent
import uuid
import re
import json
from pathlib import Path

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
#MainMenu { display: none !important; }
footer { display: none !important; }

/* Hide header background but keep sidebar toggle visible */
header[data-testid="stHeader"] {
    background: transparent !important;
    height: 0 !important;
    overflow: visible !important;
}

/* Ensure sidebar toggle button is always clickable */
[data-testid="collapsedControl"],
[data-testid="stSidebarCollapsedControl"],
button[kind="headerNoPadding"] {
    visibility: visible !important;
    z-index: 999 !important;
    position: fixed !important;
    top: 8px !important;
    left: 8px !important;
}

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


def _set_pending(question: str):
    """Callback for option/quick-question buttons — sets the pending question."""
    st.session_state.pending_question = question


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
        st.button(
            q,
            key=f"qq_{q}",
            use_container_width=True,
            on_click=_set_pending,
            args=(q,),
        )

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
                col.button(
                    f"👉 {opt}",
                    key=f"opt_{idx}_{i}",
                    use_container_width=True,
                    on_click=_set_pending,
                    args=(opt,),
                )

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

    # Get agent response (streamed)
    with st.chat_message("assistant", avatar="🎓"):
        tool_calls_log = []
        full_content = ""
        tool_expander = None
        text_placeholder = st.empty()
        thinking_cleared = False

        # Load facts from JSON
        facts_path = Path(__file__).parent / "thaparfacts.json"
        with open(facts_path, "r", encoding="utf-8") as f:
            thapar_facts = json.load(f)
        facts_json = json.dumps(thapar_facts)
        first_emoji = thapar_facts[0]["emoji"] if thapar_facts else "🎓"
        first_text = thapar_facts[0]["text"] if thapar_facts else "Loading..."

        # Show thinking animation with Lottie avatar + Thapar facts
        thinking_html = """
            <script src="https://cdnjs.cloudflare.com/ajax/libs/lottie-web/5.12.2/lottie.min.js"></script>
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

            * { margin: 0; padding: 0; box-sizing: border-box; }

            .thinking-container {
                font-family: 'Inter', sans-serif;
                display: flex;
                flex-direction: column;
                align-items: center;
                padding: 16px 16px 12px;
            }

            /* Lottie avatar wrapper */
            .avatar-wrapper {
                width: 120px;
                height: 120px;
                border-radius: 50%;
                background: linear-gradient(135deg, rgba(59,130,246,0.12), rgba(139,92,246,0.12));
                display: flex;
                align-items: center;
                justify-content: center;
                margin-bottom: 10px;
                position: relative;
                animation: pulse-ring 2.5s ease-in-out infinite;
            }

            .avatar-wrapper::before {
                content: '';
                position: absolute;
                width: 140px;
                height: 140px;
                border-radius: 50%;
                border: 2px solid rgba(59,130,246,0.15);
                animation: ping 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
            }

            #lottie-avatar {
                width: 90px;
                height: 90px;
            }

            @keyframes pulse-ring {
                0%, 100% { box-shadow: 0 0 0 0 rgba(59,130,246,0.15); }
                50% { box-shadow: 0 0 0 12px rgba(139,92,246,0.05); }
            }

            @keyframes ping {
                0% { transform: scale(1); opacity: 0.6; }
                75%, 100% { transform: scale(1.15); opacity: 0; }
            }

            /* Status label */
            .thinking-label {
                font-size: 13px;
                font-weight: 600;
                color: #60a5fa;
                margin-bottom: 12px;
                display: flex;
                align-items: center;
                gap: 8px;
            }

            .thinking-label .dot-pulse {
                display: flex;
                gap: 4px;
            }

            .thinking-label .dot-pulse span {
                width: 5px;
                height: 5px;
                border-radius: 50%;
                background: #8b5cf6;
                animation: dotPulse 1.4s ease-in-out infinite;
            }
            .thinking-label .dot-pulse span:nth-child(2) { animation-delay: 0.2s; }
            .thinking-label .dot-pulse span:nth-child(3) { animation-delay: 0.4s; }

            @keyframes dotPulse {
                0%, 80%, 100% { opacity: 0.3; transform: scale(0.8); }
                40% { opacity: 1; transform: scale(1.3); }
            }

            /* Fact card */
            .fact-card {
                background: linear-gradient(135deg, rgba(59,130,246,0.06), rgba(139,92,246,0.06));
                border: 1px solid rgba(99,102,241,0.15);
                border-radius: 16px;
                padding: 12px 20px;
                text-align: center;
                max-width: 400px;
                width: 100%;
                animation: fadeSwap 0.5s ease;
            }

            .fact-emoji {
                font-size: 22px;
                margin-bottom: 4px;
            }

            .fact-text {
                font-size: 13px;
                font-weight: 500;
                color: #94a3b8;
                line-height: 1.5;
            }

            .fact-label {
                font-size: 10px;
                text-transform: uppercase;
                letter-spacing: 1.5px;
                color: #475569;
                margin-bottom: 8px;
                font-weight: 600;
            }

            @keyframes fadeSwap {
                from { opacity: 0; transform: translateY(6px); }
                to   { opacity: 1; transform: translateY(0); }
            }
            </style>

            <div class="thinking-container">
                <div class="avatar-wrapper">
                    <div id="lottie-avatar"></div>
                </div>

                <div class="thinking-label">
                    Scout is thinking
                    <div class="dot-pulse">
                        <span></span><span></span><span></span>
                    </div>
                </div>

                <div class="fact-label">✨ Did you know?</div>
                <div class="fact-card" id="fact-card">
                    <div class="fact-emoji" id="fact-emoji">FIRST_EMOJI</div>
                    <div class="fact-text" id="fact-text">FIRST_TEXT</div>
                </div>
            </div>

            <script>
            // Load Lottie animation
            lottie.loadAnimation({
                container: document.getElementById('lottie-avatar'),
                renderer: 'svg',
                loop: true,
                autoplay: true,
                path: 'https://assets9.lottiefiles.com/packages/lf20_zrqthn6o.json'
            });

            // Rotate facts
            const facts = FACTS_PLACEHOLDER;
            let idx = 0;
            setInterval(() => {
                idx = (idx + 1) % facts.length;
                const card = document.getElementById("fact-card");
                const emoji = document.getElementById("fact-emoji");
                const text = document.getElementById("fact-text");
                if (card && emoji && text) {
                    card.style.animation = "none";
                    void card.offsetHeight;
                    card.style.animation = "fadeSwap 0.5s ease";
                    emoji.innerText = facts[idx].emoji;
                    text.innerText = facts[idx].text;
                }
            }, 3000);
            </script>
        """
        thinking_html = thinking_html.replace("FACTS_PLACEHOLDER", facts_json)
        thinking_html = thinking_html.replace("FIRST_EMOJI", first_emoji)
        thinking_html = thinking_html.replace("FIRST_TEXT", first_text)

        with text_placeholder.container():
            components.html(thinking_html, height=320)

        for event in st.session_state.agent.stream(
            user_input,
            config={"configurable": {"thread_id": st.session_state.thread_id}},
        ):
            if event["type"] == "tool_call":
                # Show/update tool activity expander
                if tool_expander is None:
                    tool_expander = st.expander("🔧 Tool activity", expanded=True)
                with tool_expander:
                    st.markdown(
                        f'<div class="tool-activity">'
                        f'Called <span class="tool-name">{event["name"]}</span>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

            elif event["type"] == "token":
                if not thinking_cleared:
                    text_placeholder.empty()
                    thinking_cleared = True
                full_content += event["content"]
                text_placeholder.markdown(full_content + "▌")

            elif event["type"] == "done":
                full_content = event["full_content"]
                tool_calls_log = event.get("tool_calls", [])

        # Collapse tool expander after done
        if tool_expander is not None:
            tool_expander.expanded = False

        # Parse options from the final response
        display_text, options = parse_options(full_content)

        # Render final text (remove cursor)
        text_placeholder.markdown(display_text)

        # Show option pills as buttons
        if options:
            cols = st.columns(min(len(options), 3))
            for i, opt in enumerate(options):
                col = cols[i % min(len(options), 3)]
                col.button(
                    f"👉 {opt}",
                    key=f"new_opt_{i}",
                    use_container_width=True,
                    on_click=_set_pending,
                    args=(opt,),
                )

    # Save to history
    st.session_state.messages.append({
        "role": "assistant",
        "content": full_content,
        "display_text": display_text,
        "options": options,
        "tool_calls": tool_calls_log,
    })
