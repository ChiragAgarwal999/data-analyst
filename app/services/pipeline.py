from pathlib import Path
import asyncio
import json

from app.services.preprocessing import load_sheets, clean_sheet, merge_related_sheets
from app.services.feature_engineering import engineer_features, compute_feature_importance
from app.services.analysis import build_analysis_summary, create_visualizations
from app.services.reporting import generate_html_report, generate_pdf_report


async def run_analysis_pipeline(input_path: Path, output_dir: Path):
    sheets = await asyncio.to_thread(load_sheets, input_path)
    cleaned = {}
    cleaning_logs = {}

    for name, df in sheets.items():
        cleaned_df, log = await asyncio.to_thread(clean_sheet, df)
        cleaned[name] = cleaned_df
        cleaning_logs[name] = log

    merged_df = await asyncio.to_thread(merge_related_sheets, cleaned)
    feature_df = await asyncio.to_thread(engineer_features, merged_df)
    feat_importance = await asyncio.to_thread(compute_feature_importance, feature_df)
    analysis_summary = await asyncio.to_thread(build_analysis_summary, feature_df, feat_importance)

    charts = await asyncio.to_thread(create_visualizations, feature_df, output_dir)

    cleaned_excel = output_dir / "cleaned_dataset.xlsx"
    feature_csv = output_dir / "feature_engineered.csv"
    feature_df.to_csv(feature_csv, index=False)
    with __import__("pandas").ExcelWriter(cleaned_excel) as writer:
        for sheet_name, df in cleaned.items():
            df.to_excel(writer, sheet_name=sheet_name[:31], index=False)
        merged_df.to_excel(writer, sheet_name="merged", index=False)
        feature_df.to_excel(writer, sheet_name="features", index=False)

    summary_json = output_dir / "analysis_summary.json"
    summary_json.write_text(json.dumps(analysis_summary, indent=2, default=str), encoding="utf-8")

    html_report = output_dir / "analysis_report.html"
    pdf_report = output_dir / "analysis_report.pdf"

    await asyncio.to_thread(generate_html_report, analysis_summary, charts, html_report)
    await asyncio.to_thread(generate_pdf_report, analysis_summary, pdf_report)

    return {
        "artifacts": {
            "cleaned_excel": cleaned_excel.name,
            "feature_dataset_csv": feature_csv.name,
            "analysis_json": summary_json.name,
            "analysis_html": html_report.name,
            "analysis_pdf": pdf_report.name,
            "charts": [Path(c).name for c in charts],
        },
        "data_quality_score": analysis_summary.get("data_quality_score", 0),
        "kpi_insights": analysis_summary.get("kpi_insights", []),
        "target_candidates": analysis_summary.get("target_candidates", []),
        "ml_model_recommendations": analysis_summary.get("model_recommendations", []),
        "cleaning_logs": cleaning_logs,
    }
