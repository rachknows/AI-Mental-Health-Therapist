# Step 1: Importing libraries and setting-up Streamlit page
import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000/ask"

st.set_page_config(page_title="AI Mental Health Therapist", layout="wide")

st.title("MindMate: Your Personal Therapist")
st.caption("A safe space to share your thoughts")

# Sidebar section
with st.sidebar:
    st.header("What is MindMate?")
    st.write("Your AI companion for mental well being.")

    st.divider()

    if st.button("Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

# Step 2: Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Step 3: Display existing chat history FIRST
for msg in st.session_state.chat_history:

    avatar = "😊" if msg["role"] == "user" else "🪷"

    with st.chat_message(msg["role"], avatar=avatar):
        st.write(msg["content"])

# Step 4: Get user input
user_input = st.chat_input("What's on your mind today?")

if user_input:
    # Show user message immediately
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_input
    })

    try:
        # Spinner while backend processes
        with st.spinner("MindMate is thinking..."):
            response = requests.post(
                BACKEND_URL,
                json={"message": user_input}
            )

            data = response.json()

            bot_reply = data.get("response", "Sorry, I couldn't process that.")
            tool_used = data.get("tool_called", "None")

    except Exception:
        bot_reply = "⚠️ Backend service is currently unavailable."
        tool_used = "Error"

    # Add assistant response
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": f"{bot_reply}\n\n*(Tool used: {tool_used})*"
    })

    # Force UI refresh so new messages appear correctly
    st.rerun()