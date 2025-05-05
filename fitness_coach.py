#Sheila Chebii
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage
from langgraph.graph import StateGraph, END
from typing import TypedDict, List

# Load environment variables
load_dotenv()

# Initialize the language model with temperature setting
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Test the connection
def test_connection():
    try:
        response = llm.invoke("Hello! Are you ready to help with fitness?")
        print(response.content)
    except Exception as e:
        print(f"Error connecting to the model: {e}")

# Define the State TypedDict
class State(TypedDict):
    user_data: dict  # Stores user information (e.g., goals, preferences)
    workout_plan: List[str]  # List of workouts
    progress: dict  # Tracks user progress

# Function to handle user queries
def handle_user_query(query: str) -> str:
    try:
        response = llm.invoke(query)
        return response.content
    except Exception as e:
        return f"Error processing your query: {e}"

# Main function to interact with the user
def main():
    test_connection()
    
    while True:
        user_query = input("What would you like to know about fitness? (type 'exit' to quit): ")
        if user_query.lower() == 'exit':
            print("Goodbye!")
            break
        
        response = handle_user_query(user_query)
        print("Response:", response)

if __name__ == "__main__":
    main()