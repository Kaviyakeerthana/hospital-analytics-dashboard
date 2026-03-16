import pandas as pd
from sqlalchemy import text
from database import engine

CSV_PATH = "../output/dim_branch.csv"

def run():
    df = pd.read_csv(CSV_PATH)
    df.columns = df.columns.str.strip()

    inserted = 0
    updated  = 0

    with engine.begin() as conn:
        for _, row in df.iterrows():
            sql = text("""
                INSERT INTO dim_branch (branch_id, branch_name, city, total_beds, icu_beds)
                VALUES (:branch_id, :branch_name, :city, :total_beds, :icu_beds)
                ON DUPLICATE KEY UPDATE
                    branch_name = VALUES(branch_name),
                    city        = VALUES(city),
                    total_beds  = VALUES(total_beds),
                    icu_beds    = VALUES(icu_beds)
            """)
            result = conn.execute(sql, {
                "branch_id":   row["branch_id"],
                "branch_name": row["branch_name"],
                "city":        row["city"],
                "total_beds":  int(row["total_beds"]),
                "icu_beds":    int(row["icu_beds"])
            })
            # rowcount == 1 → insert, 2 → update, 0 → no change
            if result.rowcount == 1:
                inserted += 1
            elif result.rowcount == 2:
                updated += 1

    return {
        "table":    "dim_branch",
        "inserted": inserted,
        "updated":  updated,
        "total":    len(df)
    }
