# VESIT: AI-Powered Smart Lighting System 🛰️

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![Streamlit](https://img.shields.io/badge/streamlit-%23FF4B4B.svg?style=for-the-badge&logo=streamlit&logoColor=white)

This repository contains a fully functional prototype for an intelligent street lighting system. The project uses a dedicated AI agent to ingest live weather data, make smart decisions about lighting levels, and provide a real-time dashboard for monitoring and control, all running within a single, unified Python application.

!

---
## ✨ Key Features

- **AI-Driven Automation:** The agent automatically adjusts streetlight brightness based on real-time conditions like precipitation, cloud cover, and time of day.
- **Live Control Dashboard:** An interactive web UI built with Streamlit for at-a-glance monitoring of the entire lighting fleet.
- **Dynamic Map Visualization:** An interactive map that visualizes each pole's location and status. The size and color intensity of each light change dynamically with its brightness.
- **Fault Highlighting:** Poles with a "Fault" status are highlighted with a distinct red outline on the map for immediate operator attention.
- **Human-in-the-Loop Control:** Operators can manually select any pole and override the AI's settings.
- **Resilience Testing:** A "Simulate Attack" feature demonstrates the system's ability to handle anomalous data by entering a pre-defined fail-safe state.
- **Live Weather & Log Viewer:** The dashboard displays live weather data fetched from the API and includes an integrated log viewer to see the agent's real-time activity.

---
## 🏗️ Architecture

This application utilizes a **multi-threaded architecture** within a single Python script to run both the backend API and the frontend dashboard simultaneously.

-   A **background thread** is dedicated to running the **Flask API server**. This thread handles all agent logic, database interactions, and communication with the external WeatherAPI.
-   The **main thread** runs the **Streamlit web application**. It queries the background API (running on `localhost`) to populate the user interface and send commands.

This design simplifies deployment and testing while still maintaining a logical separation between the data processing backend and the presentation frontend.

---
## 🚀 Setup and Run

### Prerequisites
- Python 3.8+
- Git
- An API key from [WeatherAPI.com](https://www.weatherapi.com/)

### Installation & Execution
1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
    cd your-repo-name
    ```
2.  **Create the environment file:**
    Create a file named `.env` in the main project folder and add your API key:
    ```ini
    WEATHER_API_KEY="your_actual_api_key_goes_here"
    ```
3.  **Set up the Virtual Environment and Install Dependencies:**
    ```bash
    # Create the virtual environment
    python -m venv venv

    # Activate it (use the command for your OS)
    # On Windows:
    venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    
    # Install all required packages
    pip install -r requirements.txt
    ```

4.  **Run the Application:**
    From the root project directory, run the following command. This single command starts both the backend server and the frontend dashboard.
    ```bash
    streamlit run app.py
    ```
    *Your web browser should open automatically with the live dashboard.*

---
## 📖 Usage Guide

- **Refresh Live Data:** Click this button in the sidebar to command the agent to fetch the latest weather data and recalculate brightness levels for the fleet.
- **Simulate Attack:** Click this to test the system's fail-safe response. The online poles will change to "Data Anomaly Detected" with 50% brightness. Click "Refresh Live Data" to return to normal operation.
- **Pole Management:** Select any pole from the dropdown to manually override its settings.

---
## 🗺️ Future Roadmap

This project provides a solid foundation for several advanced features:
- **Historical Analytics:** Store lighting and weather data over time in a database like SQLite to create charts for energy analysis and fault prediction.
- **Proactive Maintenance:** Automatically generate maintenance alerts for poles that are in a "Fault" state for an extended period.
- **Advanced Agent Logic:** Move from a rule-based system to a simple machine learning model (e.g., a decision tree) for more nuanced lighting decisions.
- **Dockerization:** Package the entire application into a Docker container for ultimate portability and one-command deployment.

---
## 📄 License
This project is licensed under the MIT License.
