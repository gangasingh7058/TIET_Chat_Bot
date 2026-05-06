# TietBot — College Assistant 🎓

TietBot is an AI-powered chatbot that answers queries about **Thapar Institute of Engineering & Technology (TIET)**. It uses **LangGraph**, **HuggingFace**, and **PageIndex** to search through college documents and provide accurate, sourced answers.

---

## ✨ Features

- 🔍 **Document Search** — Queries indexed college PDFs for relevant information
- 🗂️ **Structured Retrieval** — Navigates document hierarchies to find precise sections
- 📖 **Page-Level Access** — Fetches exact pages for detailed answers
- 🧠 **Agentic Tool Use** — The agent plans and uses tools autonomously
- 💬 **Multi-turn Conversations** — Full conversation memory via LangGraph checkpointing
- 🎨 **Polished Streamlit UI** — Glassmorphism, gradient backgrounds, and smooth animations

---

## 🏗️ Project Structure

```
Tiet Chat Bot/
├── Agent/
│   ├── __init__.py
│   ├── graph.py              # LangGraph agent definition, state, and routing
│   ├── tools.py              # PageIndex tools (list_documents, get_structure, get_page)
│   └── prompts/
│       ├── __init__.py
│       ├── prompts.py        # Loads the system prompt from markdown
│       └── college_assistant.md  # System prompt for TietBot
├── PDFS/                     # Source college PDF documents
├── .streamlit/
│   └── config.toml           # Streamlit theme configuration
├── app.py                    # Streamlit frontend
├── index_docs.py             # One-time script to index PDFs with PageIndex
├── doc_ids.json              # Mapping of PDF filenames → PageIndex doc IDs
├── requirements.txt          # Python dependencies
├── .env                      # API keys (not committed)
└── README.md
```

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/your-username/tiet-chat-bot.git
cd tiet-chat-bot
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
.\venv\Scripts\Activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root:

```env
HUGGING_FACE_API_TOKEN=your_huggingface_token_here
```

| Variable | Where to get it |
|---|---|
| `HUGGING_FACE_API_TOKEN` | [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) |

### 5. Index the documents (one-time)

```bash
python index_docs.py
```

### 6. Run the chatbot

```bash
streamlit run app.py
```

---

## 🧠 How It Works

```
User Query
    │
    ▼
LangGraph Agent (main_node)
    │
    ├── list_documents()          ← See all available college PDFs
    ├── get_document_structure()  ← Get document outline & section map
    └── get_page_content()        ← Fetch specific pages for detail
    │
    ▼
Tool Result → LLM → Final Answer
```

TietBot uses a **ReAct-style agentic loop**:
1. The LLM receives your question and the available tools
2. It plans which tool(s) to call and in what order
3. Tool results are fed back to the LLM
4. The LLM generates a final, grounded answer

---

## 📚 Available Documents

| Document | Content |
|---|---|
| Brief Intro | Overview of TIET |
| UG Admission Details | Undergraduate admission process, eligibility, cutoffs |
| Diploma Admission | Diploma program admissions |
| Fees & Hostel Details | Fee structure and hostel charges |
| International Programs | Exchange programs and international tie-ups |
| Scholarships | Merit and financial aid scholarships |

---

## 🤖 Model

By default, TietBot uses **`Qwen/Qwen2.5-72B-Instruct`** via the HuggingFace Inference API.

---

## 📋 Requirements

- Python 3.10+
- HuggingFace account (free tier works)
- Local PageIndex installation

---

## 📄 License

MIT License
