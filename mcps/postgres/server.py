from mcps.postgres.db_tools import get_patient_history, get_high_risk_patients

class PostgresMCP:
    def __init__(self):
        self.name = "PostgresMCP"

    def fetch_patient_history(self, patient_name):
        return get_patient_history(patient_name)

    def fetch_high_risk_patients(self):
        return get_high_risk_patients()