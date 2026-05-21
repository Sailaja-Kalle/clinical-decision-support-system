# 🏥 Clinical Decision Support System

> AI-powered healthcare platform for real-time patient analysis using multi-agent AI, machine learning, and large language models.

![Python](https://img.shields.io/badge/Python-3.14-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.136-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.57-red)
![Groq](https://img.shields.io/badge/LLM-Groq%20Llama3.1-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🌟 What This System Does

This system acts like an AI doctor assistant. When a patient's data is entered:

1. **Triage Agent** checks if the patient is critical
2. **Risk Agent** calculates a risk score (0-100)
3. **Diagnosis Agent** identifies possible conditions
4. **Alert Agent** sends critical alerts if needed
5. **ML Model** predicts risk using RandomForest
6. **Groq LLM** generates a clinical summary in doctor's language
7. **Report** is auto-saved as JSON
8. **Dashboard** shows everything visually

---

## 🚀 Features

| Feature | Description |
|---|---|
| 🤖 Multi-Agent AI | Triage, Risk, Diagnosis, Alert, Summary agents |
| 🧠 Machine Learning | RandomForest risk prediction (100% accuracy) |
| 💬 LLM Integration | Groq Llama 3.1 for clinical summaries |
| 🗄️ Database | SQLite with SQLAlchemy ORM |
| 🔧 Skills System | Risk scoring, symptom extraction, lab analysis |
| 🪝 Hooks Pipeline | Validation, preprocessing, audit, logging |
| 🛠️ MCP Tools | Filesystem, database, browser MCPs |
| 📊 Dashboard | Streamlit UI with pink/purple/skyblue theme |
| 📁 Reports | Auto-generated JSON reports with download |
| 💬 Feedback System | User feedback and queries storage |

---

## 🏗️ Project Structure


clinical-decision-support-system/
│
├── backend/                    # FastAPI backend
│   ├── main.py                 # Main app + all routes
│   ├── schemas.py              # Pydantic models
│   ├── config.py               # Configuration
│   └── middleware.py           # Middleware
│
├── agents/                     # AI Agents
│   ├── base_agent.py           # Base agent class
│   ├── triage_agent.py         # Triage logic
│   ├── risk_agent.py           # Risk scoring
│   ├── diagnosis_agent.py      # Diagnosis + LLM
│   ├── alert_agent.py          # Critical alerts
│   ├── summary_agent.py        # LLM summaries
│   └── orchestration_agent.py  # Coordinates all agents
│
├── skills/                     # Reusable Skills
│   ├── risk_scoring/           # Risk calculator
│   ├── symptom_extraction/     # Symptom rules
│   ├── lab_analysis/           # Lab ranges
│   ├── medication_checker/     # Drug interactions
│   └── summarization/          # Summary generator
│
├── hooks/                      # Pipeline Hooks
│   ├── validation_hook.py      # Input validation
│   ├── preprocessing_hook.py   # Data cleaning
│   ├── alert_hook.py           # Critical alerts
│   ├── logging_hook.py         # Event logging
│   ├── audit_hook.py           # Decision audit
│   └── postprocessing_hook.py  # Result enrichment
│
├── mcps/                       # MCP Servers
│   ├── filesystem/             # File operations
│   ├── postgres/               # Database queries
│   └── browser/                # Web guidelines
│
├── models/                     # ML Models
│   ├── train_model.py          # Model training
│   ├── predict.py              # Predictions
│   ├── preprocessing.py        # Data preprocessing
│   └── saved_models/           # Trained model files
│
├── database/                   # Database Layer
│   ├── connection.py           # DB connection
│   ├── models.py               # Table models
│   ├── crud.py                 # CRUD operations
│   └── db.py                   # DB initialization
│
├── dashboard/                  # Streamlit UI
│   └── app.py                  # Full dashboard
│
├── tools/                      # Utility Tools
│   ├── groq_client.py          # Groq LLM client
│   ├── report_generator.py     # Report creation
│   └── logger.py               # Logging utility
│
├── data/                       # Data Files
├── logs/                       # Log Files
├── reports/                    # Generated Reports
├── feedback/                   # User Feedback
├── .env                        # Environment variables
├── requirements.txt            # Dependencies
└── README.md                   # This file

---

## ⚙️ Tech Stack

| Layer | Technology | Version |
|---|---|---|
| Backend API | FastAPI + Uvicorn | 0.136 |
| Database | SQLite + SQLAlchemy | 2.0 |
| ML Model | Scikit-learn RandomForest | Latest |
| LLM | Groq (Llama 3.1 8B Instant) | Latest |
| Dashboard | Streamlit | 1.57 |
| Data Processing | Pandas + NumPy | Latest |
| Language | Python | 3.14 |

---

## 🛠️ Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/Sailaja-Kalle/clinical-decision-support-system.git
cd clinical-decision-support-system
```

### 2. Install dependencies
```bash
pip install fastapi uvicorn sqlalchemy pandas scikit-learn streamlit python-dotenv groq plotly requests httpx aiofiles
```

### 3. Set up environment variables
Create a `.env` file:
```env
GROQ_API_KEY=your_groq_api_key_here
DATABASE_URL=sqlite:///./patients.db
APP_NAME=Clinical Decision Support System
```

Get free Groq API key at: https://console.groq.com

### 4. Train the ML model
```bash
py -m models.train_model
```

### 5. Start the backend server
```bash
py -m uvicorn backend.main:app --reload
```
Backend runs at: http://127.0.0.1:8000

### 6. Start the dashboard
```bash
py -m streamlit run dashboard/app.py
```
Dashboard runs at: http://localhost:8501

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check |
| POST | `/patient` | Submit patient for AI analysis |
| GET | `/patients` | Get all patients |
| GET | `/high-risk-patients` | Get high risk patients |
| GET | `/patient-history/{name}` | Get patient history |
| GET | `/reports` | List all saved reports |

### Sample Patient Input
```json
{
  "name": "Ravi",
  "age": 65,
  "temperature": 103.0,
  "oxygen": 88.0,
  "blood_pressure": "140/90",
  "heart_rate": 120,
  "symptoms": ["fever", "cough", "shortness of breath"],
  "diabetes": true
}
```

### Sample AI Response
```json
{
  "message": "Patient analyzed successfully",
  "patient_id": 1,
  "analysis": {
    "risk_score": 85,
    "risk_level": "HIGH",
    "is_critical": true,
    "possible_conditions": ["Respiratory", "Cardiac"],
    "alert": true,
    "alert_message": "CRITICAL ALERT: Patient requires immediate attention!",
    "summary": "AI generated clinical summary...",
    "risk_category": "HIGH PRIORITY",
    "recommended_action": "Immediate ICU evaluation",
    "ml_risk_prediction": "HIGH",
    "ml_risk_probability": 100,
    "guidelines": "Administer oxygen therapy, monitor SpO2, chest X-ray recommended."
  }
}
```

---

## 📊 AI Analysis Pipeline

Patient Input
↓
Validation Hook (check required fields)
↓
Preprocessing Hook (clean & normalize data)
↓
Logging Hook (log patient event)
↓
Alert Hook (check critical vitals)
↓
┌─────────────────────────────┐
│     Orchestration Agent     │
│  ┌──────────────────────┐   │
│  │    Triage Agent      │   │
│  │    Risk Agent        │   │
│  │    Diagnosis Agent   │   │
│  │    Alert Agent       │   │
│  │    Summary Agent     │   │
│  │    (Groq LLM)        │   │
│  └──────────────────────┘   │
└─────────────────────────────┘
↓
ML Risk Prediction (RandomForest)
↓
Postprocessing Hook (add recommendations)
↓
MCP Tools (save report + get guidelines)
↓
Audit Hook (log decision)
↓
Final Response to Dashboard

---

## 📸 Dashboard Pages

| Page | Description |
|---|---|
| 🔍 Submit Patient | AI-powered patient analysis form |
| 👥 All Patients | Full patient database table |
| 🚨 High Risk Patients | Critical cases monitor |
| 📁 Reports | View and download JSON reports |
| 💬 Feedback & Queries | User feedback system |

### Sidebar Features
- ⚡ Quick Stats (Total Patients, High Risk, Reports)
- 🟢 System Online indicator

---

## 🔒 Environment Variables

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | Your Groq API key |
| `DATABASE_URL` | SQLite database URL |
| `APP_NAME` | Application name |

---

## 📄 License

MIT License — free to use, modify and distribute.

---

## 👩‍💻 Developer


- GitHub: [@Sailaja-Kalle](https://github.com/Sailaja-Kalle)

---

## ⭐ Support

If you find this project helpful, please give it a ⭐ on GitHub!

