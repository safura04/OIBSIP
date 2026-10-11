import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


DB_NAME = "bmi_history.db"

BG_COLOR = "#F0F4F8"
TEXT_COLOR = "#1E3A5F"

CATEGORY_COLORS = {
    "Underweight": "#2563EB",
    "Normal Weight": "#15803D",
    "Overweight": "#D97706",
    "Obesity": "#DC2626",
}


# -------------------- DATABASE FUNCTIONS --------------------

def initialize_database():
    try:
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

            columns = [
                row[1]
                for row in connection.execute(
                    "PRAGMA table_info(bmi_records)"
                )
            ]

            if "user_name" not in columns:
                connection.execute("""
                    ALTER TABLE bmi_records
                    ADD COLUMN user_name TEXT NOT NULL DEFAULT 'Guest'
                """)

    except sqlite3.Error as error:
        messagebox.showerror(
            "Database Error",
            f"Could not initialize the database:\n{error}"
        )
        raise


def get_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal Weight"
    elif bmi < 30:
        return "Overweight"
    return "Obesity"


# -------------------- BMI CALCULATION --------------------

def calculate_bmi():
    user_name = name_entry.get().strip()

    if not user_name:
        messagebox.showerror(
            "Invalid Input",
            "Please enter a user name."
        )
        return

    try:
        height = float(height_entry.get())
        weight = float(weight_entry.get())

        if height <= 0 or weight <= 0:
            messagebox.showerror(
                "Invalid Input",
                "Height and weight must be greater than zero."
            )
            return

        if height > 3 or weight > 700:
            messagebox.showerror(
                "Invalid Input",
                "Please check your height and weight values."
            )
            return

        bmi = weight / (height ** 2)
        category = get_category(bmi)
        current_time = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        try:
            with sqlite3.connect(DB_NAME) as connection:
                connection.execute("""
                    INSERT INTO bmi_records
                    (date, height, weight, bmi, category, user_name)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    current_time,
                    height,
                    weight,
                    bmi,
                    category,
                    user_name
                ))

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                f"Could not save the BMI record:\n{error}"
            )
            return

        result_label.config(
            text=f"User: {user_name}\n"
                 f"BMI: {bmi:.2f}\n"
                 f"Category: {category}",
            fg=CATEGORY_COLORS[category]
        )

        status_label.config(
            text="BMI record saved successfully.",
            fg="#15803D"
        )

    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Please enter valid numbers for height and weight."
        )


# -------------------- RESET --------------------

def reset_fields():
    name_entry.delete(0, tk.END)
    height_entry.delete(0, tk.END)
    weight_entry.delete(0, tk.END)

    result_label.config(
        text="Enter your details to calculate BMI",
        fg=TEXT_COLOR
    )
    status_label.config(text="")


# -------------------- BMI HISTORY GRAPH --------------------

def show_history():
    user_name = name_entry.get().strip()

    if not user_name:
        messagebox.showerror(
            "User Required",
            "Enter a user name to view that user's BMI history."
        )
        return

    try:
        with sqlite3.connect(DB_NAME) as connection:
            records = connection.execute("""
                SELECT date, bmi, category
                FROM bmi_records
                WHERE user_name = ?
                ORDER BY date, id
            """, (user_name,)).fetchall()

    except sqlite3.Error as error:
        messagebox.showerror(
            "Database Error",
            f"Could not read BMI history:\n{error}"
        )
        return

    if not records:
        messagebox.showinfo(
            "No History",
            f"No BMI records found for {user_name}."
        )
        return

    dates = [
        datetime.strptime(record[0], "%Y-%m-%d %H:%M:%S")
        for record in records
    ]
    values = [record[1] for record in records]

    history_window = tk.Toplevel(root)
    history_window.title(f"BMI History - {user_name}")
    history_window.geometry("800x500")
    history_window.configure(bg=BG_COLOR)

    figure = Figure(figsize=(8, 4.5), dpi=100)
    axis = figure.add_subplot(111)

    axis.plot(
        dates,
        values,
        marker="o",
        linewidth=2,
        color="#2563EB",
        label="BMI"
    )

    axis.axhline(
        y=18.5, linestyle="--",
        color="#2563EB", alpha=0.7, label="18.5"
    )
    axis.axhline(
        y=25, linestyle="--",
        color="#15803D", alpha=0.7, label="25"
    )
    axis.axhline(
        y=30, linestyle="--",
        color="#DC2626", alpha=0.7, label="30"
    )

    axis.set_title(f"BMI Trend for {user_name}")
    axis.set_xlabel("Date and Time")
    axis.set_ylabel("BMI")
    axis.grid(True, alpha=0.3)
    axis.legend()
    figure.autofmt_xdate()
    figure.tight_layout()

    canvas = FigureCanvasTkAgg(
        figure,
        master=history_window
    )
    canvas.draw()
    canvas.get_tk_widget().pack(
        fill=tk.BOTH,
        expand=True,
        padx=10,
        pady=10
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
        font=("Arial", 10),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(pady=8)


# -------------------- GUI DESIGN --------------------

root = tk.Tk()
root.title("BMI Calculator - Advanced")
root.geometry("450x610")
root.resizable(False, False)
root.configure(bg=BG_COLOR)

tk.Label(
    root,
    text="BMI Calculator",
    font=("Arial", 23, "bold"),
    bg=BG_COLOR,
    fg=TEXT_COLOR
).pack(pady=(18, 6))

tk.Label(
    root,
    text="Advanced Edition | BMI History Tracking",
    font=("Arial", 10),
    bg=BG_COLOR,
    fg="#555555"
).pack(pady=(0, 12))

tk.Label(
    root,
    text="User Name",
    font=("Arial", 12),
    bg=BG_COLOR
).pack()

name_entry = tk.Entry(
    root,
    font=("Arial", 12),
    justify="center"
)
name_entry.pack(pady=5)

tk.Label(
    root,
    text="Height (meters)",
    font=("Arial", 12),
    bg=BG_COLOR
).pack()

height_entry = tk.Entry(
    root,
    font=("Arial", 12),
    justify="center"
)
height_entry.pack(pady=5)

tk.Label(
    root,
    text="Weight (kilograms)",
    font=("Arial", 12),
    bg=BG_COLOR
).pack()

weight_entry = tk.Entry(
    root,
    font=("Arial", 12),
    justify="center"
)
weight_entry.pack(pady=5)

tk.Button(
    root,
    text="Calculate BMI",
    command=calculate_bmi,
    font=("Arial", 11, "bold"),
    bg="#2563EB",
    fg="white",
    width=20
).pack(pady=(10, 5))

tk.Button(
    root,
    text="View My BMI History Graph",
    command=show_history,
    font=("Arial", 11),
    bg="#0F766E",
    fg="white",
    width=26
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
    bg=BG_COLOR,
    fg=TEXT_COLOR,
    wraplength=400
)
result_label.pack(pady=(10, 5))

status_label = tk.Label(
    root,
    text="",
    font=("Arial", 9),
    bg=BG_COLOR,
    fg="#15803D"
)
status_label.pack(pady=3)

tk.Label(
    root,
    text="BMI is a screening measure, not a diagnosis.",
    font=("Arial", 9),
    bg=BG_COLOR,
    fg="#555555"
).pack(side="bottom", pady=10)


# -------------------- START APPLICATION --------------------

try:
    initialize_database()
except sqlite3.Error:
    root.destroy()
    raise

root.mainloop()