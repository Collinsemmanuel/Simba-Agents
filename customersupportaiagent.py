 # Rukia Hassan customer support AI agent 
 import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env file
load_dotenv()

# Initialize the Groq client
groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Function to handle user input and provide responses using Groq
def get_groq_response(user_question):
    chat_completion = groq_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": user_question,
            }
        ],
        model="llama-3.3-70b-versatile",
    )
    return chat_completion.choices[0].message.content

# Main function for user interaction
def main():
    print('I am customer support AI, Your personal Assistant')
    user_question = input('Please enter your question: ')
    
    # Get response from Groq
    groq_response = get_groq_response(user_question)
    print("Groq Response:", groq_response)

if __name__ == "__main__":
    main()