import streamlit as st
import requests
import json
import os
from datetime import datetime

API_URL = "https://clinical-decision-backend.onrender.com"

st.set_page_config(
    page_title="Clinical Decision Support System",
    page_icon="🏥",
    layout="wide"
)

st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #1a0a2e 0%, #16213e 50%, #0f3460 100%); }
    .header-box {
        background: linear-gradient(90deg, #6a0572, #a855f7, #38bdf8);
        padding: 22px 30px; border-radius: 15px; margin-bottom: 25px;
        text-align: center; box-shadow: 0 0 30px rgba(168, 85, 247, 0.4);
    }
    .header-box h1 { color: white; font-size: 2.2em; margin: 0; text-shadow: 0 0 20px rgba(255,255,255,0.3); }
    .header-box p { color: #e0b8ff; margin: 5px 0 0 0; }
    .metric-card {
        background: linear-gradient(135deg, #2d1b4e, #1e2a4a);
        border: 1px solid #7c3aed; border-radius: 12px; padding: 18px;
        text-align: center; margin: 5px; box-shadow: 0 0 15px rgba(124, 58, 237, 0.2);
    }
    .metric-label { color: #c084fc; font-size: 0.85em; text-transform: uppercase; letter-spacing: 1px; }
    .metric-value { font-size: 2em; font-weight: bold; margin: 8px 0; }
    .metric-high { color: #f472b6; text-shadow: 0 0 10px rgba(244,114,182,0.5); }
    .metric-medium { color: #fb923c; text-shadow: 0 0 10px rgba(251,146,60,0.5); }
    .metric-low { color: #34d399; text-shadow: 0 0 10px rgba(52,211,153,0.5); }
    .metric-blue { color: #38bdf8; text-shadow: 0 0 10px rgba(56,189,248,0.5); }
    .alert-critical {
        background: linear-gradient(90deg, #4a0030, #6b0045);
        border-left: 5px solid #f472b6; border-radius: 8px; padding: 15px 20px;
        color: #f9a8d4; font-weight: bold; font-size: 1.1em; margin: 15px 0;
        box-shadow: 0 0 20px rgba(244,114,182,0.3);
    }
    .summary-box {
        background: linear-gradient(135deg, #1e1040, #162040);
        border: 1px solid #7c3aed; border-left: 4px solid #a855f7;
        border-radius: 10px; padding: 18px; color: #e0c3ff;
        line-height: 1.7; margin: 10px 0; box-shadow: 0 0 15px rgba(168,85,247,0.15);
    }
    .condition-tag {
        display: inline-block; background: linear-gradient(90deg, #2d1b4e, #1a1040);
        color: #c084fc; border: 1px solid #7c3aed; border-radius: 20px;
        padding: 6px 16px; margin: 4px; font-size: 0.9em;
        box-shadow: 0 0 8px rgba(124,58,237,0.3);
    }
    .action-box {
        background: linear-gradient(135deg, #0c2a3a, #0a1f30);
        border: 1px solid #0ea5e9; border-left: 4px solid #38bdf8;
        border-radius: 10px; padding: 15px 20px; color: #7dd3fc;
        font-size: 1em; margin: 10px 0; box-shadow: 0 0 15px rgba(56,189,248,0.15);
    }
    .guideline-box {
        background: linear-gradient(135deg, #2a0a3a, #1a0828);
        border: 1px solid #a855f7; border-left: 4px solid #c084fc;
        border-radius: 10px; padding: 15px 20px; color: #d8b4fe;
        margin: 10px 0; box-shadow: 0 0 15px rgba(192,132,252,0.15);
    }
    .section-title {
        color: #c084fc; font-size: 1em; font-weight: 600;
        margin: 20px 0 8px 0; text-transform: uppercase; letter-spacing: 2px;
        text-shadow: 0 0 10px rgba(192,132,252,0.5);
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a1f3a, #0d2744, #0a2040) !important;
        border-right: 2px solid #38bdf8 !important;
    }
    [data-testid="stSidebar"] > div:first-child {
        background: linear-gradient(180deg, #0a1f3a, #0d2744, #0a2040) !important;
    }
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a1f3a, #0d2744, #0a2040) !important;
    }
    section[data-testid="stSidebar"] p { color: #38bdf8 !important; font-weight: 600 !important; }
    section[data-testid="stSidebar"] label { color: #f9a8d4 !important; font-weight: 500 !important; }
    section[data-testid="stSidebar"] span { color: #7dd3fc !important; }
    section[data-testid="stSidebar"] div { color: #e0f2ff !important; }
    section[data-testid="stSidebar"] .stSelectbox > div > div {
        background: #0d2744 !important; border: 1px solid #38bdf8 !important;
        color: #f9a8d4 !important; border-radius: 8px !important;
    }
    .stTextInput input, .stNumberInput input {
        background-color: #1e1040 !important; color: #e0c3ff !important;
        border: 1px solid #7c3aed !important; border-radius: 8px !important;
    }
    .stMultiSelect > div { background-color: #1e1040 !important; border: 1px solid #7c3aed !important; }
    .stTextArea textarea {
        background-color: #1e1040 !important; color: #e0c3ff !important;
        border: 1px solid #7c3aed !important; border-radius: 8px !important;
    }
    label { color: #c084fc !important; }
    .stCheckbox label { color: #e0c3ff !important; font-size: 1em !important; }
    .stCheckbox span { color: #e0c3ff !important; }
    [data-testid="stCheckbox"] label p { color: #e0c3ff !important; }
    .stButton > button {
        background: linear-gradient(90deg, #7c3aed, #a855f7, #38bdf8) !important;
        color: white !important; border: none !important; border-radius: 10px !important;
        padding: 12px 30px !important; font-size: 1em !important;
        font-weight: bold !important; width: 100% !important;
        box-shadow: 0 0 20px rgba(168,85,247,0.4) !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        background: linear-gradient(90deg, #0d2744, #0a1f38) !important;
        border-radius: 10px !important;
        padding: 5px !important;
    }
    .stTabs [data-baseweb="tab"] {
        color: #f9a8d4 !important;
        font-weight: 600 !important;
        font-size: 1em !important;
        border-radius: 8px !important;
        padding: 8px 20px !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #7c3aed, #38bdf8) !important;
        color: white !important;
    }
    .stTabs [data-baseweb="tab-highlight"] {
        background: transparent !important;
    }

</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-box">
    <h1>🏥 Clinical Decision Support System</h1>
    <p>AI-Powered Patient Analysis Platform</p>
</div>
""", unsafe_allow_html=True)

# Sidebar Quick Stats
st.sidebar.markdown("---")
try:
    patients_resp = requests.get(f"{API_URL}/patients", timeout=2)
    all_patients = patients_resp.json()
    total_patients = len(all_patients)

    risk_resp = requests.get(f"{API_URL}/high-risk-patients", timeout=2)
    risk_data = risk_resp.json()
    high_risk = len(risk_data.get("high_risk_patients", []))

    reports_resp = requests.get(f"{API_URL}/reports", timeout=2)
    reports_data = reports_resp.json()
    total_reports = len(reports_data.get("reports", []))

    st.sidebar.markdown(f"""
    <div style="background:linear-gradient(135deg,#0d2744,#0a1f38);border:1px solid #38bdf8;
    border-radius:12px;padding:15px;margin:10px 0;">
        <div style="color:#38bdf8;font-size:0.8em;text-transform:uppercase;
        letter-spacing:1px;margin-bottom:10px;">⚡ Quick Stats</div>
        <div style="display:flex;justify-content:space-between;margin:8px 0;">
            <span style="color:#c084fc;">👥 Total Patients</span>
            <span style="color:#f9a8d4;font-weight:bold;">{total_patients}</span>
        </div>
        <div style="display:flex;justify-content:space-between;margin:8px 0;">
            <span style="color:#c084fc;">🚨 High Risk</span>
            <span style="color:#f472b6;font-weight:bold;">{high_risk}</span>
        </div>
        <div style="display:flex;justify-content:space-between;margin:8px 0;">
            <span style="color:#c084fc;">📁 Reports</span>
            <span style="color:#7dd3fc;font-weight:bold;">{total_reports}</span>
        </div>
        <div style="margin-top:10px;padding-top:8px;border-top:1px solid #1e3a5f;">
            <span style="color:#34d399;font-size:0.85em;">🟢 System Online</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
except:
    st.sidebar.markdown("""
    <div style="background:#1a0a2e;border:1px solid #f472b6;border-radius:10px;padding:12px;">
        <span style="color:#f472b6;">🔴 Backend Offline</span>
    </div>
    """, unsafe_allow_html=True)

st.sidebar.markdown("---")

menu = st.sidebar.selectbox("🧭 Navigation", [
    "🔍 Submit Patient",
    "👥 All Patients",
    "🚨 High Risk Patients",
    "📁 Reports",
    "💬 Feedback & Queries"
])

# ── Submit Patient ──────────────────────────────────────────
if menu == "🔍 Submit Patient":
    st.markdown('<div class="section-title">📋 New Patient Analysis</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("👤 Patient Name")
        age = st.number_input("🎂 Age", min_value=0, max_value=120, value=30)
        temperature = st.number_input("🌡️ Temperature (F)", min_value=90.0, max_value=115.0, value=98.6)
        oxygen = st.number_input("💨 Oxygen (%)", min_value=0.0, max_value=100.0, value=98.0)

    with col2:
        heart_rate = st.number_input("❤️ Heart Rate", min_value=0, max_value=300, value=80)
        blood_pressure = st.text_input("🩺 Blood Pressure", value="120/80")
        diabetes = st.checkbox("🩸 Has Diabetes")
        symptoms = st.multiselect("🤒 Symptoms (select from list)", [
            "fever", "cough", "chest pain", "shortness of breath",
            "headache", "dizziness", "palpitations", "chills",
            "nausea", "vomiting", "fatigue", "weakness",
            "sweating", "back pain", "abdominal pain", "swelling"
        ])
        extra = st.text_input("✏️ Type additional symptoms (comma separated)",
                              placeholder="e.g. joint pain, blurred vision, rash")
        if extra:
            typed = [s.strip().lower() for s in extra.split(",") if s.strip()]
            symptoms = symptoms + typed

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🔍 Analyze Patient"):
        if not name:
            st.error("⚠️ Please enter patient name!")
        else:
            payload = {
                "name": name, "age": int(age),
                "temperature": float(temperature), "oxygen": float(oxygen),
                "heart_rate": int(heart_rate), "blood_pressure": blood_pressure,
                "symptoms": symptoms, "diabetes": diabetes
            }
            with st.spinner("🤖 AI is analyzing patient..."):
                try:
                    response = requests.post(f"{API_URL}/patient", json=payload)
                    result = response.json()
                    analysis = result.get("analysis", {})
                    risk_level = analysis.get("risk_level", "LOW")

                    risk_color = "metric-high" if risk_level == "HIGH" else "metric-medium" if risk_level == "MEDIUM" else "metric-low"
                    risk_icon = "🔴" if risk_level == "HIGH" else "🟡" if risk_level == "MEDIUM" else "🟢"
                    ml_color = "metric-high" if analysis.get("ml_risk_prediction") == "HIGH" else "metric-low"

                    c1, c2, c3, c4 = st.columns(4)
                    with c1:
                        st.markdown(f'<div class="metric-card"><div class="metric-label">Risk Level</div><div class="metric-value {risk_color}">{risk_icon} {risk_level}</div></div>', unsafe_allow_html=True)
                    with c2:
                        st.markdown(f'<div class="metric-card"><div class="metric-label">Risk Score</div><div class="metric-value metric-blue">{analysis.get("risk_score", 0)}</div></div>', unsafe_allow_html=True)
                    with c3:
                        st.markdown(f'<div class="metric-card"><div class="metric-label">ML Prediction</div><div class="metric-value {ml_color}">{analysis.get("ml_risk_prediction", "N/A")}</div></div>', unsafe_allow_html=True)
                    with c4:
                        st.markdown(f'<div class="metric-card"><div class="metric-label">ML Probability</div><div class="metric-value metric-blue">{analysis.get("ml_risk_probability", 0)}%</div></div>', unsafe_allow_html=True)

                    if analysis.get("alert"):
                        st.markdown(f'<div class="alert-critical">🚨 {analysis.get("alert_message")}</div>', unsafe_allow_html=True)

                    st.markdown('<div class="section-title">📝 Clinical Summary</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="summary-box">{analysis.get("summary", "No summary available")}</div>', unsafe_allow_html=True)

                    st.markdown('<div class="section-title">🩺 Possible Conditions</div>', unsafe_allow_html=True)
                    conditions_html = "".join([f'<span class="condition-tag">• {c}</span>' for c in analysis.get("possible_conditions", [])])
                    st.markdown(conditions_html, unsafe_allow_html=True)

                    st.markdown('<div class="section-title">✅ Recommended Action</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="action-box">💊 {analysis.get("recommended_action", "N/A")}</div>', unsafe_allow_html=True)

                    st.markdown('<div class="section-title">📚 Clinical Guidelines</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="guideline-box">📖 {analysis.get("guidelines", "N/A")}</div>', unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"❌ Error: {e}")

# ── All Patients ────────────────────────────────────────────
elif menu == "👥 All Patients":
    st.markdown('<div class="section-title">👥 All Patients</div>', unsafe_allow_html=True)
    try:
        response = requests.get(f"{API_URL}/patients")
        patients = response.json()
        if patients:
            st.markdown(f'<div class="summary-box">📊 Total patients in database: <b>{len(patients)}</b></div>', unsafe_allow_html=True)
            import pandas as pd
            df = pd.DataFrame(patients)
            cols = ["id", "name", "age", "oxygen", "temperature", "heart_rate", "created_at"]
            cols = [c for c in cols if c in df.columns]
            st.dataframe(df[cols], use_container_width=True)
        else:
            st.info("No patients found.")
    except Exception as e:
        st.error(f"❌ Error: {e}")

# ── High Risk Patients ──────────────────────────────────────
elif menu == "🚨 High Risk Patients":
    st.markdown('<div class="section-title">🚨 High Risk Patients</div>', unsafe_allow_html=True)
    try:
        response = requests.get(f"{API_URL}/high-risk-patients")
        data = response.json()
        patients = data.get("high_risk_patients", [])
        if patients:
            st.markdown(f'<div class="alert-critical">⚠️ {len(patients)} high risk patients detected!</div>', unsafe_allow_html=True)
            import pandas as pd
            df = pd.DataFrame(patients)
            st.dataframe(df, use_container_width=True)
        else:
            st.markdown('<div class="action-box">✅ No high risk patients currently.</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"❌ Error: {e}")

# ── Reports ─────────────────────────────────────────────────
elif menu == "📁 Reports":
    st.markdown('<div class="section-title">📁 Saved Reports</div>', unsafe_allow_html=True)
    try:
        response = requests.get(f"{API_URL}/reports")
        data = response.json()
        reports = data.get("reports", [])
        if reports:
            st.markdown(f'<div class="summary-box">📂 Total reports saved: <b>{len(reports)}</b></div>', unsafe_allow_html=True)

            selected = st.selectbox("📄 Select a report to view:", reports)

            if selected:
                report_path = os.path.join("reports", selected)
                try:
                    with open(report_path, "r") as f:
                        report_data = json.load(f)

                    patient = report_data.get("patient", {})
                    analysis = report_data.get("analysis", {})
                    risk_level = analysis.get("risk_level", "LOW")
                    risk_color = "metric-high" if risk_level == "HIGH" else "metric-medium" if risk_level == "MEDIUM" else "metric-low"
                    risk_icon = "🔴" if risk_level == "HIGH" else "🟡" if risk_level == "MEDIUM" else "🟢"

                    st.markdown("---")
                    st.markdown(f'<div class="section-title">👤 Patient: {patient.get("name")} | Age: {patient.get("age")} | Report: {report_data.get("report_id")}</div>', unsafe_allow_html=True)

                    c1, c2, c3, c4 = st.columns(4)
                    with c1:
                        st.markdown(f'<div class="metric-card"><div class="metric-label">Risk Level</div><div class="metric-value {risk_color}">{risk_icon} {risk_level}</div></div>', unsafe_allow_html=True)
                    with c2:
                        st.markdown(f'<div class="metric-card"><div class="metric-label">Risk Score</div><div class="metric-value metric-blue">{analysis.get("risk_score", 0)}</div></div>', unsafe_allow_html=True)
                    with c3:
                        st.markdown(f'<div class="metric-card"><div class="metric-label">Oxygen</div><div class="metric-value metric-blue">{patient.get("oxygen")}%</div></div>', unsafe_allow_html=True)
                    with c4:
                        st.markdown(f'<div class="metric-card"><div class="metric-label">Temperature</div><div class="metric-value metric-blue">{patient.get("temperature")}F</div></div>', unsafe_allow_html=True)

                    st.markdown('<div class="section-title">📝 Clinical Summary</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="summary-box">{analysis.get("summary", "N/A")}</div>', unsafe_allow_html=True)

                    st.markdown('<div class="section-title">🩺 Conditions & Actions</div>', unsafe_allow_html=True)
                    conditions_html = "".join([f'<span class="condition-tag">• {c}</span>' for c in analysis.get("possible_conditions", [])])
                    st.markdown(conditions_html, unsafe_allow_html=True)

                    st.markdown(f'<div class="action-box">💊 {analysis.get("recommended_action", "N/A")}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="guideline-box">📖 {analysis.get("guidelines", "N/A")}</div>', unsafe_allow_html=True)

                    # Download button
                    st.markdown('<div class="section-title">⬇️ Download Report</div>', unsafe_allow_html=True)
                    st.download_button(
                        label="⬇️ Download JSON Report",
                        data=json.dumps(report_data, indent=2),
                        file_name=selected,
                        mime="application/json"
                    )

                    st.markdown('<div class="section-title">📋 Full Raw Report</div>', unsafe_allow_html=True)
                    st.json(report_data)

                except Exception as e:
                    st.error(f"Could not open report: {e}")
        else:
            st.info("No reports saved yet.")
    except Exception as e:
        st.error(f"❌ Error: {e}")

# ── Feedback & Queries ──────────────────────────────────────
elif menu == "💬 Feedback & Queries":
    st.markdown('<div class="section-title">💬 Feedback & Queries</div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📝 Submit Feedback", "📋 View All Feedback"])

    with tab1:
        st.markdown('<div class="summary-box">We value your feedback! Please share your thoughts or queries below.</div>', unsafe_allow_html=True)

        fb_name = st.text_input("👤 Your Name")
        fb_email = st.text_input("📧 Email (optional)", placeholder="your@email.com")
        fb_type = st.selectbox("📌 Type", ["General Feedback", "Bug Report", "Feature Request", "Query", "Other"])
        fb_message = st.text_area("💬 Your Message", placeholder="Write your feedback or query here...", height=150)

        if st.button("📤 Submit Feedback"):
            if not fb_name or not fb_message:
                st.error("⚠️ Please enter your name and message!")
            else:
                feedback_dir = "feedback"
                os.makedirs(feedback_dir, exist_ok=True)
                feedback_file = os.path.join(feedback_dir, "feedback.json")

                new_entry = {
                    "id": datetime.now().strftime("%Y%m%d%H%M%S"),
                    "name": fb_name,
                    "email": fb_email,
                    "type": fb_type,
                    "message": fb_message,
                    "submitted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

                existing = []
                if os.path.exists(feedback_file):
                    with open(feedback_file, "r") as f:
                        try:
                            existing = json.load(f)
                        except:
                            existing = []

                existing.append(new_entry)
                with open(feedback_file, "w") as f:
                    json.dump(existing, f, indent=2)

                st.success("✅ Thank you! Your feedback has been submitted successfully!")
                st.markdown(f'<div class="action-box">📌 Type: {fb_type}<br>👤 Name: {fb_name}<br>💬 Message: {fb_message}</div>', unsafe_allow_html=True)

    with tab2:
        feedback_file = os.path.join("feedback", "feedback.json")
        if os.path.exists(feedback_file):
            with open(feedback_file, "r") as f:
                try:
                    all_feedback = json.load(f)
                except:
                    all_feedback = []

            if all_feedback:
                st.markdown(f'<div class="summary-box">📊 Total feedback received: <b>{len(all_feedback)}</b></div>', unsafe_allow_html=True)
                for fb in reversed(all_feedback):
                    type_color = "#f472b6" if fb["type"] == "Bug Report" else "#38bdf8" if fb["type"] == "Query" else "#c084fc"
                    st.markdown(f"""
                    <div style="background:linear-gradient(135deg,#1e1040,#162040);
                    border:1px solid #7c3aed;border-left:4px solid {type_color};
                    border-radius:10px;padding:15px;margin:10px 0;">
                        <div style="display:flex;justify-content:space-between;margin-bottom:8px;">
                            <span style="color:#f9a8d4;font-weight:bold;">👤 {fb['name']}</span>
                            <span style="color:#7dd3fc;font-size:0.85em;">🕐 {fb['submitted_at']}</span>
                        </div>
                        <div style="margin-bottom:6px;">
                            <span style="color:{type_color};background:rgba(124,58,237,0.2);
                            padding:3px 10px;border-radius:12px;font-size:0.85em;">📌 {fb['type']}</span>
                        </div>
                        <div style="color:#e0c3ff;line-height:1.6;">{fb['message']}</div>
                        {f'<div style="color:#7dd3fc;font-size:0.85em;margin-top:6px;">📧 {fb["email"]}</div>' if fb.get('email') else ''}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No feedback submitted yet.")
        else:
            st.info("No feedback submitted yet.")