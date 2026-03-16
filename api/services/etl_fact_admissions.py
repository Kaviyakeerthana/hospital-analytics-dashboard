import pandas as pd
from sqlalchemy import text
from database import engine

CSV_PATH = "../output/fact_admissions.csv"

def run():
    df = pd.read_csv(CSV_PATH)
    df.columns = df.columns.str.strip()

    # Ensure date column is string in ISO format
    df["admission_date"] = pd.to_datetime(df["admission_date"]).dt.strftime("%Y-%m-%d")

    inserted = 0
    updated  = 0

    with engine.begin() as conn:
        for _, row in df.iterrows():
            sql = text("""
                INSERT INTO fact_admissions (
                    admission_id, patient_id, doctor_id, branch_id, department_id,
                    admission_date, admission_time, admission_type, admission_source,
                    diagnosis_category, expected_los
                )
                VALUES (
                    :admission_id, :patient_id, :doctor_id, :branch_id, :department_id,
                    :admission_date, :admission_time, :admission_type, :admission_source,
                    :diagnosis_category, :expected_los
                )
                ON DUPLICATE KEY UPDATE
                    patient_id         = VALUES(patient_id),
                    doctor_id          = VALUES(doctor_id),
                    branch_id          = VALUES(branch_id),
                    department_id      = VALUES(department_id),
                    admission_date     = VALUES(admission_date),
                    admission_time     = VALUES(admission_time),
                    admission_type     = VALUES(admission_type),
                    admission_source   = VALUES(admission_source),
                    diagnosis_category = VALUES(diagnosis_category),
                    expected_los       = VALUES(expected_los)
            """)
            result = conn.execute(sql, {
                "admission_id":       row["admission_id"],
                "patient_id":         row["patient_id"],
                "doctor_id":          row["doctor_id"],
                "branch_id":          row["branch_id"],
                "department_id":      int(row["department_id"]),
                "admission_date":     row["admission_date"],
                "admission_time":     row["admission_time"],
                "admission_type":     row["admission_type"],
                "admission_source":   row["admission_source"],
                "diagnosis_category": row["diagnosis_category"],
                "expected_los":       int(row["expected_los"])
            })
            if result.rowcount == 1:
                inserted += 1
            elif result.rowcount == 2:
                updated += 1

    return {
        "table":    "fact_admissions",
        "inserted": inserted,
        "updated":  updated,
        "total":    len(df)
    }
