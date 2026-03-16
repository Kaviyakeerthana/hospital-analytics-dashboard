import pandas as pd
from sqlalchemy import text
from database import engine

CSV_PATH = "../output/fact_billing.csv"

def run():
    df = pd.read_csv(CSV_PATH)
    df.columns = df.columns.str.strip()

    inserted = 0
    updated  = 0

    with engine.begin() as conn:
        for _, row in df.iterrows():
            sql = text("""
                INSERT INTO fact_billing (
                    admission_id, branch_id, department_id,
                    total_procedure_cost, base_hospital_cost, total_cost,
                    billing_amount, insurance_type, payment_status
                )
                VALUES (
                    :admission_id, :branch_id, :department_id,
                    :total_procedure_cost, :base_hospital_cost, :total_cost,
                    :billing_amount, :insurance_type, :payment_status
                )
                ON DUPLICATE KEY UPDATE
                    branch_id            = VALUES(branch_id),
                    department_id        = VALUES(department_id),
                    total_procedure_cost = VALUES(total_procedure_cost),
                    base_hospital_cost   = VALUES(base_hospital_cost),
                    total_cost           = VALUES(total_cost),
                    billing_amount       = VALUES(billing_amount),
                    insurance_type       = VALUES(insurance_type),
                    payment_status       = VALUES(payment_status)
            """)
            result = conn.execute(sql, {
                "admission_id":        row["admission_id"],
                "branch_id":           row["branch_id"],
                "department_id":       int(row["department_id"]),
                "total_procedure_cost": float(row["total_procedure_cost"]),
                "base_hospital_cost":  float(row["base_hospital_cost"]),
                "total_cost":          float(row["total_cost"]),
                "billing_amount":      float(row["billing_amount"]),
                "insurance_type":      row["insurance_type"],
                "payment_status":      row["payment_status"]
            })
            if result.rowcount == 1:
                inserted += 1
            elif result.rowcount == 2:
                updated += 1

    return {
        "table":    "fact_billing",
        "inserted": inserted,
        "updated":  updated,
        "total":    len(df)
    }
