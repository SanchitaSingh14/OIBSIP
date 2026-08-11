import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Initialize database
def initialize_database():
    try:
        connection = sqlite3.connect("bmi_records.db")
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bmi_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                weight REAL NOT NULL,
                height REAL NOT NULL,
                bmi REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL
            )
        """)

        connection.commit()
        connection.close()

    except sqlite3.Error as error:
        messagebox.showerror(
            "Database Error",
            f"Could not initialize database:\n{error}"
        )


# Calculate BMI
def calculate_bmi():
    try:
        name = name_entry.get().strip()
        weight = float(weight_entry.get())
        height = float(height_entry.get())

        # Validate name
        if not name:
            messagebox.showerror(
                "Input Error",
                "Please enter your name."
            )
            return

        # Validate weight
        if weight <= 0:
            messagebox.showerror(
                "Input Error",
                "Weight must be greater than zero."
            )
            return

        # Validate height
        if height <= 0:
            messagebox.showerror(
                "Input Error",
                "Height must be greater than zero."
            )
            return

        # Calculate BMI
        bmi = weight / (height ** 2)

        # Classify BMI
        if bmi < 18.5:
            category = "Underweight"
            result_color = "orange"
        elif bmi < 25:
            category = "Normal"
            result_color = "green"
        elif bmi < 30:
            category = "Overweight"
            result_color = "orange"
        else:
            category = "Obese"
            result_color = "red"

        # Save record to database
        try:
            connection = sqlite3.connect("bmi_records.db")
            cursor = connection.cursor()

            current_date = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            cursor.execute("""
                INSERT INTO bmi_records
                (name, weight, height, bmi, category, date)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                name,
                weight,
                height,
                bmi,
                category,
                current_date
            ))

            connection.commit()
            connection.close()

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                f"Could not save BMI record:\n{error}"
            )
            return

        # Display result
        result_label.config(
            text=f"{name}'s BMI: {bmi:.2f}\nCategory: {category}",
            fg=result_color
        )

    except ValueError:
        messagebox.showerror(
            "Input Error",
            "Please enter valid numeric values for weight and height."
        )

def view_history():
    try:
        connection = sqlite3.connect("bmi_records.db")
        cursor = connection.cursor()

        cursor.execute("""
            SELECT name, weight, height, bmi, category, date
            FROM bmi_records
            ORDER BY date DESC
        """)

        records = cursor.fetchall()
        connection.close()

        # Create history window
        history_window = tk.Toplevel(window)
        history_window.title("BMI History")
        history_window.geometry("750x450")

        title = tk.Label(
            history_window,
            text="BMI History",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=15)

        if not records:
            no_records = tk.Label(
                history_window,
                text="No BMI records found.",
                font=("Arial", 12)
            )
            no_records.pack(pady=20)
            return

        # Header
        header = tk.Label(
            history_window,
            text="Name     Weight     Height     BMI     Category     Date",
            font=("Arial", 11, "bold")
        )
        header.pack(pady=5)

        # Display records
        for record in records:
            name, weight, height, bmi, category, date = record

            record_text = (
                f"{name}     "
                f"{weight:.1f} kg     "
                f"{height:.2f} m     "
                f"{bmi:.2f}     "
                f"{category}     "
                f"{date}"
            )

            record_label = tk.Label(
                history_window,
                text=record_text,
                font=("Arial", 10)
            )
            record_label.pack(anchor="w", padx=20, pady=3)

    except sqlite3.Error as error:
        messagebox.showerror(
            "Database Error",
            f"Could not read BMI history:\n{error}"
        )
def view_trend():
    try:
        name = name_entry.get().strip()

        if not name:
            messagebox.showerror(
                "Input Error",
                "Please enter a user's name first."
            )
            return

        connection = sqlite3.connect("bmi_records.db")
        cursor = connection.cursor()

        cursor.execute("""
            SELECT date, bmi
            FROM bmi_records
            WHERE name = ?
            ORDER BY date ASC
        """, (name,))

        records = cursor.fetchall()
        connection.close()

        if not records:
            messagebox.showinfo(
                "No Records",
                f"No BMI records found for {name}."
            )
            return

        dates = [record[0] for record in records]
        bmi_values = [record[1] for record in records]

        # Create graph window
        graph_window = tk.Toplevel(window)
        graph_window.title(f"{name}'s BMI Trend")
        graph_window.geometry("800x600")

        # Create matplotlib figure
        figure, axis = plt.subplots(figsize=(8, 5))

        axis.plot(
            dates,
            bmi_values,
            marker="o"
        )

        axis.set_title(f"{name}'s BMI Trend")
        axis.set_xlabel("Date")
        axis.set_ylabel("BMI")

        axis.axhline(
            y=18.5,
            linestyle="--",
            label="Underweight Limit"
        )

        axis.axhline(
            y=25,
            linestyle="--",
            label="Normal Limit"
        )

        axis.axhline(
            y=30,
            linestyle="--",
            label="Obese Limit"
        )

        axis.legend()
        axis.grid(True)
        figure.autofmt_xdate()

        # Display graph inside Tkinter
        canvas = FigureCanvasTkAgg(
            figure,
            master=graph_window
        )

        canvas.draw()
        canvas.get_tk_widget().pack(
            fill=tk.BOTH,
            expand=True
        )

    except sqlite3.Error as error:
        messagebox.showerror(
            "Database Error",
            f"Could not load BMI trend:\n{error}"
        )

# Create main window
window = tk.Tk()
window.title("BMI Calculator")
window.geometry("450x500")
window.resizable(False, False)


# Title
title_label = tk.Label(
    window,
    text="BMI Calculator",
    font=("Arial", 24, "bold")
)
title_label.pack(pady=25)


# Name
name_label = tk.Label(
    window,
    text="Name:",
    font=("Arial", 12)
)
name_label.pack()

name_entry = tk.Entry(
    window,
    font=("Arial", 12),
    width=30
)
name_entry.pack(pady=5)


# Weight
weight_label = tk.Label(
    window,
    text="Weight (kg):",
    font=("Arial", 12)
)
weight_label.pack(pady=(15, 0))

weight_entry = tk.Entry(
    window,
    font=("Arial", 12),
    width=30
)
weight_entry.pack(pady=5)


# Height
height_label = tk.Label(
    window,
    text="Height (m):",
    font=("Arial", 12)
)
height_label.pack(pady=(15, 0))

height_entry = tk.Entry(
    window,
    font=("Arial", 12),
    width=30
)
height_entry.pack(pady=5)


# Calculate button
calculate_button = tk.Button(
    window,
    text="Calculate BMI",
    font=("Arial", 12, "bold"),
    width=20,
    command=calculate_bmi
)
calculate_button.pack(pady=20)
history_button = tk.Button(
    window,
    text="View BMI History",
    font=("Arial", 11),
    width=20,
    command=view_history
)
history_button.pack(pady=5)
trend_button = tk.Button(
    window,
    text="View BMI Trend",
    font=("Arial", 11),
    width=20,
    command=view_trend
)
trend_button.pack(pady=5)


# Result
result_label = tk.Label(
    window,
    text="Enter your details and click Calculate BMI",
    font=("Arial", 13, "bold"),
    wraplength=350
)
result_label.pack(pady=10)


# Initialize database
initialize_database()


# Start application
window.mainloop()