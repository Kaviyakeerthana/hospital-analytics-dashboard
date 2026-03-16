import pandas as pd
from sqlalchemy import text
from database import engine

CSV_PATH = "../output/dim_doctor.csv"

def run():
    df = pd.read_csv(CSV_PATH)
    df.columns = df.columns.str.strip()

    inserted = 0
    updated  = 0

    with engine.begin() as conn:
        for _, row in df.iterrows():
            sql = text("""
                INSERT INTO dim_doctor
                    (doctor_id, doctor_name, department_id, branch_id, max_daily_hours)
                VALUES
                    (:doctor_id, :doctor_name, :department_id, :branch_id, :max_daily_hours)
                ON DUPLICATE KEY UPDATE
                    doctor_name     = VALUES(doctor_name),
                    department_id   = VALUES(department_id),
                    branch_id       = VALUES(branch_id),
                    max_daily_hours = VALUES(max_daily_hours)
            """)
            result = conn.execute(sql, {
                "doctor_id":       row["doctor_id"],
                "doctor_name":     row["doctor_name"],
                "department_id":   int(row["department_id"]),
                "branch_id":       row["branch_id"],
                "max_daily_hours": int(row["max_daily_hours"])
            })
            if result.rowcount == 1:
                inserted += 1
            elif result.rowcount == 2:
                updated += 1

    return {
        "table":    "dim_doctor",
        "inserted": inserted,
        "updated":  updated,
        "total":    len(df)
    }
