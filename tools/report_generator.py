import json
import os
from datetime import datetime

def generate_patient_report(patient_data, analysis):
    report = {
        "report_id": f"RPT_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "patient": {
            "name": patient_data.get("name"),
            "age": patient_data.get("age"),
            "oxygen": patient_data.get("oxygen"),
            "temperature": patient_data.get("temperature"),
            "heart_rate": patient_data.get("heart_rate")
        },
        "analysis": analysis,
        "status": "COMPLETE"
    }
    return report