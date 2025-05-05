#Ron Moen 
import random
class HealthAssistant:
    def __init__(self):
        self.symptoms = []
        self.red_flag_symptoms = ["chest pain", "high fever", "blood in stool", "confusion", "suicidal thoughts"]

    def ask_symptoms(self):
        # Ask user about their symptoms
        symptom = input("What symptoms are you experiencing? ")
        self.symptoms.append(symptom)
        self.check_symptoms(symptom)

    def check_symptoms(self, symptom):
        if symptom in self.red_flag_symptoms:
            print("It's important to seek immediate help at a nearby clinic or hospital.")
        else:
            print("Let's gather more information about your symptoms.")

    def provide_information(self):
        # Provide general health information
        conditions = {
            "malaria": "Malaria is caused by parasites transmitted through mosquito bites.",
            "typhoid": "Typhoid fever is caused by Salmonella typhi bacteria.",
            "UTI": "A urinary tract infection is an infection in any part of the urinary system.",
            "cold": "The common cold is a viral infection of your upper respiratory tract.",
            "COVID-19": "COVID-19 is caused by the coronavirus SARS-CoV-2.",
        }
        condition = input("Which condition would you like to know about? ")
        print(conditions.get(condition.lower(), "Sorry, I don't have information on that condition."))

    def suggest_doctor_visit(self):
        print("If you're unsure about your symptoms, it's best to consult a doctor.")

if __name__ == "__main__":
    assistant = HealthAssistant()
    while True:
        action = input("Would you like to (1) describe symptoms, (2) get information, or (3) exit? ")
        if action == "1":
            assistant.ask_symptoms()
        elif action == "2":
            assistant.provide_information()
        elif action == "3":
            break
        else:
            print("Invalid option. Please try again.")