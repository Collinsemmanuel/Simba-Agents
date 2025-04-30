import os
from dotenv import load_dotenv
from together import Together

# Load environment variables from .env file
load_dotenv()

# Initialize the Together client with the API key from the .env file
client = Together()  # Auth is read from TOGETHER_API_KEY in .env

# Prompt the user for their raw startup idea
user_question = input(
    "🚀 Welcome to DreamForge — where raw startup ideas become structured products.\n"
    "Tell me your idea in one sentence or paragraph. The messier, the better.\n"
    "I'll help refine it, shape your Lean Canvas, and sketch an MVP blueprint.\n"
    "Ready when you are. Just type your idea below 👇:\n"
)

# Define a system message to constrain the LLM's behavior
system_message = {
    "role": "system",
    "content": (
        "You are DreamForge, an AI agent that ONLY assists with startup ideas. "
        "Your job is to help users refine raw startup concepts, generate Lean Canvas breakdowns, and sketch MVP technical blueprints. "
        "If the user's message is not clearly a startup idea or related to building a startup, DO NOT answer it. "
        "Instead, politely respond: 'DreamForge is only for startup-related ideas. Please share a startup concept you'd like help with.'"
    )
}

# Create the conversation
messages = [
    system_message,
    {"role": "user", "content": user_question}
]

# Make the API call
response = client.chat.completions.create(
    model="meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
    messages=messages
)

# Output the result
print("\n🧠 DreamForge's Response:\n")
print(response.choices[0].message.content)
