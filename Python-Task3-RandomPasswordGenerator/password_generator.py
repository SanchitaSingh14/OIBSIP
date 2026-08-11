import tkinter as tk
from tkinter import messagebox
import string
import secrets
import pyperclip


# Store only the last 5 generated passwords
password_history = []


def calculate_strength(password):
    score = 0

    # Length
    if len(password) >= 8:
        score += 1

    if len(password) >= 12:
        score += 1

    if len(password) >= 16:
        score += 1

    # Character diversity
    if any(char.islower() for char in password):
        score += 1

    if any(char.isupper() for char in password):
        score += 1

    if any(char.isdigit() for char in password):
        score += 1

    if any(char in string.punctuation for char in password):
        score += 1

    if score <= 3:
        return "Weak"

    elif score <= 5:
        return "Medium"

    else:
        return "Strong"


def copy_password():
    password = password_entry.get()

    if not password:
        messagebox.showwarning(
            "No Password",
            "Please generate a password first."
        )
        return

    pyperclip.copy(password)

    messagebox.showinfo(
        "Copied",
        "Password copied to clipboard!"
    )


def update_history():
    history_listbox.delete(0, tk.END)

    for index, password in enumerate(password_history, start=1):
        history_listbox.insert(
            tk.END,
            f"{index}. {password}"
        )


def generate_password():
    try:
        length = int(length_value.get())

        # Validate length
        if length < 8:
            messagebox.showerror(
                "Invalid Length",
                "Password length must be at least 8 characters."
            )
            return

        # Character sets
        selected_sets = []

        if uppercase_var.get():
            selected_sets.append(string.ascii_uppercase)

        if lowercase_var.get():
            selected_sets.append(string.ascii_lowercase)

        if numbers_var.get():
            selected_sets.append(string.digits)

        if symbols_var.get():
            selected_sets.append(string.punctuation)

        # At least two character types required
        if len(selected_sets) < 2:
            messagebox.showerror(
                "Invalid Selection",
                "Please select at least two character types."
            )
            return

        # Remove ambiguous characters if requested
        if ambiguous_var.get():
            ambiguous = "0Ol1"

            selected_sets = [
                "".join(
                    character
                    for character in character_set
                    if character not in ambiguous
                )
                for character_set in selected_sets
            ]

        # Generate at least one character from every selected type
        password_characters = [
            secrets.choice(character_set)
            for character_set in selected_sets
        ]

        # Create combined character pool
        combined_characters = "".join(selected_sets)

        # Fill remaining positions
        remaining_length = length - len(password_characters)

        for _ in range(remaining_length):
            password_characters.append(
                secrets.choice(combined_characters)
            )

        # Securely shuffle the password
        secrets.SystemRandom().shuffle(password_characters)

        password = "".join(password_characters)

        # Display password
        password_entry.delete(0, tk.END)
        password_entry.insert(0, password)

        # Calculate strength
        strength = calculate_strength(password)

        strength_label.config(
            text=f"Password Strength: {strength}"
        )

        # Automatically copy password
        pyperclip.copy(password)

        # Add password to session history
        password_history.insert(0, password)

        # Keep only the latest 5 passwords
        if len(password_history) > 5:
            password_history.pop()

        # Update history display
        update_history()

    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Please enter a valid password length."
        )


# Create main window
window = tk.Tk()
window.title("Secure Password Generator")
window.geometry("500x750")
window.resizable(False, False)


# Title
title_label = tk.Label(
    window,
    text="Secure Password Generator",
    font=("Arial", 22, "bold")
)
title_label.pack(pady=25)


# Password length
length_label = tk.Label(
    window,
    text="Password Length:",
    font=("Arial", 12)
)
length_label.pack()

length_value = tk.IntVar(value=12)

length_spinbox = tk.Spinbox(
    window,
    from_=8,
    to=64,
    textvariable=length_value,
    width=10,
    font=("Arial", 12)
)
length_spinbox.pack(pady=10)


# Character type heading
type_label = tk.Label(
    window,
    text="Character Types:",
    font=("Arial", 12, "bold")
)
type_label.pack(pady=(15, 5))


# Character type variables
uppercase_var = tk.BooleanVar(value=True)
lowercase_var = tk.BooleanVar(value=True)
numbers_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=True)


# Checkboxes
uppercase_check = tk.Checkbutton(
    window,
    text="Uppercase Letters (A-Z)",
    variable=uppercase_var,
    font=("Arial", 11)
)
uppercase_check.pack(anchor="w", padx=120)

lowercase_check = tk.Checkbutton(
    window,
    text="Lowercase Letters (a-z)",
    variable=lowercase_var,
    font=("Arial", 11)
)
lowercase_check.pack(anchor="w", padx=120)

numbers_check = tk.Checkbutton(
    window,
    text="Numbers (0-9)",
    variable=numbers_var,
    font=("Arial", 11)
)
numbers_check.pack(anchor="w", padx=120)

symbols_check = tk.Checkbutton(
    window,
    text="Symbols (!@#$...)",
    variable=symbols_var,
    font=("Arial", 11)
)
symbols_check.pack(anchor="w", padx=120)


# Exclude ambiguous characters
ambiguous_var = tk.BooleanVar(value=False)

ambiguous_check = tk.Checkbutton(
    window,
    text="Exclude ambiguous characters (0, O, l, 1)",
    variable=ambiguous_var,
    font=("Arial", 11)
)
ambiguous_check.pack(pady=15)


# Password display
password_label = tk.Label(
    window,
    text="Generated Password:",
    font=("Arial", 12, "bold")
)
password_label.pack(pady=(10, 5))

password_entry = tk.Entry(
    window,
    font=("Arial", 12),
    width=38
)
password_entry.pack(pady=5)


# Password strength
strength_label = tk.Label(
    window,
    text="Password Strength: -",
    font=("Arial", 12, "bold")
)
strength_label.pack(pady=5)


# Generate button
generate_button = tk.Button(
    window,
    text="Generate Password",
    font=("Arial", 12, "bold"),
    width=22,
    command=generate_password
)
generate_button.pack(pady=15)


# Copy button
copy_button = tk.Button(
    window,
    text="Copy to Clipboard",
    font=("Arial", 11),
    width=22,
    command=copy_password
)
copy_button.pack(pady=5)


# Generation history
history_label = tk.Label(
    window,
    text="Recent Passwords (Last 5)",
    font=("Arial", 12, "bold")
)
history_label.pack(pady=(20, 5))

history_listbox = tk.Listbox(
    window,
    width=42,
    height=5,
    font=("Courier", 10)
)
history_listbox.pack(pady=5)


# Start application
window.mainloop()