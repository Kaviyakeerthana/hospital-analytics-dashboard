import pandas as pd
import numpy as np

# Load dimensions
dim_branch = pd.read_csv("../output/dim_branch.csv")
dim_department = pd.read_csv("../output/dim_department.csv")
dim_date = pd.read_csv("../output/dim_date.csv")

records = []

for _, branch in dim_branch.iterrows():

    branch_id = branch["branch_id"]
    total_beds = branch["total_beds"]
    icu_beds = branch["icu_beds"]

    # Identify ICU department
    icu_dept = dim_department[
        dim_department["department_name"].str.upper() == "ICU"
    ]

    non_icu_depts = dim_department[
        dim_department["department_name"].str.upper() != "ICU"
    ]

    # Safe calculation
    if not icu_dept.empty:
        general_beds_total = total_beds - icu_beds
    else:
        general_beds_total = total_beds

    general_beds_per_dept = (
        general_beds_total // len(non_icu_depts)
        if len(non_icu_depts) > 0 else 0
    )

    for _, d in dim_date.iterrows():

        date_id = d["date_id"]

        # ICU beds
        if not icu_dept.empty:
            occupied_icu = np.random.randint(
                int(icu_beds * 0.6),
                int(icu_beds * 0.95)
            )

            records.append({
                "branch_id": branch_id,
                "department_id": int(icu_dept.iloc[0]["department_id"]),
                "date_id": date_id,
                "bed_type": "ICU",
                "occupied_beds": occupied_icu,
                "total_beds": icu_beds
            })

        # General beds
        for _, dept in non_icu_depts.iterrows():
            occupied_general = np.random.randint(
                int(general_beds_per_dept * 0.5),
                int(general_beds_per_dept * 0.9)
            )

            records.append({
                "branch_id": branch_id,
                "department_id": int(dept["department_id"]),
                "date_id": date_id,
                "bed_type": "General",
                "occupied_beds": occupied_general,
                "total_beds": general_beds_per_dept
            })

fact_bed_utilization = pd.DataFrame(records)

fact_bed_utilization.to_csv(
    "../output/fact_bed_utilization.csv",
    index=False
)

print("✅ fact_bed_utilization generated with correct ICU & date logic")