# WeatherNow — Advanced Weather Application

## Oasis Infobyte Python Programming Internship | Task 4

**Project Level:** Advanced  
**Project Type:** Desktop GUI Application  
**Technology:** Python, Tkinter, OpenWeatherMap API

## Project Overview

WeatherNow is an advanced-level desktop weather application developed using Python as part of Task 4 of the Oasis Infobyte Python Programming Internship.

The application retrieves real-time weather information and forecast data for a user-selected city using the OpenWeatherMap API. It features a graphical user interface built with Tkinter, making weather information easy to access and understand.

## Features

- **Real-Time Weather:** Displays current weather conditions for a searched city.
- **Weather Details:** Shows temperature, feels-like temperature, humidity, wind speed, and other available weather information.
- **Weather Icons:** Displays visual indicators corresponding to weather conditions.
- **Weather Forecast:** Provides upcoming forecast information.
- **Temperature Unit Conversion:** Allows users to switch between Celsius and Fahrenheit.
- **City Search:** Fetches weather information for different cities.
- **Refresh Option:** Allows users to refresh the weather data.
- **Demo Mode:** Supports demonstration without relying on a successful live API response.
- **Scrollable Interface:** Supports scrolling through the application's content.
- **Error Handling:** Handles API errors and unsuccessful city searches.
- **Environment Variables:** Keeps the API key in a local `.env` file rather than hardcoding it into the source code.

## Technologies Used

- Python 3
- Tkinter — graphical user interface
- Requests — HTTP requests to the weather API
- Python-dotenv — loading environment variables
- OpenWeatherMap API — current weather and forecast data

## Project Structure

```text
Python-Task4-WeatherApp/
│
├── weather_app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env
└── venv/
```

**Note:** `.env` and `venv/` are local files/folders and should not be uploaded to GitHub.

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Navigate to the project directory:

```bash
cd OIBSIP/Python-Task4-WeatherApp
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

On Windows Git Bash:

```bash
source venv/Scripts/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure the API key

Create a `.env` file in the project directory and add your OpenWeatherMap API key:

```text
OPENWEATHER_API_KEY=your_api_key_here
```

Replace `your_api_key_here` with your own API key. Do not share or commit this file.

### 5. Run the application

```bash
python weather_app.py
```

## How to Use

1. Launch the application.
2. Enter the name of a city.
3. Search for the city to retrieve its weather information.
4. View the current weather details and forecast.
5. Switch temperature units when required.
6. Use the refresh option to update the information.

## API

This application uses the OpenWeatherMap API to retrieve current weather conditions and forecast data.

Website: https://openweathermap.org/api

An API key is required for live weather data. API access and forecast availability depend on the selected API endpoints and account access.

## Security

- API credentials are stored in `.env`.
- `.env` and `venv/` are excluded through `.gitignore`.
- Never publish your API key in source code, screenshots, or public repositories.

## Learning Outcomes

- Building desktop GUI applications using Tkinter.
- Integrating external APIs with Python.
- Handling HTTP requests and API responses.
- Managing environment variables securely.
- Implementing error handling and threaded network requests.
- Designing a user-friendly and scrollable interface.

## Internship Information

**Organization:** Oasis Infobyte  
**Internship:** Python Programming Internship  
**Task:** Task 4 — Weather Application  
**Project Level:** Advanced

## Author

Developed as part of the Oasis Infobyte Python Programming Internship.