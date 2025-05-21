import speech_recognition as sr

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand that.")
        return ""
    except sr.RequestError:
        print("Speech service is unavailable.")
        return ""

from transformers import pipeline

# Initialize NLU pipeline
nlu_pipeline = pipeline(
    "text-classification", 
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

def understand(text):
    # For a real agent, you would use a more sophisticated approach
    # This is a simple intent classification example
    if not text:
        return {"intent": "unknown", "confidence": 0}
    
    # Check for basic intents
    if "weather" in text.lower():
        return {"intent": "get_weather", "confidence": 0.9}
    elif "time" in text.lower():
        return {"intent": "get_time", "confidence": 0.9}
    elif "hello" in text.lower() or "hi" in text.lower():
        return {"intent": "greeting", "confidence": 0.9}
    elif "bye" in text.lower():
        return {"intent": "farewell", "confidence": 0.9}
    
    # Use transformer model for more complex inputs
    result = nlu_pipeline(text)
    return {"intent": "general", "sentiment": result[0]["label"], "confidence": result[0]["score"]}

import datetime

def generate_response(intent_data):
    intent = intent_data["intent"]
    
    if intent == "greeting":
        return "Hello! How can I help you today?"
    elif intent == "farewell":
        return "Goodbye! Have a great day!"
    elif intent == "get_time":
        current_time = datetime.datetime.now().strftime("%H:%M")
        return f"The current time is {current_time}."
    elif intent == "get_weather":
        # In a real app, you would integrate with a weather API
        return "I'm sorry, I don't have access to weather information yet."
    elif intent == "unknown":
        return "I didn't catch that. Could you repeat?"
    else:
        if intent_data.get("sentiment") == "POSITIVE":
            return "I'm glad to hear that! Is there anything I can help you with?"
        else:
            return "I understand. Is there anything specific you'd like to know?"

import pyttsx3

def speak(text):
    engine = pyttsx3.init()
    # Optional: customize voice
    # voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Female voice
    engine.setProperty('rate', 150)  # Speed
    print(f"Agent: {text}")
    engine.say(text)
    engine.runAndWait()


def main():
    speak("Hello, I'm your voice assistant. How can I help you?")
    
    while True:
        user_input = listen()
        if "exit" in user_input.lower() or "quit" in user_input.lower():
            speak("Goodbye!")
            break
            
        intent_data = understand(user_input)
        response = generate_response(intent_data)
        speak(response)

if __name__ == "__main__":
    main()