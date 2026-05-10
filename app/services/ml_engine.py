import asyncio
from pathlib import Path
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier

from app.services.cleaner import clean_dataframe
from app.services.feature_engineering import build_features
from app.services.grok_agent import decide_strategy
from app.services.report_generator import create_pdf_report
from app.utils.visualization import create_charts, feature_importance_plot
from app.utils.file_handler import update_record


def _load_all_sheets(path: Path) -> dict[str, pd.DataFrame]:
    if path.suffix.lower() == ".csv":
        return {"sheet1": pd.read_csv(path)}
    return pd.read_excel(path, sheet_name=None)


def _merge_sheets(sheets: dict[str, pd.DataFrame]) -> pd.DataFrame:
    dfs = list(sheets.values())
    merged = dfs[0].copy()
    for nxt in dfs[1:]:
        common = [c for c in merged.columns if c in nxt.columns]
        merged = merged.merge(nxt, on=common[0], how="outer") if common else pd.concat([merged, nxt], axis=1)
    return merged


async def run_full_pipeline(file_id: str, record: dict):
    input_path = Path(record["input_path"])
    output_dir = Path(record["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)

    sheets = await asyncio.to_thread(_load_all_sheets, input_path)
    merged = await asyncio.to_thread(_merge_sheets, sheets)

    summary = {
        "columns": [str(c).lower() for c in merged.columns],
        "numeric_columns": merged.select_dtypes(include="number").columns.tolist(),
        "missing": merged.isna().sum().to_dict(),
    }
    strategy = await asyncio.to_thread(decide_strategy, summary)

    cleaned, clean_stats = await asyncio.to_thread(clean_dataframe, merged, strategy)
    features = await asyncio.to_thread(build_features, cleaned, strategy.get("feature_suggestions", []))

    nums = features.select_dtypes(include="number")
    importances = []
    if nums.shape[1] > 1:
        target = strategy.get("target_candidates", [nums.columns[-1]])[0]
        if target not in nums.columns:
            target = nums.columns[-1]
        X = nums.drop(columns=[target]).fillna(0)
        y = nums[target].fillna(0)
        if strategy.get("ml_model_type") == "classification":
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            y = y.round().astype(int)
        else:
            model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X, y)
        importances = sorted([
            {"feature": c, "importance": float(i)} for c, i in zip(X.columns, model.feature_importances_)
        ], key=lambda x: x["importance"], reverse=True)

    charts = await asyncio.to_thread(create_charts, features, output_dir)
    fi_chart = await asyncio.to_thread(feature_importance_plot, importances, output_dir)

    cleaned_excel = output_dir / "cleaned_dataset.xlsx"
    with pd.ExcelWriter(cleaned_excel) as writer:
        cleaned.fillna(0).to_excel(writer, sheet_name="cleaned_dataset", index=False)
        pd.DataFrame(importances).to_excel(writer, sheet_name="feature_importance", index=False)
        pd.DataFrame(cleaned.describe(include="all").transpose()).to_excel(writer, sheet_name="summary_stats")

    report_pdf = output_dir / "insight_report.pdf"
    await asyncio.to_thread(create_pdf_report, cleaned, clean_stats, importances, charts + [fi_chart], report_pdf)

    update_record(file_id, {
        "report_pdf": str(report_pdf),
        "cleaned_excel": str(cleaned_excel),
        "status": "processed"
    })

    return {
        "file_id": file_id,
        "status": "processed",
        "cleaning_stats": clean_stats,
        "target_candidates": strategy.get("target_candidates", []),
        "model_type": strategy.get("ml_model_type"),
        "downloads": {
            "report": f"/report/{file_id}",
            "cleaned_excel": f"/cleaned/{file_id}"
        }
    }
