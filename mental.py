class MentalHealthAssistant:
    def __init__(self):
        self.introduction = "I'm here to listen and offer support, but I'm not a licensed therapist."
    
    def validate_emotions(self, user_input):
        # Simple validation of emotions
        if "anxious" in user_input:
            return "It's okay to feel anxious. Would you like to talk about what's causing it?"
        elif "stressed" in user_input:
            return "Stress can be overwhelming. Have you tried any relaxation techniques?"
        elif "self-harm" in user_input:
            return "I'm really concerned about what you're saying. It's important to talk to a professional."
        else:
            return "I'm here to listen. Please share what's on your mind."

    def coping_strategies(self):
        return "Here are some coping strategies: \n1. Deep breathing exercises \n2. Mindfulness meditation \n3. Journaling your thoughts"

    def ask_open_ended_questions(self):
        return "What do you think is the main source of your feelings right now?"

    def run(self):
        print(self.introduction)
        while True:
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit"]:
                print("Thank you for talking. Take care!")
                break
            response = self.validate_emotions(user_input)
            print("AI: " + response)
            if "self-harm" in user_input:
                print("AI: Please reach out to a mental health professional or a crisis hotline.")
            else:
                print("AI: " + self.coping_strategies())
                print("AI: " + self.ask_open_ended_questions())

if __name__ == "__main__":
    assistant = MentalHealthAssistant()
    assistant.run()