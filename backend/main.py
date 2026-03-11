from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import uvicorn

from backend.ai_agent import graph, SYSTEM_PROMPT, parse_response

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# A single turn in the conversation history
class ChatMessage(BaseModel):
    role: str          # "user" or "assistant"
    content: str


# Request now accepts history alongside the new message
class Query(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)
    history: Optional[List[ChatMessage]] = []


@app.post("/ask")
def ask(query: Query):

    # Step 1: Start with the system prompt
    messages = [("system", SYSTEM_PROMPT)]

    # Step 2: Replay all prior conversation turns so the agent has full context
    for turn in query.history:
        if turn.role == "user":
            messages.append(("user", turn.content))
        elif turn.role == "assistant":
            messages.append(("assistant", turn.content))

    # Step 3: Append the current user message
    messages.append(("user", query.message))

    # Step 4: Run the agent with the full conversation thread
    inputs = {"messages": messages}
    stream = graph.stream(inputs, stream_mode="updates")
    tool_called_name, final_response = parse_response(stream)

    return {
        "response": final_response or "I'm sorry, I couldn't generate a response.",
        "tool_called": tool_called_name
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
