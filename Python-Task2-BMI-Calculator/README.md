# BMI Calculator — Advanced Level

## Oasis Infobyte Python Programming Internship | Task 2

**Project Level:** Advanced  
**Project Type:** Desktop GUI Application

## Project Overview

The BMI Calculator is a Python desktop application developed as part of Task 2 of the Oasis Infobyte Python Programming Internship.

The application calculates Body Mass Index (BMI) using a person's height and weight, displays the corresponding BMI category, stores calculation records in an SQLite database, and visualizes BMI history using a graph.

## Features

- Graphical user interface built with Tkinter
- BMI calculation using height and weight
- Classification into Underweight, Normal Weight, Overweight, and Obesity
- Input validation for empty, non-numeric, zero, and negative values
- Automatic storage of BMI records in an SQLite database
- Persistent calculation history across application restarts
- BMI history graph using Matplotlib
- Reference lines for BMI values of 18.5, 25, and 30
- Reset button to clear the current input fields
- Error handling for invalid inputs and database failures

## Technologies Used

- **Python 3** — application logic
- **Tkinter** — graphical user interface
- **SQLite** — database storage
- **Matplotlib** — BMI history visualization

## Project Structure

```text
Python-Task2-BMI-Calculator/
├── bmi_calculator.py
├── requirements.txt
├── README.md
├── .gitignore
└── screenshots/
    └── bmi_calculator.png
```

**Note:** The `screenshots/` folder and screenshot will be added before final submission. The `bmi_history.db` database is generated automatically when the application runs and is excluded from Git using `.gitignore`.

## Installation and Execution

### Prerequisites

- Python 3 installed on your system
- pip package manager

### Installation

1. Clone or download the repository.
2. Open a terminal in the project directory.
3. Install the required dependency:

   ```bash
   python -m pip install -r requirements.txt
   ```

### Run the Application

Execute the following command:

```bash
python bmi_calculator.py
```

### How to Use

1. Enter your height in meters.
2. Enter your weight in kilograms.
3. Click **Calculate BMI** to calculate and save your result.
4. View the BMI value and corresponding category.
5. Click **View BMI History Graph** to visualize saved BMI records.
6. Click **Reset** to clear the current input fields.

## BMI Formula

BMI is calculated using the following formula:

**BMI = Weight (kg) / Height (m)²**

Example:

For a weight of 60 kg and a height of 1.65 m:

BMI = 60 / (1.65 × 1.65) = 22.04

## Adult BMI Categories

| BMI Range | Category |
|---|---|
| Below 18.5 | Underweight |
| 18.5 to below 25 | Normal Weight |
| 25 to below 30 | Overweight |
| 30 and above | Obesity |

**Disclaimer:** BMI is a screening measure and is not a diagnosis of health.

## Database

The application uses SQLite to store BMI calculation records, including:

- Date and time of calculation
- Height
- Weight
- BMI value
- BMI category

The database is created automatically when the application starts. Saved records can be used to display BMI history across multiple sessions.

## Testing

The application should be tested for:

- Valid height and weight values
- Empty input fields
- Non-numeric input
- Zero and negative values
- All four BMI categories
- Multiple saved calculations
- Database persistence after restarting the application
- BMI history graph generation

## Internship Task Details

- **Organization:** Oasis Infobyte
- **Internship:** Python Programming
- **Task Number:** Task 2
- **Task Name:** BMI Calculator
- **Project Level:** Advanced

## Author

Developed as part of the Oasis Infobyte Python Programming Internship.