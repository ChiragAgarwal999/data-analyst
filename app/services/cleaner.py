from __future__ import annotations
import pandas as pd
import numpy as np


def clean_dataframe(df: pd.DataFrame, strategy: dict) -> tuple[pd.DataFrame, dict]:
    out = df.copy()
    out.columns = [str(c).strip().lower().replace(" ", "_") for c in out.columns]

    before_rows = len(out)
    out = out.drop_duplicates()

    dropped_cols = strategy.get("drop_columns", [])
    out = out.drop(columns=[c for c in dropped_cols if c in out.columns], errors="ignore")

    for col in out.columns:
        if out[col].dtype == "object":
            out[col] = out[col].astype(str).str.strip()
            coerced = pd.to_numeric(out[col], errors="coerce")
            if coerced.notna().sum() > 0.8 * max(1, len(out)):
                out[col] = coerced

    for col in out.columns:
        if pd.api.types.is_numeric_dtype(out[col]):
            fill_method = strategy.get("imputation", {}).get(col, "median")
            fill = out[col].median() if fill_method == "median" else out[col].mean()
            out[col] = out[col].replace([np.inf, -np.inf], np.nan).fillna(fill)
        else:
            mode = out[col].mode()
            out[col] = out[col].replace("", np.nan).fillna(mode.iloc[0] if not mode.empty else "unknown")

    out = out.dropna(how="all")
    quality = max(0, min(100, int(100 - out.isna().sum().sum() * 2)))

    stats = {
        "rows_before": before_rows,
        "rows_after": len(out),
        "duplicates_removed": before_rows - len(out),
        "quality_score": quality,
    }
    return out, stats
