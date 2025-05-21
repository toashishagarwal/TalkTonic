# TalkTonic

![TalkTonic Banner](/img/banner5.png)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![OpenAI](https://img.shields.io/badge/AI-OpenAI-brightgreen.svg)](https://openai.com/)

**TalkTonic** is a sleek, modern AI voice assistant that combines the power of OpenAI's language models with an intuitive, beautiful user interface. Talk or type your questions and get intelligent responses through both text and speech.

## 🌟 Features

- **Conversational AI**: Powered by OpenAI's GPT models
- **Voice Recognition**: Speak naturally and get voice responses
- **Beautiful UI**: Modern dark-themed interface with a chat-like experience
- **Dual Input**: Use your voice or type your messages
- **Conversation Memory**: Assistant remembers context for natural conversations
- **Cross-Platform**: Works on Windows, macOS, and Linux

## 🖼️ Screenshots

![TalkTonic Screenshot](https://github.com/toashishagarwal/TalkTonic/blob/main/demo.gif)

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- OpenAI API key

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/talktonic.git
cd talktonic
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Set up your OpenAI API key**

Create a `.env` file in the project root directory:

```
OPENAI_API_KEY=your_openai_api_key_here
```

Alternatively, you can set it as an environment variable or enter it when prompted during startup.

### Running TalkTonic

```bash
python appLLMUI.py
```

## 💬 How to Use

1. **Start TalkTonic**: Run the application using the command above
2. **Voice Interaction**:
   - Click the microphone button (🎤)
   - Speak your query or command
   - Listen to the AI response
3. **Text Interaction**:
   - Type your message in the text field
   - Press Enter or click the Send button
   - Read the AI response in the chat
4. **Exit**: Say "goodbye" or close the application window

## 🛠️ Technical Details

TalkTonic integrates several powerful technologies:

- **Speech Recognition**: Uses Google's speech recognition API
- **Text-to-Speech**: Powered by pyttsx3 for offline voice synthesis
- **AI Language Model**: OpenAI's GPT models (default: gpt-3.5-turbo)
- **UI Framework**: CustomTkinter for a modern look and feel
- **Multithreading**: Background processing for a responsive UI

## 📋 Requirements

See the [requirements.txt](requirements.txt) file for a complete list of dependencies:

```
SpeechRecognition
pyttsx3
openai
python-dotenv
customtkinter
pillow
```

## 🔮 Future Plans

- Offline speech recognition option
- Custom voice selection
- Conversation saving and loading
- Theme customization
- Plugin system for extended capabilities

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- [OpenAI](https://openai.com/) for their powerful language models
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) for the modern UI components
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) for the speech recognition capabilities
- All contributors and supporters of this project

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/toashishagarwal">Ashish Agarwal</a>
</p>