import os
import streamlit as st
import requests

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000/ask")

st.set_page_config(page_title="AI Mental Health Therapist", layout="wide")
st.title("MindMate: Your Personal Therapist")
st.caption("A safe space to share your thoughts")

with st.sidebar:
    st.header("What is MindMate?")
    st.write("Your AI companion for mental well being.")
    st.divider()
    if st.button("Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display existing chat history
for msg in st.session_state.chat_history:
    avatar = "😊" if msg["role"] == "user" else "🪷"
    with st.chat_message(msg["role"], avatar=avatar):
        st.write(msg["content"])
        # Show tool badge only on assistant messages that used a tool
        if msg["role"] == "assistant" and msg.get("tool_called", "None") != "None":
            st.caption(f"🔧 Tool used: `{msg['tool_called']}`")

# Get user input
user_input = st.chat_input("What's on your mind today?")

if user_input:
    # Append user message to history
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_input
    })

    try:
        with st.spinner("MindMate is thinking..."):
            # ✅ Send the FULL chat history so the backend has full context
            response = requests.post(
                BACKEND_URL,
                json={
                    "message": user_input,
                    "history": st.session_state.chat_history[:-1]  # exclude the just-appended user msg
                }
            )
            data = response.json()
            bot_reply = data.get("response", "Sorry, I couldn't process that.")
            tool_used = data.get("tool_called", "None")

    except Exception:
        bot_reply = "⚠️ Backend service is currently unavailable."
        tool_used = "Error"

    

    # Append assistant reply to history
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": bot_reply,
        "tool_called": tool_used
    })


    st.rerun()
