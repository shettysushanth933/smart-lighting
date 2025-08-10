# VESIT-NG: AI-Powered Smart Lighting System 🛰️

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![Streamlit](https://img.shields.io/badge/streamlit-%23FF4B4B.svg?style=for-the-badge&logo=streamlit&logoColor=white)

This repository contains a Proof-of-Concept for an intelligent street lighting system. The project uses a dedicated AI agent to ingest live weather data, make smart decisions about lighting levels, and provide a real-time dashboard for monitoring and control.



---
## ✨ Key Features

- **AI-Driven Automation:** The agent automatically adjusts streetlight brightness based on real-time conditions like precipitation, cloud cover, and time of day.
- **Live Control Dashboard:** An interactive web UI built with Streamlit for at-a-glance monitoring of the entire lighting fleet.
- **Dynamic Map Visualization:** An interactive map that visualizes each pole's location and status. The size and color intensity of each light change dynamically with its brightness.
- **Fault Highlighting:** Poles with a "Fault" status are highlighted with a distinct red outline on the map for immediate operator attention.
- **Human-in-the-Loop Control:** Operators can manually select any pole and override the AI's settings.
- **Resilience Testing:** A "Simulate Attack" feature demonstrates the system's ability to handle anomalous data by entering a pre-defined fail-safe state.
- **Live Weather Panel:** The dashboard sidebar shows live weather data fetched from the API, making the agent's "senses" visible to the user.

---
## 🏗️ Architecture

The system uses a decoupled frontend/backend architecture, which is robust and scalable. The backend can be run independently of the frontend, and they communicate via a REST API.

```
+------------------+     +----------------+     +-----------------+
| WeatherAPI.com   | --> | Flask Backend  | <-- | Streamlit       |
| (External Data)  |     | (AI Agent, DB) | --> |  Frontend       |
+------------------+     +----------------+     | (Dashboard UI)  |
                               ^                      ^
                               |                      |
                               +----------------------+
                                     (User via Browser)
```

---
## 🚀 Getting Started

You will need two separate terminals to run the backend and frontend.

### Prerequisites
- Python 3.8+
- Git
- An API key from [WeatherAPI.com](https://www.weatherapi.com/)

### Setup & Installation
1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/shettysushanth933/smart-lighting.git](https://github.com/shettysushanth933/smart-lighting.git)
    cd your-repo-name
    ```
2.  **Create the environment file:**
    Create a file named `.env` in the main project folder and add your API key:
    ```ini
    WEATHER_API_KEY="your_actual_api_key_goes_here"
    ```

3.  **Set up the Backend:**
    ```bash
    cd backend
    python -m venv venv
    source venv/bin/activate  # Or `venv\Scripts\activate` on Windows
    pip install -r requirements.txt
    python api.py
    ```
    *The backend will now be running on `http://127.0.0.1:5000`. Leave this terminal open.*

4.  **Set up the Frontend (in a new terminal):**
    ```bash
    cd frontend
    python -m venv venv
    source venv/bin/activate  # Or `venv\Scripts\activate` on Windows
    pip install -r requirements.txt
    streamlit run dashboard.py
    ```
    *Your browser should open with the live dashboard.*

---
## 🗺️ Future Roadmap

This project provides a solid foundation for several advanced features:
- **Historical Analytics:** Store lighting and weather data over time in a database like SQLite to create charts for energy analysis and fault prediction.
- **Proactive Maintenance:** Automatically generate maintenance alerts for poles that are in a "Fault" state for an extended period.
- **Advanced Agent Logic:** Move from a rule-based system to a simple machine learning model (e.g., a decision tree) for more nuanced lighting decisions.
- **Dockerization:** Package the backend and frontend into Docker containers for easy, one-command deployment using `docker-compose`.

---
## 📄 License
This project is licensed under the MIT License.
