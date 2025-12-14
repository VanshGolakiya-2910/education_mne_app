import matplotlib.pyplot as plt
import pandas as pd


def plot_overview_completion(df):
    """
    2-panel figure:
    - Completion by education level
    - Rural–Urban completion gap
    """
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    # --- Plot 1: Completion by level ---
    df.groupby("education_level")["completion_rate"].mean().plot(
        kind="bar",
        ax=axes[0]
    )
    axes[0].set_title("Average Completion Rate by Education Level")
    axes[0].set_ylabel("Completion Rate (%)")
    axes[0].set_xlabel("Education Level")
    axes[0].tick_params(axis="x", rotation=20)
    axes[0].grid(axis="y", linestyle="--", alpha=0.5)

    # --- Plot 2: Rural–Urban gap ---
    pivot = df.pivot_table(
        index="education_level",
        columns="rural",
        values="completion_rate",
        aggfunc="mean"
    )

    (pivot[False] - pivot[True]).plot(
        kind="bar",
        ax=axes[1]
    )
    axes[1].set_title("Rural–Urban Completion Gap")
    axes[1].set_ylabel("Urban − Rural (pp)")
    axes[1].set_xlabel("Education Level")
    axes[1].tick_params(axis="x", rotation=20)
    axes[1].grid(axis="y", linestyle="--", alpha=0.5)

    plt.tight_layout()
    return fig


def plot_fragility_and_gender(df):
    """
    2-panel figure:
    - Fragility completion gap
    - Gender Parity Index (completion)
    """
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    # --- Plot 1: Fragility gap ---
    fragility = df.pivot_table(
        index="education_level",
        columns="fragility",
        values="completion_rate",
        aggfunc="mean"
    )

    (fragility[0] - fragility[1]).plot(
        marker="o",
        ax=axes[0]
    )
    axes[0].set_title("Completion Gap: Non-Fragile vs Fragile")
    axes[0].set_ylabel("Gap (pp)")
    axes[0].set_xlabel("Education Level")
    axes[0].grid(axis="y", linestyle="--", alpha=0.5)

    # --- Plot 2: Gender Parity Index ---
    gpi = (
        df.pivot_table(
            index="education_level",
            columns="gender",
            values="completion_rate",
            aggfunc="mean"
        )
        .assign(GPI=lambda x: x["Female"] / x["Male"])
    )

    gpi["GPI"].plot(
        kind="bar",
        ax=axes[1]
    )
    axes[1].axhline(1, linestyle="--")
    axes[1].set_title("Gender Parity Index (Completion)")
    axes[1].set_ylabel("GPI (Female / Male)")
    axes[1].set_xlabel("Education Level")
    axes[1].tick_params(axis="x", rotation=20)
    axes[1].grid(axis="y", linestyle="--", alpha=0.5)

    plt.tight_layout()
    return fig