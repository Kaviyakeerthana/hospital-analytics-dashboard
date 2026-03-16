import pandas as pd
from sqlalchemy import text
from database import engine

CSV_PATH = "../output/fact_discharge.csv"

def run():
    df = pd.read_csv(CSV_PATH)
    df.columns = df.columns.str.strip()

    df["discharge_date"] = pd.to_datetime(df["discharge_date"]).dt.strftime("%Y-%m-%d")

    inserted = 0
    updated  = 0

    with engine.begin() as conn:
        for _, row in df.iterrows():
            sql = text("""
                INSERT INTO fact_discharge (
                    admission_id, patient_id, actual_los,
                    discharge_date, discharge_time,
                    patient_outcome, discharge_type
                )
                VALUES (
                    :admission_id, :patient_id, :actual_los,
                    :discharge_date, :discharge_time,
                    :patient_outcome, :discharge_type
                )
                ON DUPLICATE KEY UPDATE
                    patient_id      = VALUES(patient_id),
                    actual_los      = VALUES(actual_los),
                    discharge_date  = VALUES(discharge_date),
                    discharge_time  = VALUES(discharge_time),
                    patient_outcome = VALUES(patient_outcome),
                    discharge_type  = VALUES(discharge_type)
            """)
            result = conn.execute(sql, {
                "admission_id":   row["admission_id"],
                "patient_id":     row["patient_id"],
                "actual_los":     int(row["actual_los"]),
                "discharge_date": row["discharge_date"],
                "discharge_time": row["discharge_time"],
                "patient_outcome": row["patient_outcome"],
                "discharge_type": row["discharge_type"]
            })
            if result.rowcount == 1:
                inserted += 1
            elif result.rowcount == 2:
                updated += 1

    return {
        "table":    "fact_discharge",
        "inserted": inserted,
        "updated":  updated,
        "total":    len(df)
    }
