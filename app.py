import streamlit as st
import streamlit.components.v1 as components
from Agent.graph import Agent
import uuid
import re

# ──────────────────────────────────────────────────
# Page config
# ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Scout — College Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────
# CSS
# ──────────────────────────────────────────────────
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

*{
    font-family:'Inter',sans-serif;
}

.stApp{
    background:linear-gradient(180deg,#ffffff 0%,#fff7f7 100%);
}

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

/* Chat styling */

.stChatMessage{
    border-radius:18px !important;
    padding:12px 16px !important;
    margin-bottom:10px !important;
    animation:fadeIn 0.3s ease;
}

@keyframes fadeIn{
    from{
        opacity:0;
        transform:translateY(10px);
    }
    to{
        opacity:1;
        transform:translateY(0px);
    }
}

/* User */

[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]){
    background:#fee2e2 !important;
    border-left:4px solid #991b1b !important;
}

/* Assistant */

[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]){
    background:#fff7ed !important;
    border-left:4px solid #b91c1c !important;
}

/* Input */

.stChatInput > div{
    border-radius:18px !important;
    border:1px solid rgba(127,29,29,0.3) !important;
    background:white !important;
}

/* Sidebar */

section[data-testid="stSidebar"]{
    background:linear-gradient(
        135deg,
        #7f1d1d 0%,
        #991b1b 50%,
        #b91c1c 100%
    ) !important;
}

section[data-testid="stSidebar"] *{
    color:white !important;
}

.glow-divider{
    height:1px;
    background:rgba(255,255,255,0.2);
    margin:14px 0;
    border:none;
}

.status-badge{
    background:rgba(255,255,255,0.12);
    padding:6px 12px;
    border-radius:18px;
    display:inline-block;
    font-size:12px;
}

/* Tool activity */

.tool-activity{
    background:#fee2e2;
    border-radius:12px;
    padding:10px;
    margin-bottom:8px;
}

/* Welcome */

.welcome-box{
    text-align:center;
    padding:30px;
    background:white;
    border-radius:24px;
    box-shadow:0 10px 40px rgba(0,0,0,0.06);
    margin-bottom:20px;
}

.welcome-box h1{
    color:#991b1b;
}

/* Thinking Animation */

.thinking-wrapper{
    width:100%;
    display:flex;
    flex-direction:column;
    align-items:center;
    justify-content:center;
    margin-top:10px;
    margin-bottom:10px;
}

.runner-area{
    width:100%;
    height:140px;
    position:relative;
    overflow:hidden;
}

.runner{
    position:absolute;
    top:20px;
    right:-350px;
    animation:runAcross 7s linear infinite;
    display:flex;
    align-items:center;
    gap:16px;
}

.runner-char{
    font-size:82px;
}

.thought-cloud{
    position:relative;
    background:white;
    color:#991b1b;
    padding:14px 22px;
    border-radius:30px;
    font-size:15px;
    font-weight:700;
    white-space:nowrap;
    box-shadow:0 10px 30px rgba(0,0,0,0.12);
}

.thought-cloud::before{
    content:'';
    position:absolute;
    width:16px;
    height:16px;
    background:white;
    border-radius:50%;
    left:-10px;
    bottom:10px;
}

.thought-cloud::after{
    content:'';
    position:absolute;
    width:10px;
    height:10px;
    background:white;
    border-radius:50%;
    left:-18px;
    bottom:2px;
}

.thinking-facts{
    margin-top:10px;
    font-size:18px;
    font-weight:700;
    color:#991b1b;
    animation:pulseText 2s infinite;
}

@keyframes runAcross{
    0%{
        right:-350px;
    }
    100%{
        right:110%;
    }
}

@keyframes pulseText{
    0%{opacity:0.3;}
    50%{opacity:1;}
    100%{opacity:0.3;}
}

</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────

OPTIONS_PATTERN = re.compile(
    r"\[OPTIONS\]\s*\n(.*?)\n\s*\[/OPTIONS\]",
    re.DOTALL
)

def parse_options(text: str):

    match = OPTIONS_PATTERN.search(text)

    if not match:
        return text, []

    options_raw = match.group(1).strip()

    options = [
        opt.strip("- •").strip()
        for opt in options_raw.splitlines()
        if opt.strip()
    ]

    clean_text = text[:match.start()].rstrip()

    trailing = text[match.end():].strip()

    if trailing:
        clean_text += "\n\n" + trailing

    return clean_text, options

# ──────────────────────────────────────────────────
# Session state
# ──────────────────────────────────────────────────

if "agent" not in st.session_state:
    st.session_state.agent = Agent(name="Scout")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

# ──────────────────────────────────────────────────
# Sidebar
# ──────────────────────────────────────────────────

with st.sidebar:

    st.markdown("## 🎓 Scout")

    st.markdown(
        '<div class="glow-divider"></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<span class="status-badge">● Online</span>',
        unsafe_allow_html=True
    )

    st.markdown("""
    ### TIET Assistant

    - 📋 Admissions
    - 💰 Fees
    - 🏠 Hostel
    - 🎓 Scholarships
    - 🌍 International Programs
    """)

    st.markdown(
        '<div class="glow-divider"></div>',
        unsafe_allow_html=True
    )

    if st.button("🔄 New Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.thread_id = str(uuid.uuid4())
        st.rerun()

# ──────────────────────────────────────────────────
# Welcome
# ──────────────────────────────────────────────────

if not st.session_state.messages:

    st.markdown("""
    <div class="welcome-box">

    <h1>🎓 Welcome to THAPAR</h1>

    <p>
    Your AI Campus Companion is ready.
    Ask anything about admissions, hostel,
    fees, scholarships and student life.
    </p>

    <br>

    🏛️ 70 Years of Excellence • 🚀 AI Powered Support

    </div>
    """, unsafe_allow_html=True)

# ──────────────────────────────────────────────────
# Chat history
# ──────────────────────────────────────────────────

for idx, msg in enumerate(st.session_state.messages):

    avatar = "🎓" if msg["role"] == "assistant" else "👤"

    with st.chat_message(msg["role"], avatar=avatar):

        display_text = msg.get(
            "display_text",
            msg["content"]
        )

        st.markdown(display_text)

# ──────────────────────────────────────────────────
# Input
# ──────────────────────────────────────────────────

user_input = st.chat_input(
    "Ask me anything about TIET..."
)

if user_input:

    st.session_state.messages.append({
        "role":"user",
        "content":user_input
    })

    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)

    with st.chat_message("assistant", avatar="🎓"):

        thinking_placeholder = st.empty()

        components.html("""
<style>

.thinking-wrapper{
    width:100%;
    display:flex;
    flex-direction:column;
    align-items:center;
    justify-content:center;
    margin-top:10px;
    margin-bottom:10px;
}

.runner-area{
    width:100%;
    height:150px;
    position:relative;
    overflow:hidden;
}

.runner{
    position:absolute;
    top:25px;
    right:-350px;
    animation:runAcross 7s linear infinite;
    display:flex;
    align-items:center;
    gap:18px;
}

.runner-char{
    font-size:90px;
}

.thought-cloud{
    position:relative;
    background:white;
    color:#991b1b;
    padding:14px 24px;
    border-radius:30px;
    font-size:16px;
    font-weight:700;
    white-space:nowrap;
    box-shadow:0 10px 25px rgba(0,0,0,0.15);
}

.thought-cloud::before{
    content:'';
    position:absolute;
    width:16px;
    height:16px;
    background:white;
    border-radius:50%;
    left:-10px;
    bottom:10px;
}

.thought-cloud::after{
    content:'';
    position:absolute;
    width:10px;
    height:10px;
    background:white;
    border-radius:50%;
    left:-18px;
    bottom:2px;
}

.thinking-facts{
    margin-top:10px;
    font-size:18px;
    font-weight:700;
    color:#991b1b;
    text-align:center;
}

@keyframes runAcross{
    0%{
        right:-400px;
    }
    100%{
        right:110%;
    }
}

</style>

<div class="thinking-wrapper">

    <div class="runner-area">

        <div class="runner">

            <div class="runner-char">
                🧑‍🎓
            </div>

            <div class="thought-cloud">
                💭 Thinking...
            </div>

        </div>

    </div>

    <div class="thinking-facts" id="fact-box">
        🏛️ TIET celebrates 70 years of excellence
    </div>

</div>

<script>

const facts = [
"🏛️ TIET celebrates 70 years of excellence",
"🚀 Strong placement culture at Thapar",
"🌍 International exchange opportunities available",
"📚 One of India's top engineering institutes",
"💡 Innovation drives the TIET ecosystem",
"🤖 Scout AI is exploring campus knowledge"
];

let factIndex = 0;

setInterval(() => {

    factIndex = (factIndex + 1) % facts.length;

    document.getElementById("fact-box").innerText =
    facts[factIndex];

}, 2000);

</script>
""", height=220)

        result = st.session_state.agent.invoke(
            user_input,
            config={
                "configurable":{
                    "thread_id":
                    st.session_state.thread_id
                }
            },
        )

        thinking_placeholder.empty()

        tool_calls_log = []
        final_content = ""

        for msg in result["messages"]:

            if msg.type == "ai":

                if msg.content:
                    final_content = msg.content

        display_text, options = parse_options(
            final_content
        )

        st.markdown(display_text)

    st.session_state.messages.append({
        "role":"assistant",
        "content":final_content,
        "display_text":display_text,
        "options":[]
    })