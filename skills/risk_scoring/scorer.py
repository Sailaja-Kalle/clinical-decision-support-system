from skills.risk_scoring.calculator import calculate_risk_score

def get_risk(data):
    return calculate_risk_score(data)