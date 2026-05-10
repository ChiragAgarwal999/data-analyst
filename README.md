# AI-Powered Excel Analytics Platform

Production-style FastAPI web app that ingests messy CSV/XLSX (including multi-sheet), performs automated cleaning, feature engineering, exploratory analytics, charting, report generation (HTML/PDF), and exportable artifacts.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open: `http://127.0.0.1:8000`

## Outputs
Each upload creates a job folder under `outputs/<job_id>/`:
- `cleaned_dataset.xlsx`
- `feature_engineered.csv`
- `analysis_summary.json`
- `analysis_report.html`
- `analysis_report.pdf`
- chart PNGs
