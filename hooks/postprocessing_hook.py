def postprocess_result(result):
    risk_score = result.get("risk_score", 0)

    if risk_score >= 70:
        result["risk_category"] = "HIGH PRIORITY"
        result["recommended_action"] = "Immediate ICU evaluation"
    elif risk_score >= 40:
        result["risk_category"] = "MEDIUM PRIORITY"
        result["recommended_action"] = "Doctor consultation within 1 hour"
    else:
        result["risk_category"] = "LOW PRIORITY"
        result["recommended_action"] = "Routine monitoring"

    return result