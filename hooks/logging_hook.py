import os
from datetime import datetime

def log_patient_event(event_type, data):
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, "app.log")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"[{timestamp}] [{event_type}] Patient: {data.get('name', 'Unknown')} | Age: {data.get('age', 'N/A')}\n"

    with open(log_file, "a") as f:
        f.write(message)

    print(f"[LoggingHook] Event logged: {event_type}")