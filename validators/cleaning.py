import pandas as pd

BOUNDS = {
    "out_of_school_rate": (0, 100),
    "attendance_rate": (50, 100),
    "completion_rate": (0, 100)
}

def clean_dataset(df):
    audit = []

    for col, (low, high) in BOUNDS.items():
        mask = (df[col] < low) | (df[col] > high)
        for idx in df[mask].index:
            audit.append({
                "row": idx,
                "column": col,
                "original": df.loc[idx, col],
                "corrected": max(low, min(high, df.loc[idx, col]))
            })
            df.loc[idx, col] = max(low, min(high, df.loc[idx, col]))

    return df, pd.DataFrame(audit)
