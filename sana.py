# lawrence wafula
import os
import asyncio
import logging
from typing import Literal
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic import BaseModel
import random

# Load environment variables
load_dotenv()

# Initialize logging
logging.basicConfig(filename='sana_ai.log', level=logging.INFO)

# make the Message class
class Message(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str


# Initialize the health-focused AI agent
health_agent = Agent(
    'openai:gpt-4o',
    system_message=(
        "You are SANA AI, an empathetic, professional health assistant. "
        "You maintain helpful, supportive conversations about health and wellness. "
        "If a user describes urgent or dangerous symptoms, gently suggest they consult a medical professional immediately."
    )
)

# Start conversation history
conversation_history = [
    Message(role="system", content="You are now assisting a user with health questions.")
]

async def chat():
    print("🩺 Welcome to SANA AI — Your Personal Health Assistant 🌱")
    print("Type 'exit' anytime to end the conversation.\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in {'exit', 'quit'}:
            print("\n👋 Goodbye! Stay healthy!")
            break

        if not user_input:
            print("⚠️ Please enter a valid question or statement.")
            continue

        # Log user input
        logging.info(f"User: {user_input}")
        conversation_history.append(Message(role="user", content=user_input))

        try:
            response = await health_agent.run(conversation_history)
            print(f"\nSANA AI: {response.output}\n")

            # Add assistant's reply to the history
            conversation_history.append(Message(role="assistant", content=response.output))

            # User feedback
            feedback = input("Was this response helpful? (yes/no): ").strip().lower()
            if feedback == 'no':
                print("Thank you for your feedback! We'll work on improving.")

        except Exception as e:
            print(f"⚠️ Oops, something went wrong: {str(e)}. Please try again.")

if __name__ == "__main__":
    try:
        asyncio.run(chat())
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! Stay healthy!")
