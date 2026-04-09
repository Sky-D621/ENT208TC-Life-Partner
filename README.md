# Focus Buddy 🎯

> An empathetic, AI-powered study timer designed to intervene in academic anxiety and deadline paralysis through cognitive micro-tasks.

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📖 Project Overview (项目简介)

Traditional productivity applications (e.g., Forest, strict app blockers) rely on negative reinforcement and punitive measures to maintain user focus. However, recent psychological insights indicate that academic procrastination often stems from emotional dysregulation and task anxiety rather than a mere lack of discipline.

**Focus Buddy** is a web-based intervention platform that rethinks the Pomodoro technique. Built entirely on Python and Streamlit, it replaces punitive lock-outs with an **"Empathy Intervention System"**. When users experience cognitive overload, they can trigger a distress state. The backend instantly captures their emotional context and leverages an LLM (Large Language Model) to generate a customized, low-friction micro-task (<40 words) to bridge the gap between anxiety and task resumption.

## ✨ Core Features (核心功能)

* **⏳ Non-Punitive Pomodoro Engine:** A robust countdown timer integrated with Streamlit's `session_state` to ensure stable time tracking across asynchronous UI updates and browser re-renders.
* **🆘 Distress Trigger & Low-Friction Logging:** A prominent intervention button coupled with quick-tap emotion tags (e.g., 😰 Anxious, 🥱 Bored, 🤯 Overwhelmed) to capture user context without demanding high cognitive load (typing).
* **🧠 LLM-Driven Cognitive Scaffolding:** Backend integration with Large Language Models via API. The system dynamically injects strict psychological system prompts to ensure the AI acts as a behavioral coach, providing immediate, physical micro-actions rather than generic motivational text.
* **📊 Local Telemetry & Analytics:** A lightweight, dependency-free local data logging mechanism (`logger.py`). It automatically appends session duration, interruption timestamps, and emotional triggers to a local `.csv` file for continuous behavioral analysis.

## 🏗️ Technical Architecture (技术架构)

This application is engineered as a lightweight, full-stack Python application, optimized for rapid iteration and deployment.

* **Frontend:** `Streamlit` (Declarative Python UI framework)
* **Backend Logic:** Pure `Python` standard libraries
* **AI Engine:** DeepSeek / Kimi / OpenAI Compatible API
* **Data Persistence:** Local flat-file storage (`CSV`/`JSON`)

## 🚀 Installation & Setup (本地部署指南)

Follow these steps to run Focus Buddy locally on your machine.

### 1. Clone the Repository

```
git clone https://github.com/Sky-D621/ENT208TC-Focus-Buddy.git
cd ENT208TC-Focus-Buddy
```

### 2. Set Up a Virtual Environment (Recommended)

It is highly recommended to isolate project dependencies using Python's built-in `venv`.

```
# Create a virtual environment named 'venv'
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

Install the required Python packages using `pip`.

```
pip install streamlit requests python-dotenv
```

### 4. Environment Variables Configuration

To keep API keys secure, Focus Buddy uses environment variables. Create a `.env` file in the root directory of the project and add your LLM API credentials.

```
# Create a .env file
touch .env
```

Inside the `.env` file, add the following (replace `your_api_key_here` with your actual key):

```
LLM_API_KEY=your_api_key_here
LLM_BASE_URL=https://api.deepseek.com/v1
```

### 5. Run the Application

Launch the Streamlit server. The application will automatically open in your default web browser at `http://localhost:8501`.

```
streamlit run app.py
```

## 📁 Directory Structure (目录结构)

```
ENT208TC-Focus-Buddy/
│
├── app.py                # Main Streamlit application and UI routing
├── ai_coach.py           # LLM API integration and System Prompt logic
├── logger.py             # Local CSV data persistence handlers
├── requirements.txt      # Python package dependencies
├── .env.example          # Example environment variables template
├── .gitignore            # Git ignore rules (excludes .env and data files)
└── README.md             # Project documentation
```

## 🔒 Data Privacy Statement (数据隐私说明)

Focus Buddy respects user privacy. All behavioral data, focus session durations, and emotional trigger logs are stored **locally** on the user's machine within a generated `focus_data.csv` file. No personal telemetry data is transmitted to external servers, with the sole exception of the anonymized emotional tags sent to the LLM API strictly for generating recovery interventions.

*Focus Buddy - Act, Don't Just Answer.*