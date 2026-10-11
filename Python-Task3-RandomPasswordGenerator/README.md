# Random Password Generator

**Oasis Infobyte Internship — Python Programming**  
**Task 3: Random Password Generator | Advanced Level**

## Project Overview

The Random Password Generator is a Python-based GUI application that generates secure, customizable passwords. Users can choose password length and character types, check password strength, and copy passwords to the clipboard.

## Features

- Generate secure random passwords using Python's `secrets` module.
- Customize password length from 8 to 64 characters.
- Select uppercase letters, lowercase letters, numbers, and symbols.
- Exclude ambiguous characters such as `0`, `O`, `1`, `l`, and `I`.
- Display password strength as Weak, Medium, or Strong.
- Automatically copy generated passwords to the clipboard.
- Copy passwords manually using the Copy to Clipboard button.
- Display the five most recently generated passwords during the current session.
- Keep password history in memory without saving it to a file.
- Provide a graphical interface using Tkinter.

## Technologies Used

- Python 3.13
- Tkinter
- Secrets
- String
- Pyperclip

## Installation

1. Install Python 3.
2. Install the required dependency:

   ```bash
   python -m pip install pyperclip
   ```

## How to Run

Open the terminal in the project folder and execute:

```bash
python password_generator.py
```

The application window will open. Choose your desired password length and character types, then click **Generate Password**.

## Project Structure

```text
Python-Task3-RandomPasswordGenerator/
├── password_generator.py
├── README.md
└── screenshots/
```

The `screenshots` folder is optional; add it when you have captured screenshots of the application.

## Learning Outcomes

- Secure random password generation.
- GUI development using Tkinter.
- Character-set manipulation.
- Clipboard integration.
- Input validation and basic password strength evaluation.

## Acknowledgement

This project was developed as part of the Oasis Infobyte Python Programming Internship.
