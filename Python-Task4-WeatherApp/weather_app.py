import os
import threading
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY", "").strip()
CURRENT_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"


class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("WeatherNow | Advanced Weather App")
        self.root.geometry("1000x780")
        self.root.minsize(650, 550)
        self.root.configure(bg="#101827")

        self.bg = "#101827"
        self.card = "#1c293d"
        self.accent = "#5cc8ff"
        self.white = "#f3f7ff"
        self.muted = "#aab8ce"

        self.city_var = tk.StringVar()
        self.status_var = tk.StringVar(
            value="Search for a city to get started."
        )
        self.use_fahrenheit = False
        self.current_data = None
        self.forecast_data = None
        self.loading = False

        self.build_ui()

    def build_ui(self):
        # Scrollable container: all app widgets belong inside self.content.
        self.scroll_container = tk.Frame(self.root, bg=self.bg)
        self.scroll_container.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(
            self.scroll_container,
            bg=self.bg,
            highlightthickness=0,
            borderwidth=0
        )
        self.scrollbar = tk.Scrollbar(
            self.scroll_container,
            orient="vertical",
            command=self.canvas.yview
        )
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.content = tk.Frame(self.canvas, bg=self.bg)
        self.canvas_window = self.canvas.create_window(
            (0, 0), window=self.content, anchor="nw"
        )

        self.content.bind("<Configure>", self._update_scrollregion)
        self.canvas.bind("<Configure>", self._resize_content)

        # Windows and macOS mouse wheel; Linux wheel buttons are also supported.
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        self.canvas.bind_all("<Button-4>", self.on_mousewheel_linux)
        self.canvas.bind_all("<Button-5>", self.on_mousewheel_linux)

        header = tk.Frame(self.content, bg=self.bg)
        header.pack(fill="x", padx=25, pady=(18, 10))

        tk.Label(
            header, text="WeatherNow",
            font=("Segoe UI", 27, "bold"),
            bg=self.bg, fg=self.white
        ).pack(anchor="w")

        tk.Label(
            header,
            text="LIVE WEATHER  |  HOURLY UPDATES  |  5-DAY FORECAST",
            font=("Segoe UI", 10, "bold"),
            bg=self.bg, fg=self.accent
        ).pack(anchor="w", pady=(3, 0))

        search = tk.Frame(self.content, bg=self.card)
        search.pack(fill="x", padx=25, pady=10)

        self.city_entry = tk.Entry(
            search, textvariable=self.city_var,
            font=("Segoe UI", 13), relief="flat",
            bg="#27364d", fg=self.white,
            insertbackground=self.white
        )
        self.city_entry.pack(
            side="left", fill="x", expand=True,
            padx=(12, 8), pady=12, ipady=8
        )
        self.city_entry.bind(
            "<Return>", lambda event: self.search_weather()
        )

        self.search_button = tk.Button(
            search, text="Search",
            command=self.search_weather,
            font=("Segoe UI", 11, "bold"),
            bg=self.accent, fg="#101827",
            activebackground="#9cdeff",
            relief="flat", cursor="hand2",
            padx=18, pady=9
        )
        self.search_button.pack(side="right", padx=(0, 12), pady=12)

        controls = tk.Frame(self.content, bg=self.bg)
        controls.pack(fill="x", padx=25, pady=3)

        self.demo_button = tk.Button(
            controls, text="Try Demo",
            command=self.load_demo,
            bg=self.card, fg=self.accent,
            activebackground="#27364d",
            activeforeground=self.white,
            relief="flat", cursor="hand2",
            padx=12, pady=7
        )
        self.demo_button.pack(side="left", padx=4)

        self.unit_button = tk.Button(
            controls, text="Switch to °F",
            command=self.toggle_units,
            bg=self.card, fg=self.white,
            activebackground="#27364d",
            activeforeground=self.white,
            relief="flat", cursor="hand2",
            padx=12, pady=7
        )
        self.unit_button.pack(side="right", padx=4)

        self.refresh_button = tk.Button(
            controls, text="↻ Refresh",
            command=self.search_weather,
            bg=self.card, fg=self.white,
            activebackground="#27364d",
            activeforeground=self.white,
            relief="flat", cursor="hand2",
            padx=12, pady=7
        )
        self.refresh_button.pack(side="right", padx=4)

        tk.Label(
            self.content, textvariable=self.status_var,
            font=("Segoe UI", 10),
            bg=self.bg, fg=self.muted
        ).pack(anchor="w", padx=28, pady=(5, 8))

        self.current_card = tk.Frame(
            self.content, bg=self.card,
            highlightthickness=1,
            highlightbackground="#2b3c55"
        )
        self.current_card.pack(fill="x", padx=25, pady=6)

        self.city_label = tk.Label(
            self.current_card, text="Your city's weather",
            font=("Segoe UI", 18, "bold"),
            bg=self.card, fg=self.white
        )
        self.city_label.pack(anchor="w", padx=20, pady=(12, 0))

        self.date_label = tk.Label(
            self.current_card, text="",
            font=("Segoe UI", 10),
            bg=self.card, fg=self.muted
        )
        self.date_label.pack(anchor="w", padx=20)

        self.icon_label = tk.Label(
            self.current_card, text="🌤️",
            font=("Segoe UI Emoji", 30),
            bg=self.card, fg=self.white
        )
        self.icon_label.pack(anchor="w", padx=18, pady=(3, 0))

        self.temp_label = tk.Label(
            self.current_card, text="--°C",
            font=("Segoe UI", 38, "bold"),
            bg=self.card, fg=self.accent
        )
        self.temp_label.pack(anchor="w", padx=20)

        self.description_label = tk.Label(
            self.current_card,
            text="Search for a city to see current conditions.",
            font=("Segoe UI", 12),
            bg=self.card, fg=self.white
        )
        self.description_label.pack(
            anchor="w", padx=20, pady=(0, 14)
        )

        metrics_frame = tk.Frame(self.content, bg=self.bg)
        metrics_frame.pack(fill="x", padx=25, pady=5)
        self.metric_labels = {}

        for title, key in [
            ("Feels like", "feels"),
            ("Humidity", "humidity"),
            ("Wind speed", "wind"),
            ("Pressure", "pressure")
        ]:
            box = tk.Frame(metrics_frame, bg=self.card)
            box.pack(
                side="left", expand=True, fill="both",
                padx=4, pady=3
            )
            tk.Label(
                box, text=title,
                font=("Segoe UI", 9),
                bg=self.card, fg=self.muted
            ).pack(pady=(9, 2))
            value = tk.Label(
                box, text="--",
                font=("Segoe UI", 12, "bold"),
                bg=self.card, fg=self.white
            )
            value.pack(pady=(0, 9))
            self.metric_labels[key] = value

        tk.Label(
            self.content, text="NEXT 6 HOURS",
            font=("Segoe UI", 11, "bold"),
            bg=self.bg, fg=self.accent
        ).pack(anchor="w", padx=28, pady=(10, 3))

        self.hourly_frame = tk.Frame(self.content, bg=self.bg)
        self.hourly_frame.pack(fill="x", padx=25, pady=2)

        tk.Label(
            self.content, text="5-DAY FORECAST",
            font=("Segoe UI", 11, "bold"),
            bg=self.bg, fg=self.accent
        ).pack(anchor="w", padx=28, pady=(10, 3))

        self.forecast_frame = tk.Frame(self.content, bg=self.bg)
        self.forecast_frame.pack(fill="x", padx=25, pady=(0, 12))

        self.city_entry.focus_set()

    def _update_scrollregion(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _resize_content(self, event):
        self.canvas.itemconfigure(self.canvas_window, width=event.width)

    def on_mousewheel(self, event):
        # Windows commonly reports multiples of 120; smaller deltas are handled too.
        if event.delta:
            steps = int(-event.delta / 120)
            if steps == 0:
                steps = -1 if event.delta > 0 else 1
            self.canvas.yview_scroll(steps, "units")

    def on_mousewheel_linux(self, event):
        self.canvas.yview_scroll(-1 if event.num == 4 else 1, "units")

    @staticmethod
    def get_icon(condition):
        icons = {
            "clear": "☀️", "clouds": "☁️", "rain": "🌧️",
            "drizzle": "🌦️", "thunderstorm": "⛈️",
            "snow": "❄️", "mist": "🌫️", "fog": "🌫️",
            "haze": "🌫️", "smoke": "🌫️", "dust": "🌫️",
            "sand": "🌫️", "ash": "🌫️", "squall": "💨",
            "tornado": "🌪️"
        }
        return icons.get(condition.lower(), "🌤️")

    def format_temperature(self, celsius):
        if self.use_fahrenheit:
            return f"{celsius * 9 / 5 + 32:.1f}°F"
        return f"{celsius:.1f}°C"

    def toggle_units(self):
        self.use_fahrenheit = not self.use_fahrenheit
        self.unit_button.config(
            text="Switch to °C" if self.use_fahrenheit else "Switch to °F"
        )
        if self.current_data and self.forecast_data:
            self.display_weather(self.current_data, self.forecast_data)

    def search_weather(self):
        city = self.city_var.get().strip()
        if not city:
            messagebox.showwarning("Missing city", "Please enter a city name.")
            return
        if not API_KEY:
            messagebox.showerror(
                "API key missing",
                "Add OPENWEATHER_API_KEY to your .env file."
            )
            return
        if self.loading:
            return

        self.loading = True
        self.search_button.config(state="disabled", text="Loading...")
        self.refresh_button.config(state="disabled")
        self.status_var.set(f"Fetching weather for {city}...")

        threading.Thread(
            target=self.fetch_weather, args=(city,), daemon=True
        ).start()

    def fetch_weather(self, city):
        try:
            params = {"q": city, "appid": API_KEY, "units": "metric"}

            response = requests.get(CURRENT_URL, params=params, timeout=12)
            response.raise_for_status()
            current = response.json()

            response = requests.get(FORECAST_URL, params=params, timeout=12)
            response.raise_for_status()
            forecast = response.json()

            self.root.after(
                0, lambda: self.display_weather(current, forecast)
            )
        except requests.exceptions.HTTPError as exc:
            code = exc.response.status_code if exc.response is not None else 0
            messages = {
                400: "Invalid request. Check the city name.",
                401: "API key is invalid or not active yet.",
                404: "City not found. Check the spelling.",
                429: "API request limit reached. Please wait."
            }
            error = messages.get(code, f"Weather service returned HTTP {code}.")
            self.root.after(0, lambda msg=error: self.show_error(msg))
        except requests.exceptions.Timeout:
            self.root.after(
                0, lambda: self.show_error("Request timed out. Please try again.")
            )
        except requests.exceptions.RequestException:
            self.root.after(
                0, lambda: self.show_error(
                    "Network error. Check your internet connection."
                )
            )
        except (ValueError, KeyError, TypeError):
            self.root.after(
                0, lambda: self.show_error("Unexpected weather data received.")
            )

    def display_weather(self, current, forecast):
        self.current_data = current
        self.forecast_data = forecast

        self.city_label.config(
            text=f"{current['name']}, {current['sys']['country']}"
        )
        self.date_label.config(text=datetime.now().strftime("%A, %d %B %Y"))
        self.icon_label.config(
            text=self.get_icon(current["weather"][0]["main"])
        )
        self.temp_label.config(
            text=self.format_temperature(current["main"]["temp"])
        )
        self.description_label.config(
            text=current["weather"][0]["description"].title()
        )
        self.metric_labels["feels"].config(
            text=self.format_temperature(current["main"]["feels_like"])
        )
        self.metric_labels["humidity"].config(
            text=f"{current['main']['humidity']}%"
        )
        self.metric_labels["wind"].config(
            text=f"{current['wind']['speed']} m/s"
        )
        self.metric_labels["pressure"].config(
            text=f"{current['main']['pressure']} hPa"
        )

        self.display_hourly(forecast)
        self.display_five_day(forecast)
        self.status_var.set(
            f"Weather updated successfully at {datetime.now().strftime('%H:%M:%S')}."
        )
        self.finish_loading()

    def display_hourly(self, forecast):
        for widget in self.hourly_frame.winfo_children():
            widget.destroy()

        # The standard 5-day forecast endpoint supplies readings about every 3 hours.
        entries = forecast.get("list", [])[:3]
        if not entries:
            tk.Label(
                self.hourly_frame, text="Hourly forecast unavailable.",
                bg=self.bg, fg=self.muted
            ).pack(anchor="w")
            return

        for item in entries:
            box = tk.Frame(self.hourly_frame, bg=self.card)
            box.pack(side="left", expand=True, fill="both", padx=4, pady=3)
            forecast_time = datetime.fromtimestamp(item["dt"])

            tk.Label(
                box, text=forecast_time.strftime("%I %p"),
                font=("Segoe UI", 10, "bold"),
                bg=self.card, fg=self.white
            ).pack(pady=(8, 3))
            tk.Label(
                box, text=self.get_icon(item["weather"][0]["main"]),
                font=("Segoe UI Emoji", 18),
                bg=self.card, fg=self.white
            ).pack(pady=2)
            tk.Label(
                box, text=self.format_temperature(item["main"]["temp"]),
                font=("Segoe UI", 11, "bold"),
                bg=self.card, fg=self.accent
            ).pack(pady=(3, 8))

    def display_five_day(self, forecast):
        for widget in self.forecast_frame.winfo_children():
            widget.destroy()

        daily = {}
        for item in forecast.get("list", []):
            date_time = datetime.fromtimestamp(item["dt"])
            date_key = date_time.date()
            distance = abs(date_time.hour - 12)
            if date_key not in daily or distance < daily[date_key]["distance"]:
                daily[date_key] = {"item": item, "distance": distance}

        days = list(daily.items())[:5]
        if not days:
            tk.Label(
                self.forecast_frame, text="Five-day forecast unavailable.",
                bg=self.bg, fg=self.muted
            ).pack(anchor="w")
            return

        for date_key, details in days:
            item = details["item"]
            card = tk.Frame(
                self.forecast_frame, bg=self.card,
                highlightthickness=1, highlightbackground="#2b3c55"
            )
            card.pack(side="left", expand=True, fill="both", padx=4, pady=4)

            tk.Label(
                card, text=date_key.strftime("%a"),
                font=("Segoe UI", 11, "bold"),
                bg=self.card, fg=self.white
            ).pack(pady=(10, 4))
            tk.Label(
                card, text=date_key.strftime("%d %b"),
                font=("Segoe UI", 9), bg=self.card, fg=self.muted
            ).pack(pady=2)
            tk.Label(
                card, text=self.get_icon(item["weather"][0]["main"]),
                font=("Segoe UI Emoji", 21),
                bg=self.card, fg=self.white
            ).pack(pady=5)
            tk.Label(
                card, text=self.format_temperature(item["main"]["temp"]),
                font=("Segoe UI", 12, "bold"),
                bg=self.card, fg=self.accent
            ).pack(pady=(3, 2))
            tk.Label(
                card, text=item["weather"][0]["description"].title(),
                font=("Segoe UI", 8), wraplength=105,
                bg=self.card, fg=self.muted
            ).pack(padx=4, pady=(2, 10))

    def load_demo(self):
        now = datetime.now()
        current = {
            "name": "Pune",
            "sys": {"country": "IN"},
            "main": {
                "temp": 28.5, "feels_like": 30.1,
                "humidity": 62, "pressure": 1012
            },
            "wind": {"speed": 3.4},
            "weather": [{"main": "Clouds", "description": "scattered clouds"}]
        }

        forecast_list = []
        conditions = [
            ("Clouds", "scattered clouds"),
            ("Clear", "clear sky"),
            ("Rain", "light rain"),
            ("Clear", "clear sky"),
            ("Clouds", "broken clouds")
        ]
        for index in range(40):
            timestamp = int(now.timestamp()) + index * 10800
            condition, description = conditions[(index // 8) % len(conditions)]
            forecast_list.append({
                "dt": timestamp,
                "dt_txt": datetime.fromtimestamp(timestamp).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "main": {
                    "temp": 26 + (index % 7) - 3,
                    "feels_like": 27 + (index % 7) - 3,
                    "humidity": 55 + (index % 20),
                    "pressure": 1010
                },
                "weather": [{"main": condition, "description": description}],
                "wind": {"speed": 2.5}
            })

        self.city_var.set("Pune")
        self.display_weather(current, {"list": forecast_list})
        self.status_var.set("DEMO MODE — sample data only, not live weather.")

    def finish_loading(self):
        self.loading = False
        self.search_button.config(state="normal", text="Search")
        self.refresh_button.config(state="normal")

    def show_error(self, message):
        self.status_var.set("Could not retrieve weather data.")
        self.finish_loading()
        messagebox.showerror("Weather Error", message)


if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
