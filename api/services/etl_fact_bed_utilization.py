import pandas as pd
from sqlalchemy import text
from database import engine

CSV_PATH = "../output/fact_bed_utilization.csv"

def run():
    df = pd.read_csv(CSV_PATH)
    df.columns = df.columns.str.strip()

    df["date_id"] = pd.to_datetime(df["date_id"]).dt.strftime("%Y-%m-%d")

    inserted = 0
    updated  = 0

    with engine.begin() as conn:
        for _, row in df.iterrows():
            # Composite PK: (branch_id, department_id, date_id, bed_type)
            # ON DUPLICATE KEY UPDATE fires cleanly — no SELECT needed.
            sql = text("""
                INSERT INTO fact_bed_utilization
                    (branch_id, department_id, date_id, bed_type, occupied_beds, total_beds)
                VALUES
                    (:branch_id, :department_id, :date_id, :bed_type, :occupied_beds, :total_beds)
                ON DUPLICATE KEY UPDATE
                    occupied_beds = VALUES(occupied_beds),
                    total_beds    = VALUES(total_beds)
            """)
            result = conn.execute(sql, {
                "branch_id":     row["branch_id"],
                "department_id": int(row["department_id"]),
                "date_id":       row["date_id"],
                "bed_type":      row["bed_type"],
                "occupied_beds": int(row["occupied_beds"]),
                "total_beds":    int(row["total_beds"])
            })
            # rowcount == 1 → fresh insert | 2 → duplicate updated | 0 → no change
            if result.rowcount == 1:
                inserted += 1
            elif result.rowcount == 2:
                updated += 1

    return {
        "table":    "fact_bed_utilization",
        "inserted": inserted,
        "updated":  updated,
        "total":    len(df)
    }
