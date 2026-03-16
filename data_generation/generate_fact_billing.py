import pandas as pd
import numpy as np

# Load Admissions, Procedures and Patient info
fact_adm = pd.read_csv("../output/fact_admissions.csv")
fact_proc = pd.read_csv("../output/fact_procedure.csv") #
dim_patient = pd.read_csv("../output/dim_patient.csv")
dim_department = pd.read_csv("../output/dim_department.csv")

# 1. Aggregate Procedure Costs by Admission ID
# Oru admission-ku panna ella procedure cost-aiyum sum panrom
proc_totals = fact_proc.groupby("admission_id")["procedure_cost"].sum().reset_index()

# 2. Merge Admissions with Patient Insurance and Procedure Totals
fact = fact_adm.merge(dim_patient[["patient_id", "insurance_type"]], on="patient_id", how="left")
fact = fact.merge(dim_department[["department_id", "department_name"]], on="department_id", how="left")
fact = fact.merge(proc_totals, on="admission_id", how="left").fillna(0) # Procedure illana 0

COST_MAP = {
    "Emergency": 15000, "ICU": 25000, "Cardiology": 18000,
    "Neurology": 17000, "Orthopedics": 14000, "General Medicine": 10000
}

records = []
for _, row in fact.iterrows():
    # Base Hospital Charge (Room/Doctor fee)
    base_dept_cost = COST_MAP.get(row["department_name"], 12000)
    
    # Total Actual Cost = Dept Base Cost + Sum of all Procedures
    total_hospital_cost = round((base_dept_cost + row["procedure_cost"]) * np.random.uniform(0.9, 1.1), 2)

    # Billing based on Insurance
    if row["insurance_type"] == "Govt":
        billing_amount = total_hospital_cost * 0.9  # Discounted
        paid_prob = 0.7
    elif row["insurance_type"] == "Private":
        billing_amount = total_hospital_cost * 1.4  # Premium
        paid_prob = 0.9
    else:
        billing_amount = total_hospital_cost * 1.1  # Standard
        paid_prob = 0.8

    records.append({
        "admission_id": row["admission_id"],
        "branch_id": row["branch_id"],
        "department_id": row["department_id"],
        "total_procedure_cost": round(row["procedure_cost"], 2), # Breakdown-kaga
        "base_hospital_cost": round(base_dept_cost, 2),
        "total_cost": total_hospital_cost,
        "billing_amount": round(billing_amount, 2),
        "insurance_type": row["insurance_type"],
        "payment_status": np.random.choice(["Paid", "Pending"], p=[paid_prob, 1-paid_prob])
    })

fact_billing = pd.DataFrame(records)
fact_billing.to_csv("../output/fact_billing.csv", index=False)
print("✅ fact_billing updated with procedure costs!")