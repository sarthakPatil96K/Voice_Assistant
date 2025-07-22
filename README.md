# Voice Assistant

A mini-project developed by Paras Baliram Patil, Sarthak Jagdish Patil, Vaishnav Sharad Patil, and Nikhil Anil Pawar under the guidance of Prof. Priyanka Bhilare at Rajiv Gandhi Institute of Technology, Mumbai. This project showcases a Python-based desktop voice assistant that simplifies everyday tasks using speech recognition, text-to-speech, and integrated APIs.

---

## 🔍 Project Overview

This Voice Assistant utilizes Artificial Intelligence techniques to interact with users through voice commands. The assistant listens to the user, processes the command, and performs various tasks including:

- Providing weather updates
- Reading news
- Playing YouTube videos
- Searching Google or Wikipedia
- Opening/closing applications
- Sending WhatsApp messages
- Setting alarms
- Defining dictionary terms
- Casual chatting via HuggingFace chatbot

---

## 🧠 Technologies Used

### 🖥️ Backend
- **Python 3.8+**
- **Libraries:** 
  - `speech_recognition`
  - `pyttsx3`
  - `eel`
  - `requests`, `json`
  - `wikipedia`, `datetime`, `os`, `webbrowser`
  - `threading`

### 🌐 Frontend
- **HTML5**
- **CSS3**
- **JavaScript**
- **Eel** for Python–JS communication

---

## 🔧 Features

| Feature               | Description                                                                 |
|-----------------------|-----------------------------------------------------------------------------|
| Weather               | Real-time weather updates via OpenWeatherMap API                            |
| News                  | Fetch latest news using News API                                            |
| App Control           | Open/close installed applications via voice commands                        |
| Wikipedia Search      | Get summaries from Wikipedia                                                 |
| Google & YouTube      | Search and play results in browser                                           |
| Alarms & Reminders    | Set alarms via voice                                                        |
| Dictionary            | Define and explain words                                                     |
| WhatsApp Automation   | Send messages through voice input                                           |
| HuggingFace Chatbot   | Engage in basic conversation using integrated chatbot                        |

---

## 🏗️ Installation

1. **Clone the repository:**

```bash
git clone https://github.com/yourusername/voice-assistant.git
cd voice-assistant
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Set up your API keys** in the script where required (`weather`, `news`).

4. **Run the application:**

```bash
python main.py
```

> Make sure to have `index.html` and other frontend files in the correct folder for Eel to render.

---

## 📈 System Architecture

```
[User]
   ↓
[GUI (HTML/CSS)]
   ↓
[Speech Recognition ←→ Text Processing ←→ Text-to-Speech]
   ↓
[Command Execution (Local/API)]
   ↓
[Output Feedback to User]
```

---

## 🚀 Future Scope

- Improved NLP understanding
- Custom user profiles and preferences
- Offline voice command processing
- IoT device integration
- Enhanced UI and mobile compatibility

---

## 📚 References

- AI-Based Virtual Assistant Using Python – Academia.edu
- Intelligent Voice Assistant Using OpenCV Approach
- Communicative Voice Assistant Using Python & Visual Studio Code

---

## 🙌 Acknowledgment

Special thanks to Prof. Priyanka Bhilare and the faculty of Rajiv Gandhi Institute of Technology for continuous support and guidance throughout this project.

---

## 🧑‍💻 Authors

- Paras Baliram Patil
- Sarthak Jagdish Patil
- Vaishnav Sharad Patil
- Nikhil Anil Pawar
