from mcps.filesystem.tools import save_patient_report, list_reports, read_patient_report

class FilesystemMCP:
    def __init__(self):
        self.name = "FilesystemMCP"

    def save_report(self, patient_name, data):
        return save_patient_report(patient_name, data)

    def list_all_reports(self):
        return list_reports()

    def read_report(self, filename):
        return read_patient_report(f"reports/{filename}")