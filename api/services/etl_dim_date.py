import pandas as pd
from sqlalchemy import text
from database import engine

CSV_PATH = "../output/dim_date.csv"

def run():
    df = pd.read_csv(CSV_PATH)
    df.columns = df.columns.str.strip()

    # Normalise boolean: CSV stores True/False as strings
    df["is_weekend"] = df["is_weekend"].astype(str).str.lower().map(
        {"true": 1, "false": 0, "1": 1, "0": 0}
    ).fillna(0).astype(int)

    inserted = 0
    updated  = 0

    with engine.begin() as conn:
        for _, row in df.iterrows():
            sql = text("""
                INSERT INTO dim_date
                    (date_id, year, month, month_name, day, weekday, is_weekend)
                VALUES
                    (:date_id, :year, :month, :month_name, :day, :weekday, :is_weekend)
                ON DUPLICATE KEY UPDATE
                    year       = VALUES(year),
                    month      = VALUES(month),
                    month_name = VALUES(month_name),
                    day        = VALUES(day),
                    weekday    = VALUES(weekday),
                    is_weekend = VALUES(is_weekend)
            """)
            result = conn.execute(sql, {
                "date_id":    row["date_id"],
                "year":       int(row["year"]),
                "month":      int(row["month"]),
                "month_name": row["month_name"],
                "day":        int(row["day"]),
                "weekday":    row["weekday"],
                "is_weekend": int(row["is_weekend"])
            })
            if result.rowcount == 1:
                inserted += 1
            elif result.rowcount == 2:
                updated += 1

    return {
        "table":    "dim_date",
        "inserted": inserted,
        "updated":  updated,
        "total":    len(df)
    }
