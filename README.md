# Smart Fitness Management System

## Project Description

The **Smart Fitness Management System (SFMS)** is a Python desktop application built with Tkinter. It allows users to manage personal fitness goals by tracking workouts, nutrition, and progress via a user-friendly interface. All data is stored in memory for demonstration purposes, with modules for user profiles, logging activities, and generating basic analytics.

## Features

- **User Management**: Create, update, and delete user profiles with details (name, age, gender, goals).
- **Workout Tracking**: Log, edit, and delete workouts including exercise type, duration, calories burned, and notes.
- **Goal Tracking**: Set and monitor fitness goals with progress and targets.
- **Nutrition Tracking**: Record meals with nutritional data (calories, protein, carbs, fats, notes).
- **Reports & Analytics**: View summaries of calories burned vs. consumed, nutrition totals, and create basic charts (requires Matplotlib).

## Technologies Used

- Python 3 (Programming Language)
- Tkinter (GUI Framework)
- Standard Python libraries (tkinter, messagebox, scrolledtext)
- Matplotlib (for charts – optional)

## Installation

1. **Clone the Repository**
    ```
    git clone https://github.com/Sazzad591/Smart-Fitness-Management-System.git
    ```
2. **Install Python**
    - Check Python 3 is installed:
        ```
        python --version
        ```
    - Download from [python.org](https://www.python.org/)
3. **Install Dependencies** (for charts)
    ```
    pip install matplotlib
    ```
4. **Run the Application**
    ```
    python sfms_gui.py
    ```

## Usage

- Open the app by running `sfms_gui.py`.
- Access modules via the main menu: User Management, Workout Tracking, Goal Tracking, Nutrition Tracking, Reports.
- **User Management**: Add or edit users.
- **Workout Tracking**: Log exercises with calories and notes, and edit/delete entries.
- **Goal Tracking**: Set goals and update progress.
- **Nutrition Tracking**: Log meals and nutrition data.
- **Reports & Analytics**: Generate summaries and optional bar chart.

**Note:** All data is lost when the app is closed. For persistent storage, file/database integration would be needed.

## Screenshots

### Main Window
(screenshots/1.png)

### User Management
(screenshots/2.png)

### Workout Tracking Module
(screenshots/3.png)

### Goal Tracking Module
(screenshots/4.png)

### Nutrition Tracking Module
(screenshots/5.png)

### Reports & Analytics
![Reports](screenshots/6.png)

## Contributing

Contributions are welcome!

1. Fork the repository
2. Create your feature branch
    ```
    git checkout -b feature-name
    ```
3. Commit your changes
    ```
    git commit -m "Describe your feature"
    ```
4. Push to your branch
    ```
    git push origin feature-name
    ```
5. Open a Pull Request

## License

This project is for educational purposes only.

## Contact

For questions or suggestions, please open a GitHub issue or contact the repository owner.

