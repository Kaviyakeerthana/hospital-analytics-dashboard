import pandas as pd
import numpy as np
from datetime import timedelta

from config import (
    START_DATE,
    END_DATE
)

# Load fact_admissions (must already be generated)
fact_admissions = pd.read_csv("../output/fact_admissions.csv")

# Generate discharge dates

fact_discharge = pd.DataFrame()

fact_discharge["admission_id"] = fact_admissions["admission_id"]
fact_discharge["patient_id"] = fact_admissions["patient_id"]

# Convert admission_date to datetime
admission_dates = pd.to_datetime(fact_admissions["admission_date"])

# Actual LOS varies around expected LOS
actual_los = (
    fact_admissions["expected_los"]
    + np.random.randint(-1, 4, size=len(fact_admissions))
).clip(lower=1)

fact_discharge["actual_los"] = actual_los

# Discharge date = admission_date + actual_los
fact_discharge["discharge_date"] = admission_dates + pd.to_timedelta(actual_los, unit="D")

# Random discharge time
fact_discharge["discharge_time"] = np.random.choice(
    pd.date_range("08:00", "22:00", freq="30min").strftime("%H:%M"),
    size=len(fact_discharge)
)

# Patient outcome
fact_discharge["patient_outcome"] = np.random.choice(
    ["Recovered", "Improved", "Transferred", "Deceased"],
    size=len(fact_discharge),
    p=[0.65, 0.20, 0.10, 0.05]
)

# Discharge type
fact_discharge["discharge_type"] = np.random.choice(
    ["Normal", "AMA", "Transfer"],
    size=len(fact_discharge),
    p=[0.85, 0.10, 0.05]
)

# Validation
assert fact_discharge["discharge_date"].notna().all()
assert (fact_discharge["actual_los"] > 0).all()

# Save
fact_discharge.to_csv("../output/fact_discharge.csv", index=False)

print("✅ fact_discharge generated successfully")