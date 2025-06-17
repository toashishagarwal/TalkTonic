import speech_recognition as sr
import pyttsx3
import os
import google.generativeai as genai
import threading
import time
import tkinter as tk
from tkinter import ttk, scrolledtext
from dotenv import load_dotenv
import customtkinter as ctk
from PIL import Image, ImageTk
import requests
from io import BytesIO

# Load environment variables from .env file
load_dotenv()

# Set up Gemini API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize speech components
recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed

# Set CustomTkinter appearance
ctk.set_appearance_mode("dark")  # Options: "dark", "light", "system"
ctk.set_default_color_theme("blue")  # Options: "blue", "green", "dark-blue"

class VoiceAssistantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Talk Tonic- Your AI Voice Assistant (Gemini)")
        self.root.geometry("800x600")
        self.root.minsize(650, 500)
        
        # Initialize Gemini model
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Initialize conversation history for Gemini
        self.chat = self.model.start_chat(history=[])
        
        # Create UI elements
        self.create_ui()
        
        # Flag for active listening
        self.listening = False
        self.stop_listening = False
        
        # Add a welcome message
        self.add_message("Hello! I'm your AI voice assistant powered by Gemini. Click the microphone to start speaking.", "assistant")
        
    def create_ui(self):
        # Main frame
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Configure grid layout
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=0)
        
        # Chat display area
        self.chat_frame = ctk.CTkFrame(self.main_frame)
        self.chat_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 5))
        
        # Configure chat frame layout
        self.chat_frame.grid_columnconfigure(0, weight=1)
        self.chat_frame.grid_rowconfigure(0, weight=1)
        
        # Chat display (scrollable)
        self.chat_display = ctk.CTkScrollableFrame(self.chat_frame)
        self.chat_display.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.chat_display.grid_columnconfigure(0, weight=1)
        
        # Control frame for buttons
        self.control_frame = ctk.CTkFrame(self.main_frame)
        self.control_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(5, 10))
        
        # Center the button in the control frame
        self.control_frame.grid_columnconfigure(0, weight=1)
        self.control_frame.grid_columnconfigure(1, weight=1)
        self.control_frame.grid_columnconfigure(2, weight=1)
        
        # Text input for typing messages
        self.text_input = ctk.CTkEntry(self.control_frame, placeholder_text="Type a message...", height=40)
        self.text_input.grid(row=0, column=0, sticky="ew", padx=(5, 5), pady=10)
        self.text_input.bind("<Return>", self.send_text_message)
        
        # Send button
        self.send_button = ctk.CTkButton(self.control_frame, text="Send", width=80, height=40, 
                                         command=self.send_text_message)
        self.send_button.grid(row=0, column=1, padx=5, pady=10)
        
        # Microphone button
        self.mic_button = ctk.CTkButton(self.control_frame, text="🎤", width=80, height=40, 
                                        font=("Arial", 20), command=self.toggle_listening)
        self.mic_button.grid(row=0, column=2, padx=(5, 5), pady=10)
        
        # Status indicator
        self.status_label = ctk.CTkLabel(self.main_frame, text="Ready", height=20)
        self.status_label.grid(row=2, column=0, sticky="ew", padx=10)
        
    def add_message(self, message, sender):
        """Add a message to the chat display."""
        # Create a frame for the message with the right alignment and color
        if sender == "user":
            msg_frame = ctk.CTkFrame(self.chat_display, fg_color="#1E88E5")  # Blue for user
            anchor = "e"  # East/right alignment
        else:
            msg_frame = ctk.CTkFrame(self.chat_display, fg_color="#424242")  # Gray for assistant
            anchor = "w"  # West/left alignment
        
        # Add the message to the frame
        msg_label = ctk.CTkLabel(msg_frame, text=message, wraplength=500, justify="left")
        msg_label.pack(padx=10, pady=8)
        
        # Add the frame to the chat display
        msg_frame.pack(fill="x", padx=10, pady=5, anchor=anchor)
        
        # Auto-scroll to the bottom of the chat
        self.chat_display._parent_canvas.yview_moveto(1.0)
    
    def toggle_listening(self):
        """Toggle the listening state."""
        if not self.listening:
            # Start listening
            self.listening = True
            self.stop_listening = False
            self.mic_button.configure(fg_color="#FF5252")  # Red when active
            self.status_label.configure(text="Listening...")
            
            # Start listening in a separate thread
            threading.Thread(target=self.listen_for_speech, daemon=True).start()
        else:
            # Stop listening
            self.stop_listening = True
            self.mic_button.configure(fg_color="#2196F3")  # Back to blue
            self.status_label.configure(text="Ready")
    
    def listen_for_speech(self):
        """Listen for speech input."""
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                
                while self.listening and not self.stop_listening:
                    try:
                        self.status_label.configure(text="Listening...")
                        audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                        
                        self.status_label.configure(text="Processing...")
                        user_input = recognizer.recognize_google(audio)
                        
                        if user_input:
                            # Update UI in the main thread
                            self.root.after(0, lambda: self.process_input(user_input))
                            break
                    except sr.WaitTimeoutError:
                        continue
                    except sr.UnknownValueError:
                        self.status_label.configure(text="Could not understand audio. Try again.")
                        time.sleep(1)
                    except sr.RequestError as e:
                        self.status_label.configure(text=f"Speech service error: {e}")
                        break
        
        finally:
            # Reset UI elements when done
            self.listening = False
            self.root.after(0, lambda: self.mic_button.configure(fg_color="#2196F3"))
            self.root.after(0, lambda: self.status_label.configure(text="Ready"))
    
    def send_text_message(self, event=None):
        """Send a message from the text input."""
        message = self.text_input.get().strip()
        if message:
            self.text_input.delete(0, tk.END)
            self.process_input(message)
    
    def process_input(self, user_input):
        """Process user input and generate a response."""
        # Add user message to chat
        self.add_message(user_input, "user")
        
        # Check for exit commands
        exit_commands = ["exit", "quit", "goodbye"]
        if any(cmd in user_input.lower() for cmd in exit_commands):
            response = "Goodbye! Have a great day."
            self.add_message(response, "assistant")
            # Speak response in a separate thread
            threading.Thread(target=self.speak_text, args=(response,), daemon=True).start()
            return
        
        # Update status
        self.status_label.configure(text="Thinking...")
        
        # Generate response in a separate thread
        threading.Thread(target=self.generate_and_speak_response, args=(user_input,), daemon=True).start()
    
    def generate_and_speak_response(self, user_input):
        """Generate a response using Gemini and speak it."""
        try:
            # Generate response
            response = self.generate_gemini_response(user_input)
            
            # Update UI in the main thread
            self.root.after(0, lambda: self.add_message(response, "assistant"))
            self.root.after(0, lambda: self.status_label.configure(text="Ready"))
            
            # Speak the response
            self.speak_text(response)
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.root.after(0, lambda: self.add_message(error_msg, "assistant"))
            self.root.after(0, lambda: self.status_label.configure(text="Error occurred"))
    
    def generate_gemini_response(self, input_text):
        """Generate a response using Gemini's API."""
        try:
            # Add system instruction for voice interaction
            prompt = f"""You are a helpful voice assistant. Keep your responses brief, conversational, and engaging. 
            Provide precise and succinct answers suitable for voice interaction. Keep responses under 100 words when possible.
            
            User message: {input_text}"""
            
            # Generate response using Gemini
            response = self.chat.send_message(prompt)
            
            return response.text
            
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            return "I'm having trouble connecting to my brain right now. Could you try again in a moment?"
    
    def speak_text(self, text):
        """Convert text to speech and play it."""
        engine.say(text)
        engine.runAndWait()


def check_dependencies():
    """Check for required dependencies and install if missing."""
    try:
        import customtkinter
    except ImportError:
        print("Installing required package: customtkinter")
        os.system("pip install customtkinter")
    
    try:
        from PIL import Image, ImageTk
    except ImportError:
        print("Installing required package: pillow")
        os.system("pip install pillow")
    
    try:
        import google.generativeai
    except ImportError:
        print("Installing required package: google-generativeai")
        os.system("pip install google-generativeai")
    
    try:
        from dotenv import load_dotenv
    except ImportError:
        print("Installing required package: python-dotenv")
        os.system("pip install python-dotenv")

def main():
    """Main function to run the voice assistant app."""
    # Check for dependencies first
    check_dependencies()
    
    # Verify API key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Warning: Gemini API key not found. Please set it as an environment variable.")
        api_key = input("Please enter your Gemini API key: ")
        genai.configure(api_key=api_key)
    
    # Initialize and run the GUI app
    root = ctk.CTk()
    app = VoiceAssistantApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
