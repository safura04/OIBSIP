# Random Password Generator

## Oasis Infobyte Internship – Python Task 3

A secure Random Password Generator developed using Python as part of the Oasis Infobyte Internship. This application provides a graphical user interface (GUI) that allows users to generate strong random passwords based on their preferred length and character types.

## Features

- Generate secure random passwords.
- Customize password length from 8 to 64 characters.
- Choose uppercase letters, lowercase letters, numbers, and symbols.
- Exclude ambiguous characters such as `0`, `O`, `1`, `l`, and `I`.
- Display password strength as Weak, Medium, or Strong.
- Copy generated passwords to the clipboard.
- View the five most recently generated passwords during the session.
- Keep password history temporary without saving it to a file.

## Technologies Used

- Python 3.13
- Tkinter – Graphical User Interface
- Secrets – Secure random password generation
- String – Character sets
- Pyperclip – Clipboard functionality

## Installation

1. Install Python 3.13 or a compatible Python 3 version.
2. Install the required dependency:

   ```bash
   pip install pyperclip
   ```

3. Download or clone the repository.
4. Open the project folder in VS Code.

## How to Run

Execute the following command in the terminal:

```bash
python password_generator.py
```

The Password Generator window will open. Select your desired password length and character types, then click **Generate Password**.

## Project Structure

```text
Python-Task3-RandomPasswordGenerator/
│
├── password_generator.py
└── README.md
```

## Learning Outcomes

- Understanding secure random number generation using Python's `secrets` module.
- Building graphical interfaces using Tkinter.
- Working with strings and character sets.
- Implementing clipboard functionality.
- Applying input validation and basic password strength evaluation.

## Acknowledgement

This project was developed as part of the Python Programming Internship at Oasis Infobyte.

