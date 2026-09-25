# Oasis Infobyte Internship - Python Task 1
# Voice Assistant
# Beginner Level 
import speech_recognition as sr
import subprocess
import time
from datetime import datetime
import webbrowser

recognizer = sr.Recognizer()
microphone = sr.Microphone()

with microphone as source:
    print("Calibrating microphone...")
    recognizer.adjust_for_ambient_noise(source, duration=1)

def speak(text):
    command = [
        "powershell",
        "-NoProfile",
        "-Command",
        f'Add-Type -AssemblyName System.Speech; '
        f'$speak = New-Object System.Speech.Synthesis.SpeechSynthesizer; '
        f'$speak.Speak("{text.replace(chr(34), chr(39))}")'
    ]

    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1)

def listen():
    try:
        with microphone as source:
            print("Listening...")
            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=5
            )

        print("Processing...")

        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text.lower()

    except sr.WaitTimeoutError:
        print("No speech detected.")
        return ""

    except sr.UnknownValueError:
        speak("Sorry, I couldn't understand that. Please try again.")
        return ""

    except sr.RequestError:
        print("Speech recognition service is unavailable.")
        return ""

    except Exception as e:
        print("Microphone error:", e)
        return ""

    
while True:
    command = listen()

    if command == "":
        continue

    if "hello" in command or "hi" in command:
        speak("Hello! How can I help you?")

    elif "time" in command:
        current_time = datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}")

    elif "date" in command or "today" in command:
        current_date = datetime.now().strftime("%d %B %Y")
        speak(f"Today's date is {current_date}")

    elif "search" in command:
        search_query = command.replace("search for", "").replace("search", "").strip()

        if search_query:
            speak(f"Searching for {search_query}")
            webbrowser.open(
                "https://www.google.com/search?q="
                + search_query.replace(" ", "+")
            )
        else:
            speak("What would you like me to search for?")

    elif "bye" in command or "exit" in command or "quit" in command:
        speak("Goodbye! Have a nice day.")
        break

    else:
        speak("Sorry, I don't understand that command.")