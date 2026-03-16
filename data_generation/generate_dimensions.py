import pandas as pd
import numpy as np
from datetime import datetime

from config import (
    BRANCHES,
    DEPARTMENTS,
    START_DATE,
    END_DATE,
    NUM_PATIENTS,
    NUM_DOCTORS,
    AGE_GROUPS,
    INSURANCE_TYPES,
    RISK_CATEGORIES
)
# dim_branch

dim_branch = pd.DataFrame(
    BRANCHES,
    columns=["branch_id", "branch_name", "city", "total_beds", "icu_beds"]
)

# validation
assert (dim_branch["icu_beds"] <= dim_branch["total_beds"]).all()


# dim_department

dim_department = pd.DataFrame({
    "department_id": range(1, len(DEPARTMENTS) + 1),
    "department_name": DEPARTMENTS
})

# dim_date
dates = pd.date_range(start=START_DATE, end=END_DATE)

dim_date = pd.DataFrame({
    "date_id": dates,
    "year": dates.year,
    "month": dates.month,
    "month_name": dates.month_name(),
    "day": dates.day,
    "weekday": dates.day_name(),
    "is_weekend": dates.weekday >= 5
})

# dim_patient
patient_ids = [f"P{str(i).zfill(5)}" for i in range(1, NUM_PATIENTS + 1)]

dim_patient = pd.DataFrame({
    "patient_id": patient_ids,
    "age_group": np.random.choice(AGE_GROUPS, NUM_PATIENTS, p=[0.2, 0.3, 0.3, 0.2]),
    "gender": np.random.choice(["Male", "Female"], NUM_PATIENTS),
    "insurance_type": np.random.choice(INSURANCE_TYPES, NUM_PATIENTS, p=[0.4, 0.4, 0.2]),
    "risk_category": np.random.choice(RISK_CATEGORIES, NUM_PATIENTS, p=[0.5, 0.3, 0.2])
})


# dim_doctor
doctor_ids = [f"D{str(i).zfill(4)}" for i in range(1, NUM_DOCTORS + 1)]

dim_doctor = pd.DataFrame({
    "doctor_id": doctor_ids,
    "doctor_name": [f"Dr_{i}" for i in doctor_ids],
    "department_id": np.random.choice(dim_department["department_id"], NUM_DOCTORS),
    "branch_id": np.random.choice(dim_branch["branch_id"], NUM_DOCTORS),
    "max_daily_hours": np.random.randint(6, 11, NUM_DOCTORS)
})


dim_branch.to_csv("../output/dim_branch.csv", index=False)
dim_department.to_csv("../output/dim_department.csv", index=False)
dim_patient.to_csv("../output/dim_patient.csv", index=False)
dim_doctor.to_csv("../output/dim_doctor.csv", index=False)
dim_date.to_csv("../output/dim_date.csv", index=False)

print("✅ All dimension tables generated successfully")