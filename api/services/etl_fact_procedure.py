import pandas as pd
from sqlalchemy import text
from database import engine

CSV_PATH = "../output/fact_procedure.csv"

def run():
    df = pd.read_csv(CSV_PATH)
    df.columns = df.columns.str.strip()

    df["procedure_date"] = pd.to_datetime(df["procedure_date"]).dt.strftime("%Y-%m-%d")

    inserted = 0
    updated  = 0

    with engine.begin() as conn:
        for _, row in df.iterrows():
            sql = text("""
                INSERT INTO fact_procedure (
                    procedure_id, admission_id, patient_id, department_id,
                    procedure_name, procedure_cost, procedure_date
                )
                VALUES (
                    :procedure_id, :admission_id, :patient_id, :department_id,
                    :procedure_name, :procedure_cost, :procedure_date
                )
                ON DUPLICATE KEY UPDATE
                    admission_id   = VALUES(admission_id),
                    patient_id     = VALUES(patient_id),
                    department_id  = VALUES(department_id),
                    procedure_name = VALUES(procedure_name),
                    procedure_cost = VALUES(procedure_cost),
                    procedure_date = VALUES(procedure_date)
            """)
            result = conn.execute(sql, {
                "procedure_id":   row["procedure_id"],
                "admission_id":   row["admission_id"],
                "patient_id":     row["patient_id"],
                "department_id":  int(row["department_id"]),
                "procedure_name": row["procedure_name"],
                "procedure_cost": float(row["procedure_cost"]),
                "procedure_date": row["procedure_date"]
            })
            if result.rowcount == 1:
                inserted += 1
            elif result.rowcount == 2:
                updated += 1

    return {
        "table":    "fact_procedure",
        "inserted": inserted,
        "updated":  updated,
        "total":    len(df)
    }
