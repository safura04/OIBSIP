
# Oasis Infobyte Internship - Python Task 1
# Voice Assistant - Beginner Level

import speech_recognition as sr
import subprocess
import time
import threading
import queue
import tkinter as tk
from datetime import datetime
import webbrowser


# -------------------- VOICE ASSISTANT SETUP --------------------

recognizer = sr.Recognizer()
microphone = sr.Microphone()
messages = queue.Queue()
is_listening = False
is_closing = False


def speak(text):
    messages.put(("assistant", text))

    command = [
        "powershell",
        "-NoProfile",
        "-Command",
        f'Add-Type -AssemblyName System.Speech; '
        f'$speak = New-Object System.Speech.Synthesis.SpeechSynthesizer; '
        f'$speak.Speak("{text.replace(chr(34), chr(39))}")'
    ]

    subprocess.run(
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    time.sleep(1)


def listen():
    try:
        with microphone as source:
            messages.put(("status", "Listening..."))
            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=5
            )

        messages.put(("status", "Processing..."))
        command = recognizer.recognize_google(audio).lower()
        messages.put(("user", command))
        return command

    except sr.WaitTimeoutError:
        messages.put(("status", "No speech detected. Try again."))
        return ""

    except sr.UnknownValueError:
        speak("Sorry, I couldn't understand that. Please try again.")
        return ""

    except sr.RequestError:
        messages.put(("status", "Speech recognition service unavailable."))
        return ""

    except Exception as error:
        messages.put(("status", f"Microphone error: {error}"))
        return ""


def process_command(command):
    if not command:
        return

    if "hello" in command or "hi" in command:
        speak("Hello! How can I help you?")

    elif "time" in command:
        current_time = datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}")

    elif "date" in command or "today" in command:
        current_date = datetime.now().strftime("%d %B %Y")
        speak(f"Today's date is {current_date}")

    elif "search" in command:
        search_query = (
            command.replace("search for", "")
            .replace("search", "")
            .strip()
        )

        if search_query:
            speak(f"Searching for {search_query}")
            webbrowser.open(
                "https://www.google.com/search?q="
                + search_query.replace(" ", "+")
            )
        else:
            speak("What would you like me to search for?")

    elif any(word in command.split() for word in ["bye", "exit", "quit"]):
        speak("Goodbye! Have a nice day.")
        messages.put(("close", ""))
        return

    else:
        speak("Sorry, I don't understand that command.")


# -------------------- GUI FUNCTIONS --------------------

def start_listening():
    global is_listening

    if is_listening or is_closing:
        return

    is_listening = True
    mic_button.config(state="disabled", text="🎙 Listening...")
    status_label.config(text="Listening... Speak now!")

    threading.Thread(
        target=voice_worker,
        daemon=True
    ).start()


def voice_worker():
    global is_listening

    try:
        command = listen()

        if command:
            process_command(command)

    except Exception as error:
        messages.put(("status", f"Error: {error}"))

    finally:
        messages.put(("ready", ""))


def add_message(sender, message):
    chat_box.config(state="normal")

    if sender == "user":
        chat_box.insert("end", f"\nYou: {message}\n", "user")
    else:
        chat_box.insert("end", f"\nAssistant: {message}\n", "assistant")

    chat_box.see("end")
    chat_box.config(state="disabled")


def check_messages():
    global is_listening, is_closing

    if is_closing:
        return

    try:
        while True:
            event, data = messages.get_nowait()

            if event in ("user", "assistant"):
                add_message(event, data)

            elif event == "status":
                status_label.config(text=data)

            elif event == "ready":
                is_listening = False
                mic_button.config(
                    state="normal",
                    text="🎙  Speak to Assistant"
                )
                status_label.config(text="Ready — click to speak")

            elif event == "close":
                close_app()
                return

    except queue.Empty:
        pass

    root.after(100, check_messages)


def close_app():
    global is_closing

    is_closing = True
    root.destroy()


# -------------------- GUI DESIGN --------------------

root = tk.Tk()
root.title("Voice Assistant")
root.geometry("620x650")
root.minsize(500, 550)
root.configure(bg="#111827")
root.protocol("WM_DELETE_WINDOW", close_app)

title_label = tk.Label(
    root,
    text="VOICE ASSISTANT",
    font=("Segoe UI", 23, "bold"),
    bg="#111827",
    fg="#2DD4BF"
)
title_label.pack(pady=(25, 5))

subtitle_label = tk.Label(
    root,
    text="Your personal desktop assistant",
    font=("Segoe UI", 11),
    bg="#111827",
    fg="#9CA3AF"
)
subtitle_label.pack(pady=(0, 20))

status_label = tk.Label(
    root,
    text="Calibrating microphone...",
    font=("Segoe UI", 11),
    bg="#111827",
    fg="#FBBF24"
)
status_label.pack(pady=5)

chat_box = tk.Text(
    root,
    height=15,
    width=60,
    bg="#1F2937",
    fg="#E5E7EB",
    font=("Segoe UI", 11),
    wrap="word",
    relief="flat",
    padx=15,
    pady=10,
    state="disabled"
)
chat_box.pack(fill="both", expand=True, padx=25, pady=15)

chat_box.tag_configure("user", foreground="#67E8F9")
chat_box.tag_configure("assistant", foreground="#6EE7B7")

mic_button = tk.Button(
    root,
    text="🎙  Speak to Assistant",
    command=start_listening,
    font=("Segoe UI", 12, "bold"),
    bg="#0D9488",
    fg="white",
    activebackground="#0F766E",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    padx=20,
    pady=12
)
mic_button.pack(pady=10)

exit_button = tk.Button(
    root,
    text="Exit",
    command=close_app,
    font=("Segoe UI", 10),
    bg="#374151",
    fg="white",
    activebackground="#4B5563",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    padx=25,
    pady=7
)
exit_button.pack(pady=(0, 20))


# -------------------- START APPLICATION --------------------

def calibrate_microphone():
    try:
        with microphone as source:
            recognizer.adjust_for_ambient_noise(
                source,
                duration=1
            )

        status_label.config(text="Ready — click to speak")
        status_label.config(fg="#6EE7B7")

    except Exception as error:
        status_label.config(text=f"Microphone error: {error}")
        mic_button.config(state="disabled")


root.after(100, check_messages)
root.after(100, lambda: threading.Thread(
    target=calibrate_microphone,
    daemon=True
).start())

root.mainloop()
