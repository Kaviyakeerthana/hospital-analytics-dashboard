import pandas as pd
from sqlalchemy import text
from database import engine

CSV_PATH = "../output/fact_doctor_utilization.csv"

def run():
    df = pd.read_csv(CSV_PATH)
    df.columns = df.columns.str.strip()

    df["date_id"] = pd.to_datetime(df["date_id"]).dt.strftime("%Y-%m-%d")

    inserted = 0
    updated  = 0

    with engine.begin() as conn:
        for _, row in df.iterrows():
            # Composite PK: (doctor_id, date_id, shift_type)
            # ON DUPLICATE KEY UPDATE fires cleanly — no SELECT needed.
            sql = text("""
                INSERT INTO fact_doctor_utilization
                    (doctor_id, branch_id, department_id, date_id,
                     shift_type, available_hours, booked_hours)
                VALUES
                    (:doctor_id, :branch_id, :department_id, :date_id,
                     :shift_type, :available_hours, :booked_hours)
                ON DUPLICATE KEY UPDATE
                    branch_id       = VALUES(branch_id),
                    department_id   = VALUES(department_id),
                    available_hours = VALUES(available_hours),
                    booked_hours    = VALUES(booked_hours)
            """)
            result = conn.execute(sql, {
                "doctor_id":       row["doctor_id"],
                "branch_id":       row["branch_id"],
                "department_id":   int(row["department_id"]),
                "date_id":         row["date_id"],
                "shift_type":      row["shift_type"],
                "available_hours": float(row["available_hours"]),
                "booked_hours":    float(row["booked_hours"])
            })
            # rowcount == 1 → fresh insert | 2 → duplicate updated | 0 → no change
            if result.rowcount == 1:
                inserted += 1
            elif result.rowcount == 2:
                updated += 1

    return {
        "table":    "fact_doctor_utilization",
        "inserted": inserted,
        "updated":  updated,
        "total":    len(df)
    }
