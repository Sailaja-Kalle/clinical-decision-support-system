from mcps.browser.web_tools import search_medical_guidelines

class BrowserMCP:
    def __init__(self):
        self.name = "BrowserMCP"

    def get_guidelines(self, condition):
        return search_medical_guidelines(condition)