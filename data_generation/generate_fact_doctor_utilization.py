import pandas as pd
import numpy as np

# Load dimensions
dim_doctor = pd.read_csv("../output/dim_doctor.csv")
dim_date   = pd.read_csv("../output/dim_date.csv")

records = []

for _, doc in dim_doctor.iterrows():

    # Doctor works on ~70% of days (NO random_state)
    working_dates = dim_date.sample(
        frac=np.random.uniform(0.65, 0.8)
    )

    for _, d in working_dates.iterrows():

        shift_type = np.random.choice(
            ["Day", "Night"], p=[0.7, 0.3]
        )

        available_hours = doc["max_daily_hours"]

        # Booked hours = 60% – 100% of available
        booked_hours = round(
            available_hours * np.random.uniform(0.6, 1.0), 1
        )

        records.append({
            "doctor_id": doc["doctor_id"],
            "branch_id": doc["branch_id"],
            "department_id": doc["department_id"],
            "date_id": d["date_id"],   # consistent with dim_date
            "shift_type": shift_type,
            "available_hours": available_hours,
            "booked_hours": booked_hours
        })

fact_doctor_utilization = pd.DataFrame(records)

fact_doctor_utilization.to_csv(
    "../output/fact_doctor_utilization.csv",
    index=False
)

print("✅ fact_doctor_utilization generated successfully")