import speech_recognition as sr
import pyttsx3
import os
import openai
from dotenv import load_dotenv

# Load environment variables from .env file (optional but recommended)
load_dotenv()

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    print("Warning: OpenAI API key not found. Please set it as an environment variable.")
    openai.api_key = input("Please enter your OpenAI API key: ")

# Initialize speech components
recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed

def listen():
    """Capture audio from microphone and convert to text."""
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

def speak(text):
    """Convert text to speech and play it."""
    print(f"Agent: {text}")
    engine.say(text)
    engine.runAndWait()

def generate_openai_response(input_text, conversation_history=None):
    """Generate a response using OpenAI's API."""
    if conversation_history is None:
        conversation_history = []
    
    # Format messages for the OpenAI API
    messages = [{"role": "system", "content": "You are a helpful voice assistant. Keep your responses brief, conversational, and engaging. Provide precise and succinct answers suitable for voice interaction."}]
    
    # Add conversation history
    for item in conversation_history:
        messages.append({"role": item["role"], "content": item["content"]})
    
    # Add the current user input
    messages.append({"role": "user", "content": input_text})
    
    try:
        # Call the OpenAI API
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",  # You can change to "gpt-4" if you have access
            messages=messages,
            max_tokens=100,
            temperature=0.7,
        )
        
        # Extract the assistant's reply
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return "I'm having trouble connecting to my brain right now. Could you try again in a moment?"

def main():
    """Main function to run the voice assistant."""
    speak("Hello, I'm your voice assistant powered by OpenAI. How can I help you?")
    
    conversation_history = []
    
    while True:
        user_input = listen()
        
        if not user_input:
            speak("I didn't catch that. Could you please repeat?")
            continue
            
        if "exit" in user_input.lower() or "quit" in user_input.lower() or "goodbye" in user_input.lower():
            speak("Goodbye! Have a great day.")
            break
        
        # Add user input to conversation history
        conversation_history.append({"role": "user", "content": user_input})
        
        # Keep conversation history limited to last 10 exchanges for context
        if len(conversation_history) > 20:  # Each exchange is 2 items (user + assistant)
            conversation_history = conversation_history[-20:]
        
        # Generate response using OpenAI
        response = generate_openai_response(user_input, conversation_history)
        
        # Add assistant response to conversation history
        conversation_history.append({"role": "assistant", "content": response})
        
        speak(response)

if __name__ == "__main__":
    main()