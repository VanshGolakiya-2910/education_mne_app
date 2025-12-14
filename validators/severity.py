def compute_severity_score(qa_report):
    score = 0

    # Missing values
    missing_pct = sum(qa_report["missing_values_percent"].values())
    if missing_pct > 10:
        score += 3
    elif missing_pct > 0:
        score += 1

    # Bound violations
    if qa_report["bound_violations"] > 5:
        score += 3
    elif qa_report["bound_violations"] > 0:
        score += 1

    # Logic violations (very serious)
    if qa_report["logic_violations"] > 0:
        score += 5

    if score <= 1:
        return "LOW"
    elif score <= 4:
        return "MEDIUM"
    else:
        return "HIGH"
