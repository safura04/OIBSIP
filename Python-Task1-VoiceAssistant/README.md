
# Python Voice Assistant

## Oasis Infobyte Internship – Python Task 1

**Level: Beginner**

A Python-based voice assistant developed as part of the Oasis Infobyte Internship. This project combines speech recognition, voice responses, web search, and a graphical user interface (GUI).

The application allows users to interact with the assistant through spoken commands using a desktop window.

## Features

- Voice input through the microphone
- Responds to greetings such as "Hello" and "Hi"
- Provides the current time and date
- Performs Google searches using voice commands
- Provides spoken responses
- Displays user commands and assistant responses in the GUI
- Shows listening and processing status
- Uses background threading to keep the GUI responsive
- Handles unrecognized speech and microphone errors
- Supports exit commands such as "Bye", "Exit", and "Quit"

## Technologies Used

- Python
- Tkinter for the graphical user interface
- SpeechRecognition for speech-to-text
- PyAudio for microphone input
- Windows Speech Synthesizer for text-to-speech
- Google Speech Recognition
- datetime module
- webbrowser module
- threading and queue modules

## Project Structure

```text
Python-Task1-VoiceAssistant/
├── assistant.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Requirements

- Windows operating system
- Python 3.13 recommended for this project
- Working microphone
- Internet connection for speech recognition and Google searches
- Required Python packages listed in `requirements.txt`

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/safura04/OIBSIP.git
```

### 2. Open the Project Folder

```bash
cd OIBSIP/Python-Task1-VoiceAssistant
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

For Windows Git Bash:

```bash
source venv/Scripts/activate
```

For Windows Command Prompt:

```cmd
venv\Scripts\activate
```

### 5. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 6. Run the Application

```bash
python assistant.py
```

## How to Use

1. Launch the application.
2. Click the **Speak to Assistant** button.
3. Speak a supported command when the assistant is listening.
4. View your command and the assistant's response in the conversation area.
5. Click the microphone button again to give another command.
6. Click **Exit** or say "Exit" to close the application.

## Example Commands

| Voice command | Expected action |
|---|---|
| Hello | Responds with a greeting |
| What is the time? | Announces the current time |
| What is today's date? | Announces the current date |
| Search for Python tutorials | Opens a Google search |
| Exit | Says goodbye and closes the application |

## How It Works

1. The user clicks the microphone button.
2. The microphone captures the spoken command.
3. SpeechRecognition converts the speech into text.
4. The program identifies the command and performs the corresponding action.
5. The assistant displays its response and speaks it using the Windows Speech Synthesizer.
6. Background threading helps keep the graphical interface responsive during listening.

## Error Handling

The application handles situations such as:

- No speech detected
- Unrecognized speech
- Speech recognition service errors
- Microphone errors

## Privacy

The application uses Google Speech Recognition to process voice input, which requires sending audio to an online service. Avoid speaking passwords, financial information, or other sensitive information while using the application.

## Internship Details

- **Organization:** Oasis Infobyte
- **Track:** Python Programming
- **Task:** Task 1 – Voice Assistant
- **Level:** Beginner

## Author

**Safura Mulla**

Oasis Infobyte Internship – Python Programming
