# 🎙️ Python Voice Assistant

### Oasis Infobyte Internship | Python Programming | Task 1

A beginner-level **Python Voice Assistant** developed as part of the **Oasis Infobyte Python Programming Internship**.

The project allows users to interact with a computer using spoken commands. It captures voice input through a microphone, converts speech into text, processes the command, performs the requested action, and provides a spoken response.

---

## 📌 Project Overview

The Voice Assistant is a Python-based desktop assistant designed to demonstrate fundamental concepts of:

- Speech recognition
- Voice-based interaction
- Text-to-speech
- Command processing
- Date and time handling
- Web browser automation
- Exception handling
- Python virtual environments
- External package management

The assistant continuously listens for commands until the user asks it to exit.

---

## ✨ Features

### 🎤 1. Voice Input

The assistant captures spoken commands using the system microphone.

Speech is converted into text using the `SpeechRecognition` library and Google's speech recognition service.

---

### 👋 2. Greeting Recognition

The assistant recognizes common greetings such as:

```text
Hello
Hi
```

Example:

```text
User: Hello

Assistant: Hello! How can I help you?
```

---

### 🕐 3. Current Time

The assistant can provide the current system time.

Example:

```text
User: What is the time?

Assistant: The current time is 10:30 PM
```

The time is obtained using Python's built-in `datetime` module.

---

### 📅 4. Current Date

The assistant can provide the current date.

Example:

```text
User: What is today's date?

Assistant: Today's date is 25 September 2026
```

The date is generated dynamically using Python's `datetime` module.

---

### 🌐 5. Voice-Based Web Search

The assistant can perform a Google search based on a spoken topic.

Example:

```text
User: Search for Python tutorials
```

The assistant:

1. Extracts the search topic.
2. Announces that it is searching.
3. Opens Google in the default web browser.
4. Displays the search results.

---

### 🔊 6. Text-to-Speech Feedback

The assistant provides spoken responses instead of relying only on terminal output.

The final implementation uses the **Windows Speech Synthesizer** through PowerShell.

This approach was selected to provide stable voice feedback while maintaining reliable repeated microphone input on Windows.

---

### 🛡️ 7. Error Handling

The assistant handles common problems gracefully, including:

- No speech detected
- Speech that cannot be understood
- Speech recognition service errors
- Unexpected microphone errors

The program does not terminate simply because one voice command fails.

---

### 🚪 8. Exit Commands

The assistant can be stopped using:

```text
Bye
Exit
Quit
```

Example:

```text
User: Exit

Assistant: Goodbye! Have a nice day.
```

---

# 🧰 Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| SpeechRecognition | Converts spoken input into text |
| PyAudio | Provides microphone/audio input |
| Windows Speech Synthesizer | Converts responses into speech |
| datetime | Provides current date and time |
| webbrowser | Opens Google search results |
| subprocess | Communicates with Windows PowerShell |
| time | Controls timing between operations |

---

# 🏗️ Project Architecture

The application follows a simple voice-processing pipeline:

```text
                 ┌──────────────────┐
                 │      User        │
                 │  Speaks Command  │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │    Microphone    │
                 └────────┬─────────┘
                          │
                          ▼
              ┌────────────────────────┐
              │   SpeechRecognition    │
              │     Speech → Text      │
              └───────────┬────────────┘
                          │
                          ▼
                ┌────────────────────┐
                │ Command Processing │
                └─────────┬──────────┘
                          │
          ┌───────────────┼────────────────┐
          │               │                │
          ▼               ▼                ▼
      Time/Date       Web Search       Greeting
          │               │                │
          └───────────────┼────────────────┘
                          │
                          ▼
                ┌────────────────────┐
                │  Response Engine   │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │ Windows Speech     │
                │ Synthesizer (TTS)  │
                └─────────┬──────────┘
                          │
                          ▼
                    🔊 Voice Output
```

---

# 📁 Project Structure

```text
Python-Task1-VoiceAssistant/
│
├── assistant.py
│       └── Main Voice Assistant application
│
├── requirements.txt
│       └── Python package dependencies
│
├── README.md
│       └── Project documentation
│
├── .gitignore
│       └── Files and folders excluded from Git
│
└── venv/
        └── Local Python virtual environment
```

> The `venv/` directory is used locally and is excluded from GitHub using `.gitignore`.

---

# ⚙️ How the Application Works

The application follows the following process:

### Step 1: Microphone Calibration

When the program starts, the microphone is calibrated to account for ambient background noise.

```python
recognizer.adjust_for_ambient_noise(source, duration=1)
```

This helps improve speech recognition in different environments.

---

### Step 2: Capture Voice

The assistant waits for the user to speak.

```python
audio = recognizer.listen(
    source,
    timeout=5,
    phrase_time_limit=5
)
```

The assistant waits for speech and limits the maximum duration of a command.

---

### Step 3: Speech-to-Text

The recorded audio is sent to the speech recognition service:

```python
text = recognizer.recognize_google(audio)
```

The spoken command is converted into text.

For example:

```text
"What is the time?"
```

becomes:

```text
"what is the time"
```

---

### Step 4: Command Processing

The recognized text is converted to lowercase and checked against predefined commands.

For example:

```python
elif "time" in command:
```

If the command contains `"time"`, the assistant generates the current time.

---

### Step 5: Perform the Requested Action

Depending on the command, the assistant can:

- Respond to greetings
- Tell the time
- Tell the date
- Search Google
- Exit the application

---

### Step 6: Voice Response

The generated response is passed to the Windows Speech Synthesizer.

The user therefore receives an audible response rather than only terminal output.

---

# 💻 Installation and Setup

## Prerequisites

Before running the project, make sure the system has:

- Windows operating system
- Python 3.13 or compatible Python 3.x version
- Working microphone
- Internet connection
- Git
- VS Code or another Python IDE

---

## 1. Clone the Repository

Clone the main OIBSIP repository:

```bash
git clone https://github.com/safura04/OIBSIP.git
```

---

## 2. Open the Repository

Move into the repository:

```bash
cd OIBSIP
```

Then open the Voice Assistant project:

```bash
cd Python-Task1-VoiceAssistant
```

---

## 3. Create a Virtual Environment

Create a separate Python environment for this project:

```bash
python -m venv venv
```

A virtual environment keeps project dependencies isolated from other Python projects.

---

## 4. Activate the Virtual Environment

### Windows Git Bash

```bash
source venv/Scripts/activate
```

### Windows Command Prompt

```cmd
venv\Scripts\activate
```

After activation, the terminal should show:

```text
(venv)
```

---

## 5. Install Dependencies

Install all required external packages:

```bash
pip install -r requirements.txt
```

The dependencies are defined in:

```text
requirements.txt
```

---

## 6. Run the Application

Start the assistant with:

```bash
python assistant.py
```

The application will first calibrate the microphone and then begin listening for commands.

You should see:

```text
Calibrating microphone...
Listening...
```

---

# 🎮 Usage

Once the program displays:

```text
Listening...
```

speak a supported command.

### Greeting

```text
Hello
```

### Time

```text
What is the time?
```

### Date

```text
What is today's date?
```

### Google Search

```text
Search for Python tutorials
```

or:

```text
Search for artificial intelligence
```

### Exit

```text
Exit
```

You can also use:

```text
Bye
```

or:

```text
Quit
```

---

# 🧪 Example Interaction

```text
Calibrating microphone...

Listening...
You said: hello

Assistant:
Hello! How can I help you?

Listening...
You said: what is the time

Assistant:
The current time is 10:30 PM

Listening...
You said: what is today's date

Assistant:
Today's date is 25 September 2026

Listening...
You said: search for Python tutorials

Assistant:
Searching for Python tutorials

[Google search opens in the default browser]

Listening...
You said: exit

Assistant:
Goodbye! Have a nice day.
```

---

# 🛡️ Error Handling

The application includes exception handling for several possible situations.

### No Speech Detected

If the user does not speak within the listening period, the application continues running instead of crashing.

---

### Unrecognized Speech

If speech is detected but cannot be understood, the assistant responds:

```text
Sorry, I couldn't understand that. Please try again.
```

---

### Speech Recognition Service Error

If the speech recognition service cannot be reached, the application handles the error instead of terminating unexpectedly.

---

### Microphone Errors

Unexpected microphone-related errors are caught using exception handling.

---

# 🔐 Privacy Considerations

The application uses the microphone to capture spoken commands.

Speech recognition is performed using Google's speech recognition service through the `SpeechRecognition` library.

The application does not intentionally store voice recordings, user commands, passwords, or personal information.

Web searches are opened in the user's default browser when a search command is given.

Users should understand that spoken audio processed through an external speech recognition service may be subject to that service's own policies.

---

# 📦 Dependencies

The project uses the following external Python packages:

```text
SpeechRecognition==3.17.0
PyAudio==0.2.14
```

Python standard-library modules used by the project include:

```text
datetime
webbrowser
subprocess
time
```

These standard-library modules do not require separate installation.

---

# 🧹 Git and Project Hygiene

The project contains a `.gitignore` file to prevent unnecessary local files from being uploaded to GitHub.

The following types of files are excluded:

```text
venv/
__pycache__/
*.pyc
*.pyo
.vscode/
.env
```

The local virtual environment is therefore not included in the public repository.

---

# 🚀 Future Improvements

The current implementation focuses on the **Beginner Level requirements** of the Oasis Infobyte task.

Possible future enhancements include:

- Natural language intent recognition
- Weather API integration
- Email sending through voice commands
- Voice-controlled reminders
- General knowledge question answering
- Custom user commands
- More advanced conversational interaction
- Support for additional languages
- GUI-based interface
- Smart-home integrations

These features are outside the scope of the current Beginner Level implementation.

---

# 🎓 Internship Information

**Organization:** Oasis Infobyte

**Internship Track:** Python Programming

**Task:** Task 1 – Voice Assistant

**Level:** Beginner

**Project Type:** Python Voice Assistant

---

# 👨‍💻 Author

**Safura Mulla**

Python Programming Intern  
Oasis Infobyte Internship

---

# 📜 License

This project was developed as part of an internship assignment for educational and demonstration purposes.