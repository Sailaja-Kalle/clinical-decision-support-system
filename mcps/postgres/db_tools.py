from database.connection import SessionLocal
from database.models import Patient

def get_patient_history(patient_name):
    db = SessionLocal()
    try:
        patients = db.query(Patient).filter(
            Patient.name.ilike(f"%{patient_name}%")
        ).all()
        return [
            {
                "id": p.id,
                "name": p.name,
                "age": p.age,
                "oxygen": p.oxygen,
                "temperature": p.temperature,
                "created_at": str(p.created_at)
            }
            for p in patients
        ]
    finally:
        db.close()

def get_high_risk_patients():
    db = SessionLocal()
    try:
        patients = db.query(Patient).all()
        return [
            {
                "id": p.id,
                "name": p.name,
                "oxygen": p.oxygen,
                "temperature": p.temperature
            }
            for p in patients
            if p.oxygen and p.oxygen < 90
        ]
    finally:
        db.close()