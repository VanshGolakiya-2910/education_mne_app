import pandas as pd
import random

# =========================================================
# CONFIGURATION
# =========================================================

EDU_LEVELS = ["Primary", "Lower Secondary", "Higher Secondary"]
GENDERS = ["Male", "Female"]

COUNTRIES = [
    {"country": "Afghanistan", "dev": "Least", "fragile": True},
    {"country": "South Sudan", "dev": "Least", "fragile": True},
    {"country": "Chad", "dev": "Least", "fragile": True},
    {"country": "Somalia", "dev": "Least", "fragile": True},

    {"country": "Bangladesh", "dev": "Less", "fragile": False},
    {"country": "Nepal", "dev": "Less", "fragile": False},
    {"country": "Ethiopia", "dev": "Least", "fragile": False},
    {"country": "Uganda", "dev": "Least", "fragile": False},

    {"country": "India", "dev": "Less", "fragile": False},
    {"country": "Bhutan", "dev": "Less", "fragile": False},
    {"country": "Vietnam", "dev": "Less", "fragile": False},
    {"country": "Philippines", "dev": "Less", "fragile": False},
    {"country": "Morocco", "dev": "Less", "fragile": False},
    {"country": "Egypt", "dev": "Less", "fragile": False},

    {"country": "Bosnia and Herzegovina", "dev": "More", "fragile": False},
    {"country": "Serbia", "dev": "More", "fragile": False},
    {"country": "Poland", "dev": "More", "fragile": False},
    {"country": "Chile", "dev": "More", "fragile": False},
    {"country": "Malaysia", "dev": "More", "fragile": False},
]

# ---------------------------------------------------------
# BASELINES
# ---------------------------------------------------------

OSR_BASE = {
    "Least": (20, 40),
    "Less": (10, 25),
    "More": (3, 12)
}

ATTENDANCE_BASE = {
    "Primary": (85, 98),
    "Lower Secondary": (70, 90),
    "Higher Secondary": (60, 85)
}

COMPLETION_BASE = {
    "Primary": (80, 95),
    "Lower Secondary": (60, 80),
    "Higher Secondary": (40, 70)
}

# =========================================================
# GENERATOR FUNCTIONS
# =========================================================

def generate_osr(dev, wealth, rural, gender, fragile):
    osr = random.uniform(*OSR_BASE[dev])

    # Wealth (strong negative)
    osr -= wealth * random.uniform(1.5, 3.0)

    # Rural penalty
    if rural:
        osr += random.uniform(5, 15)

    # Gender (soft)
    if gender == "Female":
        osr += random.uniform(-2, 6)

    # Fragility penalty
    if fragile:
        osr += random.uniform(5, 15)

    return round(max(0, min(100, osr)), 1)


def generate_attendance(level, dev, wealth, gender, fragile):
    ar = random.uniform(*ATTENDANCE_BASE[level])

    # Development weak
    ar += random.uniform(-3, 3)

    # Wealth weak
    ar += random.uniform(-1, 4)

    # Conflict strong
    if fragile:
        ar -= random.uniform(5, 15)

    # Gender neutral
    ar += random.uniform(-2, 2)

    return round(max(50, min(100, ar)), 1)


def generate_completion(level, dev, wealth, rural, gender, fragile):
    cr = random.uniform(*COMPLETION_BASE[level])

    # Development strong
    if dev == "More":
        cr += random.uniform(5, 10)
    elif dev == "Least":
        cr -= random.uniform(5, 10)

    # Wealth strong
    cr += wealth * random.uniform(2, 5)

    # Rural penalty
    if rural:
        cr -= random.uniform(10, 25)

    # Gender by level
    if level == "Higher Secondary" and gender == "Female":
        cr += random.uniform(2, 6)
    elif level == "Lower Secondary":
        cr += random.uniform(-3, 3)

    # Fragility penalty
    if fragile:
        cr -= random.uniform(5, 15)

    return round(max(30, min(100, cr)), 1)


# =========================================================
# MAIN DATA GENERATION
# =========================================================

rows = []

for c in COUNTRIES:
    for level in EDU_LEVELS:
        for gender in GENDERS:
            rural = random.choice([True, False])
            wealth = random.randint(1, 5)

            osr = generate_osr(c["dev"], wealth, rural, gender, c["fragile"])
            ar = generate_attendance(level, c["dev"], wealth, gender, c["fragile"])
            cr = generate_completion(level, c["dev"], wealth, rural, gender, c["fragile"])

            # -------------------------------------------------
            # CONSISTENCY ENFORCEMENT
            # -------------------------------------------------

            ar = min(ar, 100 - osr)
            cr = min(cr, ar)

            rows.append({
                "country": c["country"],
                "development_level": c["dev"],
                "fragility": int(c["fragile"]),
                "education_level": level,
                "gender": gender,
                "rural": rural,
                "wealth_quintile": wealth,
                "out_of_school_rate": osr,
                "attendance_rate": ar,
                "completion_rate": cr
            })

df = pd.DataFrame(rows)
df.to_csv("synthetic_education_monitoring_data.csv", index=False)

# =========================================================
# INTENTIONAL DATA QUALITY ISSUES (FOR QA TESTING)
# =========================================================

# 1. Introduce missing attendance values (5%)
for idx in df.sample(frac=0.05, random_state=42).index:
    df.loc[idx, "attendance_rate"] = None

# 2. Introduce completion > attendance (2%)
for idx in df.sample(frac=0.02, random_state=24).index:
    if pd.notna(df.loc[idx, "attendance_rate"]):
        df.loc[idx, "completion_rate"] = df.loc[idx, "attendance_rate"] + random.uniform(1, 5)

# 3. Introduce OSR + AR > 100 (1%)
for idx in df.sample(frac=0.01, random_state=7).index:
    if pd.notna(df.loc[idx, "attendance_rate"]):
        df.loc[idx, "attendance_rate"] = min(
            100,
            df.loc[idx, "attendance_rate"] + random.uniform(5, 10)
        )


print("Synthetic education monitoring dataset generated successfully.")
