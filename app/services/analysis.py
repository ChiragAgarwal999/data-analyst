from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def build_analysis_summary(df: pd.DataFrame, feature_importance: list[dict]):
    numeric = df.select_dtypes(include=[np.number])
    desc = numeric.describe().to_dict() if not numeric.empty else {}
    corr = numeric.corr().fillna(0).to_dict() if numeric.shape[1] > 1 else {}

    anomaly_count = 0
    if not numeric.empty:
        z = ((numeric - numeric.mean()) / (numeric.std().replace(0, 1))).abs()
        anomaly_count = int((z > 3).any(axis=1).sum())

    quality = max(0, min(100, int(100 - (df.isna().sum().sum() / max(1, df.size)) * 100 - anomaly_count * 0.1)))

    targets = [c for c in df.columns if any(k in c.lower() for k in ["target", "label", "price", "sales", "revenue", "cost"])]
    model_recs = [
        "RandomForest/XGBoost for tabular mixed data",
        "LightGBM/CatBoost for large categorical-heavy datasets",
        "ARIMA/Prophet for time-series targets",
    ]

    return {
        "executive_summary": "Dataset was cleaned, standardized, analyzed, and transformed into a prediction-ready structure.",
        "key_findings": [
            f"Rows: {len(df)}, Columns: {len(df.columns)}",
            f"Anomalies detected: {anomaly_count}",
            f"Top feature: {feature_importance[0]['feature'] if feature_importance else 'N/A'}",
        ],
        "descriptive_statistics": desc,
        "correlation": corr,
        "feature_importance": feature_importance,
        "kpi_insights": ["Automated KPI scan completed", "Data quality and anomalies assessed"],
        "target_candidates": targets[:5],
        "model_recommendations": model_recs,
        "prediction_readiness": "High" if quality > 75 else "Medium" if quality > 50 else "Low",
        "risks": ["Potential proxy leakage", "Non-stationary trend risk", "Domain-specific validation required"],
        "data_quality_score": quality,
        "recommendations": [
            "Validate target definition with domain expert",
            "Run temporal split if timestamps are present",
            "Add business rules for outlier retention",
        ],
    }


def create_visualizations(df: pd.DataFrame, output_dir: Path):
    chart_paths = []
    numeric = df.select_dtypes(include=[np.number])
    if not numeric.empty:
        chart1 = output_dir / "histogram.png"
        numeric.hist(figsize=(10, 6))
        plt.tight_layout()
        plt.savefig(chart1)
        plt.close("all")
        chart_paths.append(str(chart1))

    if numeric.shape[1] > 1:
        corr = numeric.corr()
        chart2 = output_dir / "correlation_heatmap.png"
        plt.figure(figsize=(8, 6))
        plt.imshow(corr, cmap="coolwarm", aspect="auto")
        plt.colorbar()
        plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)
        plt.yticks(range(len(corr.columns)), corr.columns)
        plt.tight_layout()
        plt.savefig(chart2)
        plt.close("all")
        chart_paths.append(str(chart2))

    return chart_paths
