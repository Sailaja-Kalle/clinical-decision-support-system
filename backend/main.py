from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi import Depends
from backend.schemas import PatientInput
from database.connection import get_db
from database.crud import save_patient, get_all_patients
from database.db import init_db
from agents.orchestration_agent import OrchestrationAgent
from hooks.validation_hook import validate_patient_data
from hooks.preprocessing_hook import preprocess_patient_data
from hooks.alert_hook import check_critical_alerts
from hooks.logging_hook import log_patient_event
from hooks.audit_hook import audit_decision
from hooks.postprocessing_hook import postprocess_result
from models.predict import predict_risk
from mcps.filesystem.server import FilesystemMCP
from mcps.postgres.server import PostgresMCP
from mcps.browser.server import BrowserMCP
from tools.report_generator import generate_patient_report

app = FastAPI(title="Clinical Decision Support System")

init_db()
orchestration = OrchestrationAgent()
filesystem_mcp = FilesystemMCP()
postgres_mcp = PostgresMCP()
browser_mcp = BrowserMCP()

@app.get("/")
def home():
    return {"message": "Clinical Decision Support System is running"}

@app.post("/patient")
def receive_patient(patient: PatientInput, db: Session = Depends(get_db)):
    patient_data = {
        "name": patient.name,
        "age": patient.age,
        "temperature": patient.temperature,
        "oxygen": patient.oxygen,
        "heart_rate": patient.heart_rate,
        "blood_pressure": patient.blood_pressure,
        "symptoms": patient.symptoms,
        "diabetes": patient.diabetes
    }

    validation = validate_patient_data(patient_data)
    if not validation["valid"]:
        raise HTTPException(status_code=400, detail=validation["errors"])

    patient_data = preprocess_patient_data(patient_data)
    log_patient_event("PATIENT_RECEIVED", patient_data)
    alert_result = check_critical_alerts(patient_data)
    saved = save_patient(db, patient)
    analysis = orchestration.process(patient_data)
    analysis = postprocess_result(analysis)
    ml_result = predict_risk(patient_data)
    analysis.update(ml_result)

    conditions = analysis.get("possible_conditions", ["general"])
    guidelines = browser_mcp.get_guidelines(conditions[0] if conditions else "general")
    analysis["guidelines"] = guidelines["guideline"]

    report = generate_patient_report(patient_data, analysis)
    report_path = filesystem_mcp.save_report(patient_data["name"], report)
    analysis["report_saved"] = report_path

    audit_decision(
        patient_data["name"],
        "AI Analysis Complete",
        analysis.get("risk_level", "UNKNOWN")
    )

    return {
        "message": "Patient analyzed successfully",
        "patient_id": saved.id,
        "patient_name": saved.name,
        "critical_alerts": alert_result["critical_alerts"],
        "analysis": analysis
    }

@app.get("/patients")
def get_patients(db: Session = Depends(get_db)):
    patients = get_all_patients(db)
    return patients

@app.get("/patient-history/{name}")
def get_patient_history(name: str):
    history = postgres_mcp.fetch_patient_history(name)
    return {"patient_history": history}

@app.get("/high-risk-patients")
def get_high_risk():
    patients = postgres_mcp.fetch_high_risk_patients()
    return {"high_risk_patients": patients}

@app.get("/reports")
def get_reports():
    reports = filesystem_mcp.list_all_reports()
    return {"reports": reports}