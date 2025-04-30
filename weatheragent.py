import os
import requests
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env file
load_dotenv()

# Initialize the Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Function to fetch weather information
def fetch_weather(city):
    api_key = os.getenv('OPENWEATHER_API_KEY')  # Make sure to set this in your .env file
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Prompt the user for a city
city = input('I am Weather AI, Your personal Assistant\nPlease enter the city name: ')

# Fetch weather data
weather_data = fetch_weather(city)
if weather_data:
    weather_description = weather_data['weather'][0]['description']
    temperature = weather_data['main']['temp']
    print(f"Weather in {city}: {weather_description}, Temperature: {temperature}°C")
else:
    print("Could not fetch weather data. Please check the city name.")

# Use Groq for chat completion
user_question = input('Please enter your question: ')
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": user_question,
        }
    ],
    model="llama-3.3-70b-versatile",
)

print(chat_completion.choices[0].message.content)