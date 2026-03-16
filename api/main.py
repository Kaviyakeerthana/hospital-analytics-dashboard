"""
Hospital Analytics ETL API
===========================
Run with:  uvicorn main:app --reload --port 8000
Docs at:   http://localhost:8000/docs
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from services import (
    etl_dim_branch,
    etl_dim_department,
    etl_dim_patient,
    etl_dim_doctor,
    etl_dim_date,
    etl_fact_admissions,
    etl_fact_discharge,
    etl_fact_procedure,
    etl_fact_billing,
    etl_fact_bed_utilization,
    etl_fact_doctor_utilization,
)

app = FastAPI(
    title="Hospital Analytics ETL API",
    description="Trigger ETL loads for each dimension and fact table.",
    version="1.0.0",
)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─────────────────────────────────────────
# Helper
# ─────────────────────────────────────────
def _run(service_module):
    """Wrap any ETL service call with consistent error handling."""
    try:
        result = service_module.run()
        return JSONResponse(content={"status": "success", "data": result})
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


# ─────────────────────────────────────────
# Dimension endpoints  (load FIRST)
# ─────────────────────────────────────────

@app.post("/etl/dim/branch", tags=["Dimensions"])
def load_dim_branch():
    """Load / upsert dim_branch from CSV."""
    return _run(etl_dim_branch)


@app.post("/etl/dim/department", tags=["Dimensions"])
def load_dim_department():
    """Load / upsert dim_department from CSV."""
    return _run(etl_dim_department)


@app.post("/etl/dim/patient", tags=["Dimensions"])
def load_dim_patient():
    """Load / upsert dim_patient from CSV."""
    return _run(etl_dim_patient)


@app.post("/etl/dim/doctor", tags=["Dimensions"])
def load_dim_doctor():
    """Load / upsert dim_doctor from CSV.
    Requires dim_branch and dim_department to be loaded first."""
    return _run(etl_dim_doctor)


@app.post("/etl/dim/date", tags=["Dimensions"])
def load_dim_date():
    """Load / upsert dim_date from CSV."""
    return _run(etl_dim_date)


# ─────────────────────────────────────────
# Fact endpoints  (load AFTER dimensions)
# ─────────────────────────────────────────

@app.post("/etl/fact/admissions", tags=["Facts"])
def load_fact_admissions():
    """Load / upsert fact_admissions.
    Requires: dim_branch, dim_department, dim_patient, dim_doctor."""
    return _run(etl_fact_admissions)


@app.post("/etl/fact/discharge", tags=["Facts"])
def load_fact_discharge():
    """Load / upsert fact_discharge.
    Requires: fact_admissions."""
    return _run(etl_fact_discharge)


@app.post("/etl/fact/procedure", tags=["Facts"])
def load_fact_procedure():
    """Load / upsert fact_procedure.
    Requires: fact_admissions, fact_discharge."""
    return _run(etl_fact_procedure)


@app.post("/etl/fact/billing", tags=["Facts"])
def load_fact_billing():
    """Load / upsert fact_billing.
    Requires: fact_admissions, fact_procedure."""
    return _run(etl_fact_billing)


@app.post("/etl/fact/bed-utilization", tags=["Facts"])
def load_fact_bed_utilization():
    """Load / upsert fact_bed_utilization.
    Requires: dim_branch, dim_department, dim_date."""
    return _run(etl_fact_bed_utilization)


@app.post("/etl/fact/doctor-utilization", tags=["Facts"])
def load_fact_doctor_utilization():
    """Load / upsert fact_doctor_utilization.
    Requires: dim_doctor, dim_date."""
    return _run(etl_fact_doctor_utilization)


# ─────────────────────────────────────────
# Convenience: run ALL ETL in correct order
# ─────────────────────────────────────────

@app.post("/etl/run-all", tags=["Pipeline"])
def run_all_etl():
    """
    Execute every ETL service in dependency-safe order.
    Stops on the first failure and reports which step failed.
    """
    pipeline = [
        ("dim_branch",              etl_dim_branch),
        ("dim_department",          etl_dim_department),
        ("dim_patient",             etl_dim_patient),
        ("dim_date",                etl_dim_date),
        ("dim_doctor",              etl_dim_doctor),          # needs branch + dept
        ("fact_admissions",         etl_fact_admissions),     # needs all dims
        ("fact_discharge",          etl_fact_discharge),      # needs admissions
        ("fact_procedure",          etl_fact_procedure),      # needs admissions + discharge
        ("fact_billing",            etl_fact_billing),        # needs admissions + procedure
        ("fact_bed_utilization",    etl_fact_bed_utilization),
        ("fact_doctor_utilization", etl_fact_doctor_utilization),
    ]

    results = []
    for name, module in pipeline:
        try:
            result = module.run()
            results.append({"step": name, "status": "success", "data": result})
        except Exception as exc:
            results.append({"step": name, "status": "failed", "error": str(exc)})
            return JSONResponse(
                status_code=500,
                content={
                    "status":  "pipeline_failed",
                    "failed_at": name,
                    "results": results,
                },
            )

    return JSONResponse(content={"status": "all_success", "results": results})


# ─────────────────────────────────────────
# Health check
# ─────────────────────────────────────────

@app.get("/health", tags=["System"])
def health():
    return {"status": "ok"}
