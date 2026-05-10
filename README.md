# AI Data Analyst SaaS (FastAPI).

This app implements a production-style backend workflow:

1. `POST /upload` (.xlsx/.csv)
2. `POST /process/{file_id}` (AI-driven cleaning + feature engineering + ML preparation + report generation)
3. `GET /report/{file_id}` (PDF download)
4. `GET /cleaned/{file_id}` (cleaned Excel download)

## Architecture
- `app/api`: upload and processing endpoints
- `app/services/cleaner.py`: robust cleaning
- `app/services/grok_agent.py`: Grok decision engine stub/fallback JSON strategy
- `app/services/feature_engineering.py`: derived features and encoding
- `app/services/ml_engine.py`: end-to-end orchestration + baseline model fitting
- `app/services/report_generator.py`: PDF generation
- `app/utils/file_handler.py`: file/metadata tracking
- `app/utils/visualization.py`: charts and feature-importance graph

## Run
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000` for a simple upload/process UI.
