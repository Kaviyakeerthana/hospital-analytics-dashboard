import pandas as pd
from sqlalchemy import text
from database import engine

CSV_PATH = "../output/dim_patient.csv"

def run():
    df = pd.read_csv(CSV_PATH)
    df.columns = df.columns.str.strip()

    inserted = 0
    updated  = 0

    with engine.begin() as conn:
        for _, row in df.iterrows():
            sql = text("""
                INSERT INTO dim_patient
                    (patient_id, age_group, gender, insurance_type, risk_category)
                VALUES
                    (:patient_id, :age_group, :gender, :insurance_type, :risk_category)
                ON DUPLICATE KEY UPDATE
                    age_group      = VALUES(age_group),
                    gender         = VALUES(gender),
                    insurance_type = VALUES(insurance_type),
                    risk_category  = VALUES(risk_category)
            """)
            result = conn.execute(sql, {
                "patient_id":     row["patient_id"],
                "age_group":      row["age_group"],
                "gender":         row["gender"],
                "insurance_type": row["insurance_type"],
                "risk_category":  row["risk_category"]
            })
            if result.rowcount == 1:
                inserted += 1
            elif result.rowcount == 2:
                updated += 1

    return {
        "table":    "dim_patient",
        "inserted": inserted,
        "updated":  updated,
        "total":    len(df)
    }
