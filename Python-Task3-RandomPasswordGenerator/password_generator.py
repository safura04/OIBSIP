import tkinter as tk
from tkinter import ttk, messagebox
import secrets
import string
import pyperclip


# Character sets for password generation
CHARACTERS = {
    "Uppercase (A-Z)": string.ascii_uppercase,
    "Lowercase (a-z)": string.ascii_lowercase,
    "Numbers (0-9)": string.digits,
    "Symbols (!@#$)": "!@#$%^&*()-_=+[]{};:,.?/"
}

AMBIGUOUS = "0O1lI"


class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Password Generator")
        self.root.geometry("540x690")
        self.root.resizable(False, False)
        self.root.configure(bg="#101827")

        self.history = []
        self.password_var = tk.StringVar()
        self.length_var = tk.IntVar(value=16)
        self.exclude_var = tk.BooleanVar(value=True)

        self.options = {
            name: tk.BooleanVar(value=True if i < 3 else False)
            for i, name in enumerate(CHARACTERS)
        }

        self.build_ui()

    def build_ui(self):
        tk.Label(
            self.root,
            text="SECURE PASSWORD GENERATOR",
            font=("Segoe UI", 19, "bold"),
            bg="#101827",
            fg="#60A5FA"
        ).pack(pady=(22, 5))

        tk.Label(
            self.root,
            text="Create strong, random passwords",
            font=("Segoe UI", 10),
            bg="#101827",
            fg="#CBD5E1"
        ).pack(pady=(0, 18))

        options_frame = tk.Frame(
            self.root, bg="#1E293B", padx=22, pady=16
        )
        options_frame.pack(fill="x", padx=25)

        tk.Label(
            options_frame,
            text="PASSWORD LENGTH",
            bg="#1E293B",
            fg="white",
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w")

        length_row = tk.Frame(options_frame, bg="#1E293B")
        length_row.pack(fill="x", pady=8)

        self.length_label = tk.Label(
            length_row,
            text="16 characters",
            bg="#1E293B",
            fg="#60A5FA",
            font=("Segoe UI", 10, "bold")
        )
        self.length_label.pack(side="right")

        self.length_scale = ttk.Scale(
            length_row,
            from_=8,
            to=64,
            command=self.update_length
        )
        self.length_scale.set(16)
        self.length_scale.pack(
            side="left", fill="x", expand=True, padx=(0, 12)
        )

        tk.Label(
            options_frame,
            text="CHARACTER TYPES",
            bg="#1E293B",
            fg="white",
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", pady=(12, 5))

        for name, variable in self.options.items():
            tk.Checkbutton(
                options_frame,
                text=name,
                variable=variable,
                bg="#1E293B",
                fg="#E2E8F0",
                selectcolor="#334155",
                activebackground="#1E293B",
                activeforeground="white",
                font=("Segoe UI", 10)
            ).pack(anchor="w", pady=2)

        tk.Checkbutton(
            options_frame,
            text="Exclude ambiguous characters (0, O, 1, l, I)",
            variable=self.exclude_var,
            bg="#1E293B",
            fg="#E2E8F0",
            selectcolor="#334155",
            activebackground="#1E293B",
            activeforeground="white",
            font=("Segoe UI", 9)
        ).pack(anchor="w", pady=(10, 0))

        tk.Button(
            self.root,
            text="GENERATE PASSWORD",
            command=self.generate_password,
            bg="#2563EB",
            fg="white",
            activebackground="#1D4ED8",
            activeforeground="white",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            cursor="hand2",
            pady=11
        ).pack(fill="x", padx=25, pady=18)

        result_frame = tk.Frame(
            self.root, bg="#1E293B", padx=18, pady=15
        )
        result_frame.pack(fill="x", padx=25)

        tk.Label(
            result_frame,
            text="YOUR PASSWORD",
            bg="#1E293B",
            fg="#94A3B8",
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w")

        tk.Entry(
            result_frame,
            textvariable=self.password_var,
            font=("Consolas", 13),
            justify="center",
            bg="#0F172A",
            fg="#4ADE80",
            insertbackground="white",
            relief="flat",
            state="readonly"
        ).pack(fill="x", pady=10, ipady=9)

        self.strength_label = tk.Label(
            result_frame,
            text="Strength: Not generated",
            bg="#1E293B",
            fg="#CBD5E1",
            font=("Segoe UI", 10, "bold")
        )
        self.strength_label.pack(pady=(0, 10))

        tk.Button(
            result_frame,
            text="COPY TO CLIPBOARD",
            command=self.copy_password,
            bg="#334155",
            fg="white",
            activebackground="#475569",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            pady=8
        ).pack(fill="x")

        history_frame = tk.Frame(self.root, bg="#101827")
        history_frame.pack(fill="x", padx=25, pady=16)

        tk.Label(
            history_frame,
            text="RECENT PASSWORDS (SESSION ONLY)",
            bg="#101827",
            fg="#94A3B8",
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w")

        self.history_box = tk.Listbox(
            history_frame,
            height=4,
            bg="#1E293B",
            fg="#CBD5E1",
            selectbackground="#2563EB",
            font=("Consolas", 10),
            relief="flat"
        )
        self.history_box.pack(fill="x", pady=6)

        tk.Label(
            self.root,
            text="Passwords are not saved to a file.",
            bg="#101827",
            fg="#64748B",
            font=("Segoe UI", 9)
        ).pack()

    def update_length(self, value):
        length = round(float(value))
        self.length_var.set(length)
        self.length_label.config(text=f"{length} characters")

    def generate_password(self):
        length = self.length_var.get()

        selected = [
            chars
            for name, chars in CHARACTERS.items()
            if self.options[name].get()
        ]

        if len(selected) < 2:
            messagebox.showerror(
                "Invalid Selection",
                "Please select at least two character types."
            )
            return

        if self.exclude_var.get():
            selected = [
                "".join(c for c in chars if c not in AMBIGUOUS)
                for chars in selected
            ]

        if any(not chars for chars in selected):
            messagebox.showerror(
                "Invalid Selection",
                "A selected character type has no available characters."
            )
            return

        # Guarantee at least one character from every selected type
        password_chars = [
            secrets.choice(chars) for chars in selected
        ]

        all_chars = "".join(selected)

        password_chars.extend(
            secrets.choice(all_chars)
            for _ in range(length - len(password_chars))
        )

        # Securely shuffle the password characters
        for i in range(len(password_chars) - 1, 0, -1):
            j = secrets.randbelow(i + 1)
            password_chars[i], password_chars[j] = (
                password_chars[j], password_chars[i]
            )

        password = "".join(password_chars)
        self.password_var.set(password)
        self.update_strength(password)

        # Automatically copy the generated password
        try:
            pyperclip.copy(password)
        except pyperclip.PyperclipException:
            messagebox.showwarning(
                "Clipboard Warning",
                "Password generated, but automatic copying failed. "
                "Use the Copy to Clipboard button or copy it manually."
            )

        # Keep only the five most recent passwords in memory
        self.history.insert(0, password)
        self.history = self.history[:5]

        self.history_box.delete(0, tk.END)

        for item in self.history:
            self.history_box.insert(tk.END, item)

    def update_strength(self, password):
        length = len(password)

        variety = sum([
            any(c in string.ascii_lowercase for c in password),
            any(c in string.ascii_uppercase for c in password),
            any(c in string.digits for c in password),
            any(c in CHARACTERS["Symbols (!@#$)"] for c in password)
        ])

        if length >= 16 and variety >= 3:
            strength = "Strong"
            color = "#4ADE80"
        elif length >= 12 and variety >= 2:
            strength = "Medium"
            color = "#FACC15"
        else:
            strength = "Weak"
            color = "#F87171"

        self.strength_label.config(
            text=f"Strength: {strength}",
            fg=color
        )

    def copy_password(self):
        password = self.password_var.get()

        if not password:
            messagebox.showwarning(
                "No Password",
                "Generate a password first."
            )
            return

        try:
            pyperclip.copy(password)
            messagebox.showinfo(
                "Copied",
                "Password copied to clipboard."
            )
        except pyperclip.PyperclipException:
            messagebox.showerror(
                "Clipboard Error",
                "Clipboard access failed. Please copy the password manually."
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()