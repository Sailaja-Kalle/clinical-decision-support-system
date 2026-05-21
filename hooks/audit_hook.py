import os
from datetime import datetime

def audit_decision(patient_name, decision, risk_level):
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    audit_file = os.path.join(log_dir, "audit.log")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"[{timestamp}] Patient: {patient_name} | Decision: {decision} | Risk: {risk_level}\n"

    with open(audit_file, "a") as f:
        f.write(message)

    print(f"[AuditHook] Decision audited for {patient_name}")