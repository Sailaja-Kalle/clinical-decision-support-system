import json
import os

def load_ranges():
    path = os.path.join(os.path.dirname(__file__), "ranges.json")
    with open(path) as f:
        return json.load(f)

def analyze_labs(lab_data):
    ranges = load_ranges()
    results = {}

    for test, value in lab_data.items():
        if test in ranges:
            r = ranges[test]
            if value < r["min"]:
                results[test] = "LOW"
            elif value > r["max"]:
                results[test] = "HIGH"
            else:
                results[test] = "NORMAL"

    return {"lab_results": results}