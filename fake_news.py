import re
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline

# Sample dataset (text and labels)
data = [
    ("You have won a prize! Click here to claim.", 1),  # 1 indicates fake
    ("Safaricom is giving away free data!", 1),
    ("The weather is nice today.", 0),  # 0 indicates real
    ("Urgent: Your account has been compromised!", 1),
    ("Join us for a community meeting this Saturday.", 0),
    ("Act now to receive your cash reward!", 1),
    ("Healthy eating is important for your well-being.", 0),
]

# Split the dataset into texts and labels
texts, labels = zip(*data)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.2, random_state=42)

# Create a pipeline with TF-IDF vectorization and Random Forest classifier
model = make_pipeline(TfidfVectorizer(), RandomForestClassifier())

# Train the model
model.fit(X_train, y_train)

def is_suspicious(message):
    # Check for common signs of scams or fake news
    suspicious_phrases = [
        "you have won", "click here", "urgent", "too good to be true",
        "act now", "limited time", "fake endorsement", "M-Pesa fraud"
    ]
    
    # Check for urgency traps and manipulative language
    if any(phrase in message.lower() for phrase in suspicious_phrases):
        return True, "Contains suspicious phrases."

    # Check for poor grammar or spelling
    if not re.match(r'^[A-Z].*[.!?]$', message):  # Simple check for sentence structure
        return True, "Poor grammar or structure detected."

    # Predict using the trained model
    prediction = model.predict([message])

    if prediction[0] == 1:  # Assuming 1 indicates fake news/scam
        return True, "Detected as fake news or scam."

    return False, "Message appears to be legitimate."

# Example usage
user_message = "You have won a prize! Click here to claim."
is_fake, reason = is_suspicious(user_message)
print(f"Is the message suspicious? {is_fake}. Reason: {reason}")

# Test another message
user_message2 = "Join us for a community meeting this Saturday."
is_fake2, reason2 = is_suspicious(user_message2)
print(f"Is the message suspicious? {is_fake2}. Reason: {reason2}")