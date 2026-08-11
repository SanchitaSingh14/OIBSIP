# BMI Calculator

A Python-based GUI BMI Calculator that calculates Body Mass Index, classifies the result into standard BMI categories, stores historical records using SQLite, and displays BMI trends using Matplotlib.

## Features

- User-friendly Tkinter GUI
- User name, weight, and height input
- BMI calculation using the standard formula
- BMI classification:
  - Underweight: BMI < 18.5
  - Normal: BMI 18.5 – 24.9
  - Overweight: BMI 25 – 29.9
  - Obese: BMI >= 30
- BMI result rounded to two decimal places
- Color-coded BMI feedback
- Input validation for invalid and negative values
- Multi-user BMI records
- SQLite database for historical records
- BMI history viewer
- BMI trend visualization using Matplotlib
- Database error handling

## Technologies Used

- Python
- Tkinter
- SQLite
- Matplotlib

## BMI Formula

BMI is calculated using:

BMI = Weight (kg) / Height² (m)

## Project Structure

```text
Python-Task2-BMICalculator/
│
├── bmi_calculator.py
├── requirements.txt
├── README.md
├── .gitignore
└── bmi_records.db