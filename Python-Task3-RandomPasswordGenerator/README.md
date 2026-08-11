# Secure Random Password Generator

A Python-based secure password generator with a Tkinter graphical user interface. The application generates strong passwords using Python's cryptographically secure `secrets` module and provides password strength analysis, clipboard integration, ambiguous-character exclusion, and session-only password history.

## Features

- User-friendly Tkinter GUI
- Password length control from 8 to 64 characters
- Uppercase letters
- Lowercase letters
- Numbers
- Symbols
- Requires at least two character types
- Uses Python's `secrets` module for secure password generation
- Guarantees at least one character from every selected type
- Weak / Medium / Strong password strength indicator
- Automatic clipboard copying after password generation
- Manual "Copy to Clipboard" button
- Option to exclude ambiguous characters:
  - `0`
  - `O`
  - `l`
  - `1`
- Displays the last 5 generated passwords during the current session
- Password history is not stored in a file or database
- Input validation and error handling

## Technologies Used

- Python
- Tkinter
- secrets
- string
- pyperclip

## Security

The application uses Python's `secrets` module instead of the `random` module because `secrets` is designed for generating cryptographically secure random values.

Each generated password contains at least one character from every selected character category.

Password history is kept only in memory during the current application session and is not persisted to disk.

## Project Structure

```text
Python-Task3-RandomPasswordGenerator/
│
├── password_generator.py
├── requirements.txt
├── README.md
└── .gitignore