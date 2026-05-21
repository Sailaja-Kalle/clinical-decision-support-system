from sqlalchemy.orm import Session
from database.models import Patient
from backend.schemas import PatientInput
import json

def save_patient(db: Session, patient: PatientInput):
    db_patient = Patient(
        name=patient.name,
        age=patient.age,
        temperature=patient.temperature,
        oxygen=patient.oxygen,
        blood_pressure=patient.blood_pressure,
        heart_rate=patient.heart_rate,
        symptoms=json.dumps(patient.symptoms)
    )
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

def get_all_patients(db: Session):
    return db.query(Patient).all()