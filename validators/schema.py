SCHEMA = {
    "country": str,
    "development_level": ["Least", "Less", "More"],
    "fragility": [0, 1],
    "education_level": ["Primary", "Lower Secondary", "Higher Secondary"],
    "gender": ["Male", "Female"],
    "rural": [True, False],
    "wealth_quintile": [1, 2, 3, 4, 5],
    "out_of_school_rate": "percentage",
    "attendance_rate": "percentage",
    "completion_rate": "percentage"
}

def validate_schema_df(df):
    errors = []

    for col in SCHEMA:
        if col not in df.columns:
            errors.append(f"Missing column: {col}")

    for col, allowed in SCHEMA.items():
        if isinstance(allowed, list):
            invalid = df[~df[col].isin(allowed)][col].unique()
            if len(invalid) > 0:
                errors.append(f"Invalid values in {col}: {list(invalid)}")

    return errors
