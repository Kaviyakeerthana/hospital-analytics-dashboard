import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

from config import (
    START_DATE,
    END_DATE,
    TOTAL_ADMISSIONS,
    ADMISSION_TYPES,
    ADMISSION_SOURCES,
    DIAGNOSIS_CATEGORIES
)

# Load dimension tables
dim_patient = pd.read_csv("../output/dim_patient.csv")
dim_doctor = pd.read_csv("../output/dim_doctor.csv")
dim_branch = pd.read_csv("../output/dim_branch.csv")
dim_department = pd.read_csv("../output/dim_department.csv")

# Prepare lists
patient_ids = dim_patient["patient_id"].tolist()
doctor_ids = dim_doctor["doctor_id"].tolist()
branch_ids = dim_branch["branch_id"].tolist()
department_ids = dim_department["department_id"].tolist()

# Date range
start = pd.to_datetime(START_DATE)
end = pd.to_datetime(END_DATE)
date_range = (end - start).days

records = []

for i in range(1, TOTAL_ADMISSIONS + 1):

    admission_date = start + timedelta(days=random.randint(0, date_range))

    # Peak hour simulation (8–11 AM & 5–8 PM)
    if random.random() < 0.7:
        hour = random.choice(list(range(8, 12)) + list(range(17, 21)))
    else:
        hour = random.randint(0, 23)

    admission_time = f"{hour:02d}:{random.randint(0,59):02d}:00"

    admission_type = np.random.choice(
        ADMISSION_TYPES, p=[0.6, 0.4]  # Emergency higher
    )

    admission_source = (
        "ER" if admission_type == "Emergency"
        else np.random.choice(["OPD", "Referral"])
    )

    expected_los = (
        random.randint(5, 10) if admission_type == "Emergency"
        else random.randint(2, 6)
    )

    records.append({
        "admission_id": f"A{str(i).zfill(6)}",
        "patient_id": random.choice(patient_ids),
        "doctor_id": random.choice(doctor_ids),
        "branch_id": random.choice(branch_ids),
        "department_id": random.choice(department_ids),
        "admission_date": admission_date.date(),
        "admission_time": admission_time,
        "admission_type": admission_type,
        "admission_source": admission_source,
        "diagnosis_category": random.choice(DIAGNOSIS_CATEGORIES),
        "expected_los": expected_los
    })

fact_admissions = pd.DataFrame(records)

# Final validation
assert fact_admissions.isnull().sum().sum() == 0

fact_admissions.to_csv("../output/fact_admissions.csv", index=False)

print("✅ fact_admissions generated successfully")
print(f"📊 Total rows: {len(fact_admissions)}")