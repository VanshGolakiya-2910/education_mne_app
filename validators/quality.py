def run_quality_checks(df):
    return {
        "total_rows": len(df),
        "missing_values_percent": (df.isnull().mean() * 100).round(2).to_dict(),
        "bound_violations": int(
            ((df["attendance_rate"] > 100) | (df["attendance_rate"] < 50)).sum()
        ),
        "logic_violations": int(
            (df["completion_rate"] > df["attendance_rate"]).sum()
        )
    }
