# Hospital Resource Utilization and Patient Outcomes Dashboard

I built this project to analyze hospital operations across 5 branches
in Tamil Nadu. The goal was to create a complete data pipeline — from
generating the data all the way to an interactive dashboard that hospital
management can use to monitor day-to-day performance.

## Dashboard

 [View Full Dashboard PDF](HospitalDashboard.pdf)

## What This Project Does

This system tracks how efficiently a hospital network is running. It
monitors bed occupancy, doctor workload, patient outcomes, billing
collections, and procedure costs — all in one place.

The dashboard answers questions like:
- Which branch has the highest pending collections?
- Are ICU beds reaching critical occupancy?
- Which doctors are overworked?
- What is the 30-day patient readmission rate?
- How does cost per discharge vary across departments?

## Architecture
```
Data Generation → MySQL Star Schema → Python ETL → FastAPI API → Power BI Dashboard
```

## Key Metrics

- 45,000 admissions | ₹2,233M revenue | 5 branches
- 69.36% bed occupancy | 8.54% readmission rate
- 79.98% doctor utilization | 4.94% mortality rate

## Project Structure
```
hospital_analytics/
├── api/
│   ├── database.py
│   ├── main.py
│   └── services/
│       ├── etl_dim_branch.py
│       ├── etl_dim_department.py
│       ├── etl_dim_patient.py
│       ├── etl_dim_doctor.py
│       ├── etl_dim_date.py
│       ├── etl_fact_admissions.py
│       ├── etl_fact_discharge.py
│       ├── etl_fact_procedure.py
│       ├── etl_fact_billing.py
│       ├── etl_fact_bed_utilization.py
│       └── etl_fact_doctor_utilization.py
├── data_generation/
│   ├── config.py
│   ├── generate_dimensions.py
│   ├── generate_fact_admissions.py
│   ├── generate_fact_billing.py
│   ├── generate_fact_discharges.py
│   ├── generate_fact_procedure.py
│   ├── generate_fact_bed_utilization.py
│   └── generate_fact_doctor_utilization.py
├── HospitalDashboard.pdf
├── requirements.txt
└── README.md
```

## Tech Stack

| Layer | Technology |
|---|---|
| Data Generation | Python, Faker, Pandas |
| Database | MySQL 8.x, Star Schema (11 tables) |
| ETL Pipeline | Python, SQLAlchemy, Pandas |
| API Backend | FastAPI, Uvicorn |
| Dashboard | Power BI Desktop, DAX |

## How to Run

### 1. Clone repository
```bash
git clone https://github.com/Kaviyakeerthana/hospital-analytics-dashboard.git
cd hospital-analytics-dashboard
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure database
Create `.env` file in root folder:
```
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/hospital_analytics
```

### 4. Generate data
```bash
cd data_generation
python generate_dimensions.py
python generate_fact_admissions.py
python generate_fact_billing.py
python generate_fact_discharges.py
python generate_fact_procedure.py
python generate_fact_bed_utilization.py
python generate_fact_doctor_utilization.py
```

### 5. Start API
```bash
cd api
uvicorn main:app --reload --port 8000
```

### 6. Run ETL pipeline
```
Open browser → http://localhost:8000/docs
Trigger POST /etl/run-all to load all 11 tables at once
```

## Author

**Kaviyakeerthana R**
B.Tech Information Technology — Velalar College of Engineering and Technology

-  kaviyakeerthana1845@gmail.com
-  [LinkedIn](https://www.linkedin.com/in/kaviyakeerthana-r-897280243/)
-  [GitHub](https://github.com/Kaviyakeerthana)