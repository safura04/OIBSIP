
import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


DB_NAME = "bmi_history.db"


def initialize_database():
    with sqlite3.connect(DB_NAME) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS bmi_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                height REAL NOT NULL,
                weight REAL NOT NULL,
                bmi REAL NOT NULL,
                category TEXT NOT NULL
            )
        """)


def get_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal Weight"
    elif bmi < 30:
        return "Overweight"
    return "Obesity"


def calculate_bmi():
    try:
        height = float(height_entry.get())
        weight = float(weight_entry.get())

        if height <= 0 or weight <= 0:
            messagebox.showerror(
                "Invalid Input",
                "Height and weight must be greater than zero."
            )
            return

        bmi = weight / (height ** 2)
        category = get_category(bmi)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with sqlite3.connect(DB_NAME) as connection:
            connection.execute("""
                INSERT INTO bmi_records
                (date, height, weight, bmi, category)
                VALUES (?, ?, ?, ?, ?)
            """, (current_time, height, weight, bmi, category))

        result_label.config(
            text=f"BMI: {bmi:.2f}\nCategory: {category}"
        )

    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Please enter valid numbers for height and weight."
        )
    except sqlite3.Error as error:
        messagebox.showerror(
            "Database Error",
            f"Could not save the result:\n{error}"
        )


def reset_fields():
    height_entry.delete(0, tk.END)
    weight_entry.delete(0, tk.END)
    result_label.config(text="Enter your details to calculate BMI")


def show_history():
    try:
        with sqlite3.connect(DB_NAME) as connection:
            records = connection.execute("""
                SELECT date, bmi, category
                FROM bmi_records
                ORDER BY id
            """).fetchall()

    except sqlite3.Error as error:
        messagebox.showerror("Database Error", str(error))
        return

    if not records:
        messagebox.showinfo(
            "No History",
            "Calculate your BMI at least once to view your history."
        )
        return

    dates = [record[0] for record in records]
    values = [record[1] for record in records]

    history_window = tk.Toplevel(root)
    history_window.title("BMI History Graph")
    history_window.geometry("700x450")

    figure = Figure(figsize=(7, 4), dpi=100)
    axis = figure.add_subplot(111)

    axis.plot(
        range(1, len(values) + 1),
        values,
        marker="o",
        linewidth=2
    )

    axis.axhline(
        y=18.5, linestyle="--", label="BMI 18.5"
    )
    axis.axhline(
        y=25, linestyle="--", label="BMI 25"
    )
    axis.axhline(
        y=30, linestyle="--", label="BMI 30"
    )

    axis.set_title("BMI History")
    axis.set_xlabel("Calculation Number")
    axis.set_ylabel("BMI")
    axis.set_xticks(range(1, len(values) + 1))
    axis.grid(True, alpha=0.3)
    axis.legend()
    figure.tight_layout()

    canvas = FigureCanvasTkAgg(
        figure, master=history_window
    )
    canvas.draw()
    canvas.get_tk_widget().pack(
        fill=tk.BOTH, expand=True
    )

    latest = records[-1]
    summary = (
        f"Latest record: {latest[0]} | "
        f"BMI: {latest[1]:.2f} | "
        f"Category: {latest[2]}"
    )

    tk.Label(
        history_window,
        text=summary,
        font=("Arial", 10)
    ).pack(pady=8)


initialize_database()

root = tk.Tk()
root.title("BMI Calculator - Advanced")
root.geometry("430x500")
root.resizable(False, False)
root.configure(bg="#F0F4F8")

tk.Label(
    root,
    text="BMI Calculator",
    font=("Arial", 23, "bold"),
    bg="#F0F4F8",
    fg="#1E3A5F"
).pack(pady=(20, 8))

tk.Label(
    root,
    text="Advanced Edition | BMI History Tracking",
    font=("Arial", 10),
    bg="#F0F4F8",
    fg="#555555"
).pack(pady=(0, 15))

tk.Label(
    root,
    text="Height (meters)",
    font=("Arial", 12),
    bg="#F0F4F8"
).pack()

height_entry = tk.Entry(
    root, font=("Arial", 12), justify="center"
)
height_entry.pack(pady=7)

tk.Label(
    root,
    text="Weight (kilograms)",
    font=("Arial", 12),
    bg="#F0F4F8"
).pack()

weight_entry = tk.Entry(
    root, font=("Arial", 12), justify="center"
)
weight_entry.pack(pady=7)

tk.Button(
    root,
    text="Calculate BMI",
    command=calculate_bmi,
    font=("Arial", 11, "bold"),
    bg="#2563EB",
    fg="white",
    width=20
).pack(pady=(12, 7))

tk.Button(
    root,
    text="View BMI History Graph",
    command=show_history,
    font=("Arial", 11),
    bg="#0F766E",
    fg="white",
    width=24
).pack(pady=5)

tk.Button(
    root,
    text="Reset",
    command=reset_fields,
    font=("Arial", 10),
    width=12
).pack(pady=5)

result_label = tk.Label(
    root,
    text="Enter your details to calculate BMI",
    font=("Arial", 12, "bold"),
    bg="#F0F4F8",
    fg="#1E3A5F",
    wraplength=380
)
result_label.pack(pady=12)

tk.Label(
    root,
    text="BMI is a screening measure, not a diagnosis.",
    font=("Arial", 9),
    bg="#F0F4F8",
    fg="#555555"
).pack(side="bottom", pady=10)

root.mainloop()
