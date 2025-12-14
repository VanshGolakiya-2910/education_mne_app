def derive_all_indicators(df):
    indicators = {}

    indicators["Transition Drop-off"] = (
        df.pivot_table(
            index="country",
            columns="education_level",
            values="completion_rate",
            aggfunc="mean"
        )
        .assign(
            drop_primary_secondary=lambda x: x["Primary"] - x["Lower Secondary"],
            drop_secondary_higher=lambda x: x["Lower Secondary"] - x["Higher Secondary"]
        )
        .reset_index()
    )

    indicators["Gender Parity Index"] = (
        df.pivot_table(
            index=["country", "education_level"],
            columns="gender",
            values="completion_rate",
            aggfunc="mean"
        )
        .assign(GPI=lambda x: x["Female"] / x["Male"])
        .reset_index()
    )

    return indicators
