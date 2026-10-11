
import tkinter as tk
from tkinter import messagebox


def calculate_bmi():
    try:
        weight = float(weight_entry.get())
        height = float(height_entry.get())

        if weight <= 0 or height <= 0:
            messagebox.showerror(
                "Invalid Input",
                "Height and weight must be greater than zero."
            )
            return

        bmi = weight / (height ** 2)

        if bmi < 18.5:
            category = "Underweight"
        elif bmi < 25:
            category = "Normal Weight"
        elif bmi < 30:
            category = "Overweight"
        else:
            category = "Obesity"

        result_label.config(
            text=f"Your BMI: {bmi:.2f}\nCategory: {category}"
        )

    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Please enter valid numbers for height and weight."
        )


def reset_fields():
    height_entry.delete(0, tk.END)
    weight_entry.delete(0, tk.END)
    result_label.config(text="Enter your details to calculate BMI")


root = tk.Tk()
root.title("BMI Calculator")
root.geometry("400x450")
root.resizable(False, False)
root.configure(bg="#F0F4F8")

title_label = tk.Label(
    root,
    text="BMI Calculator",
    font=("Arial", 22, "bold"),
    bg="#F0F4F8",
    fg="#1E3A5F"
)
title_label.pack(pady=20)

tk.Label(
    root,
    text="Height (in meters)",
    font=("Arial", 12),
    bg="#F0F4F8"
).pack()

height_entry = tk.Entry(root, font=("Arial", 12), justify="center")
height_entry.pack(pady=8)

tk.Label(
    root,
    text="Weight (in kilograms)",
    font=("Arial", 12),
    bg="#F0F4F8"
).pack()

weight_entry = tk.Entry(root, font=("Arial", 12), justify="center")
weight_entry.pack(pady=8)

tk.Button(
    root,
    text="Calculate BMI",
    command=calculate_bmi,
    font=("Arial", 12, "bold"),
    bg="#2563EB",
    fg="white",
    width=18
).pack(pady=12)

tk.Button(
    root,
    text="Reset",
    command=reset_fields,
    font=("Arial", 11),
    width=12
).pack()

result_label = tk.Label(
    root,
    text="Enter your details to calculate BMI",
    font=("Arial", 12, "bold"),
    bg="#F0F4F8",
    fg="#1E3A5F",
    wraplength=340
)
result_label.pack(pady=20)

tk.Label(
    root,
    text="BMI is a screening measure, not a diagnosis.",
    font=("Arial", 9),
    bg="#F0F4F8",
    fg="#555555"
).pack(side="bottom", pady=12)

root.mainloop()
