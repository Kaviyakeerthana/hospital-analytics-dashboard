import pandas as pd
import numpy as np

np.random.seed(42)

# Load admissions AND discharges
fact_adm = pd.read_csv("../output/fact_admissions.csv")
fact_dis = pd.read_csv("../output/fact_discharge.csv") # Need this for discharge_date
dim_department = pd.read_csv("../output/dim_department.csv")

# Merge discharge info first to get dates, then department names
fact = fact_adm.merge(fact_dis[["admission_id", "discharge_date"]], on="admission_id", how="left")
fact = fact.merge(dim_department[["department_id", "department_name"]], on="department_id", how="left")

PROCEDURES = {
    "General": [
        ("Blood Test", 500, 1500),
        ("X-Ray", 1000, 3000),
        ("ECG", 800, 2000)
    ],
    "Advanced": [
        ("CT Scan", 5000, 12000),
        ("MRI", 8000, 15000),
        ("Minor Surgery", 15000, 40000),
        ("Major Surgery", 50000, 150000)
    ]
}

records = []
proc_id = 1

for _, row in fact.iterrows():
    dept = row["department_name"]

    # Decide procedure count & pool
    if dept in ["ICU", "Emergency"]:
        num_proc = np.random.randint(2, 6)
        proc_pool = PROCEDURES["Advanced"] + PROCEDURES["General"]
    else:
        num_proc = np.random.randint(1, 4)
        proc_pool = PROCEDURES["General"]

    # Date calculations
    admission_date = pd.to_datetime(row["admission_date"])
    # Handle NaN discharge dates just in case
    discharge_date = pd.to_datetime(row["discharge_date"]) if pd.notna(row["discharge_date"]) else admission_date
    
    stay_days = max((discharge_date - admission_date).days, 1)

    for _ in range(num_proc):
        # Pick a random procedure from the pool
        selection = proc_pool[np.random.randint(len(proc_pool))]
        name, low, high = selection
        
        cost = round(np.random.uniform(low, high), 2)

        # Ensure procedure happens between admission and discharge
        offset = np.random.randint(0, stay_days)
        proc_date = admission_date + pd.to_timedelta(offset, unit="D")

        records.append({
            "procedure_id": f"P{str(proc_id).zfill(7)}", # Pro ID formatted
            "admission_id": row["admission_id"],
            "patient_id": row["patient_id"],
            "department_id": row["department_id"],
            "procedure_name": name,
            "procedure_cost": cost,
            "procedure_date": proc_date.date()
        })

        proc_id += 1

fact_procedure = pd.DataFrame(records)
fact_procedure.to_csv("../output/fact_procedure.csv", index=False)

print(f"✅ Generated {len(fact_procedure)} procedures successfully!")