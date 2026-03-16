import pandas as pd
from sqlalchemy import text
from database import engine

CSV_PATH = "../output/dim_department.csv"

def run():
    df = pd.read_csv(CSV_PATH)
    df.columns = df.columns.str.strip()

    inserted = 0
    updated  = 0

    with engine.begin() as conn:
        for _, row in df.iterrows():
            sql = text("""
                INSERT INTO dim_department (department_id, department_name)
                VALUES (:department_id, :department_name)
                ON DUPLICATE KEY UPDATE
                    department_name = VALUES(department_name)
            """)
            result = conn.execute(sql, {
                "department_id":   int(row["department_id"]),
                "department_name": row["department_name"]
            })
            if result.rowcount == 1:
                inserted += 1
            elif result.rowcount == 2:
                updated += 1

    return {
        "table":    "dim_department",
        "inserted": inserted,
        "updated":  updated,
        "total":    len(df)
    }
