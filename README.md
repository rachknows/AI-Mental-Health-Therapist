# 🧠 AI Mental Health Assistant

An AI-powered conversational assistant designed to provide supportive mental health conversations and help users discover nearby therapists.
This project demonstrates how **LLM agents, specialized medical models, and external tools** can be orchestrated together to create a practical AI application.

The system combines **LangGraph agents**, **FastAPI**, and a **Streamlit conversational interface** to create an assistant that can both hold empathetic conversations and perform useful real-world actions such as searching for therapists.

---

# ✨ Project Overview

Mental health support systems powered by AI can help bridge the gap between people seeking help and the resources available to them.

This project implements a **tool-enabled AI agent** capable of:

• engaging in supportive mental health conversations
• searching for therapists using real-world web data
• detecting user location for nearby recommendations
• using specialized medical AI models when appropriate

Rather than relying on a single model, the system uses a **multi-model architecture** where one model handles reasoning while another model is used as a domain-specific tool.

---

# 🏗️ System Architecture

The application follows a modular architecture designed for AI agent experimentation and real-world integrations.

```id="arch1"
User (Streamlit Chat UI)
        │
        ▼
FastAPI Backend API
        │
        ▼
LangGraph Agent
        │
        ▼
Agent LLM (Open-source model via HuggingFace)
        │
 ┌──────┴─────────────┐
 │                    │
 ▼                    ▼
External Tools        MedGemma Tool
- DuckDuckGo Search   (Medical LLM)
- Location Detection
- Therapist Finder
```

The **agent decides when tools should be used**, allowing the system to dynamically adapt to different user needs.

---

# 🤖 Multi-Model AI Design

This system intentionally separates **reasoning** from **domain expertise**.

## 1️⃣ Agent / Reasoning Model

The primary reasoning model is an **open-source OpenAI-style LLM served via the Hugging Face inference API**.

Responsibilities:

* understanding user intent
* deciding when to call tools
* coordinating responses
* managing conversation flow

This model acts as the **decision-making layer of the agent**.

---

## 2️⃣ MedGemma Medical Model (Tool)

MedGemma is integrated as a **specialized tool** rather than the main conversational model.

The agent calls this tool when the user needs:

* emotional support
* empathetic conversation
* mental health guidance

This allows the system to combine:

* general reasoning capability from the agent LLM
* domain expertise from a medical-focused model

---

# 🧰 Tools Available to the Agent

The LangGraph agent has access to several tools.

## 🔎 DuckDuckGo Search Tool

Used to search for therapists and mental health resources on the web.

Example:

> "Find therapists in Bangalore"

The agent performs a web search and extracts relevant recommendations.

---

## 📍 Location Detection Tool

Used when a user asks for help **"near me"**.

The system detects the user's approximate location and uses that information when searching for therapists.

---

## 🧠 Mental Health Specialist Tool

This tool calls the **MedGemma model** to generate supportive and empathetic responses for mental health conversations.

---

# 💬 Example Conversations

### Example 1 — Emotional Support

User:

> "I've been feeling really anxious about work lately."

Assistant:

> "That sounds difficult. When stress starts affecting our daily life it can feel overwhelming. Would you like to talk about what's been causing the anxiety?"

---

### Example 2 — Therapist Discovery

User:

> "Can you help me find a therapist near me?"

Agent reasoning:

1. detect user location
2. search therapists using DuckDuckGo
3. return recommendations

---

# 🖥️ Tech Stack

| Layer           | Technology                 |
| --------------- | -------------------------- |
| Frontend        | Streamlit                  |
| Backend API     | FastAPI                    |
| Agent Framework | LangGraph                  |
| LLM Integration | Hugging Face Inference API |
| Medical Model   | MedGemma                   |
| Search Tool     | DuckDuckGo                 |
| Language        | Python                     |

---

# 📂 Project Structure

```id="structure1"
AI-Mental-Health-Therapist
│
├── backend
│   ├── main.py          # FastAPI server
│   ├── ai_agent.py      # LangGraph agent logic
│   ├── tools.py         # Tool implementations
│   └── config.py        # API configuration
│
├── frontend.py          # Streamlit UI
│
├── requirements.txt
├── .gitignore
├── .env
└── README.md
```

---

# 🚀 Running the Project Locally

## 1️⃣ Clone the repository

```id="run1"
git clone https://github.com/YOUR_USERNAME/AI-Mental-Health-Therapist.git
cd AI-Mental-Health-Therapist
```

---

## 2️⃣ Create a virtual environment

Using **uv**:

```id="run2"
uv venv
source .venv/Scripts/activate
```

---

## 3️⃣ Install dependencies

```id="run3"
uv pip install -r requirements.txt
```

---

## 4️⃣ Set environment variables

Create a `.env` file:

```id="run4"
HF_API_KEY=your_huggingface_api_key
```

---

## 5️⃣ Start the backend server

```id="run5"
uvicorn backend.main:app --reload
```

Backend runs at:

```id="run6"
http://localhost:8000
```

Swagger docs:

```id="run7"
http://localhost:8000/docs
```

---

## 6️⃣ Start the Streamlit UI

Open another terminal:

```id="run8"
streamlit run frontend.py
```

Streamlit will run at:

```id="run9"
http://localhost:8501
```

---

# 🔮 Possible Future Improvements

• conversation memory using LangGraph memory
• retrieval-augmented generation for mental health resources
• crisis detection and escalation mechanisms
• voice-based conversational interface
• Docker deployment
• persistent chat history

---

# ⚠️ Disclaimer

This project is intended for **educational and research purposes only**.

It is **not a replacement for professional therapy or medical advice**.
Anyone experiencing serious mental health concerns should consult qualified professionals.

---

# 📜 License

MIT License

---

# 👨‍💻 Author

Created as an exploration of **AI agents, multi-model orchestration, and real-world AI applications** using modern LLM tooling.
