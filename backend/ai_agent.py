# Step 1: Imports
from langchain.tools import tool
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langgraph.prebuilt import create_react_agent
from backend.config import HF_API_KEY
from backend.tools import (
    query_medgemma,
    find_nearby_therapists_by_location,
    get_user_location
)


# Step 2: Define Tools

@tool
def ask_mental_health_specialist(query: str) -> str:
    """Generates a therapeutic response using the MedGemma model."""
    return query_medgemma(query)


@tool
def locate_therapists(location: str) -> str:
    """Find therapists near a given location."""
    return find_nearby_therapists_by_location(location)


@tool
def detect_user_location() -> str:
    """Detect user's approximate location."""
    return get_user_location()


# Step 3: Register Tools
tools = [
    ask_mental_health_specialist,
    locate_therapists,
    detect_user_location
]


# Step 4: Setup HuggingFace LLM
hf_llm = HuggingFaceEndpoint(
    repo_id="openai/gpt-oss-20b",
    huggingfacehub_api_token=HF_API_KEY,
    task="text-generation",
    temperature=0.2,
    max_new_tokens=512
)

llm = ChatHuggingFace(llm=hf_llm)


# Step 5: System Prompt
SYSTEM_PROMPT = """
You are a compassionate AI assistant supporting mental health conversations.

Available tools:

1. ask_mental_health_specialist
Use this for emotional support and mental health guidance.

2. locate_therapists
Use this if the user asks for therapists in a specific location.

3. detect_user_location
Use this when the user asks for therapists 'near me'.

If the user says 'near me':
1. Call detect_user_location
2. Then call locate_therapists using the detected location.

Always respond with warmth and empathy.
"""


# Step 6: Create Agent
graph = create_react_agent(llm, tools=tools)


# Step 7: Parse Response
def parse_response(stream):

    tool_called_name = "None"
    final_response = None

    for s in stream:

        tool_data = s.get("tools")
        if tool_data:
            tool_messages = tool_data.get("messages")

            if tool_messages:
                for msg in tool_messages:
                    tool_called_name = getattr(msg, "name", "None")

        agent_data = s.get("agent")
        if agent_data:
            messages = agent_data.get("messages")

            if messages:
                for msg in messages:
                    content = getattr(msg, "content", None)

                    if content:
                        final_response = content

    return tool_called_name, final_response


# Local Testing
if __name__ == "__main__":

    while True:

        user_input = input("User: ")

        inputs = {
            "messages": [
                ("system", SYSTEM_PROMPT),
                ("user", user_input)
            ]
        }

        stream = graph.stream(inputs, stream_mode="updates")

        tool_called_name, final_response = parse_response(stream)

        print("TOOL CALLED:", tool_called_name)
        print("ANSWER:", final_response)