import os
import json
from datetime import datetime

def save_patient_report(patient_name, report_data, folder="reports"):
    os.makedirs(folder, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{folder}/{patient_name}_{timestamp}.json"
    with open(filename, "w") as f:
        json.dump(report_data, f, indent=2)
    print(f"[FilesystemMCP] Report saved: {filename}")
    return filename

def read_patient_report(filename):
    with open(filename, "r") as f:
        data = json.load(f)
    return data

def list_reports(folder="reports"):
    if not os.path.exists(folder):
        return []
    return os.listdir(folder)