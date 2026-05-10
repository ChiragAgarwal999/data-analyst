from __future__ import annotations
import pandas as pd
import numpy as np


def load_sheets(path):
    if str(path).lower().endswith(".csv"):
        return {"sheet1": pd.read_csv(path)}
    return pd.read_excel(path, sheet_name=None)


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]
    return df


def clean_sheet(df: pd.DataFrame):
    logs = []
    df = _normalize_columns(df)

    before = len(df)
    df = df.drop_duplicates()
    logs.append(f"Removed {before - len(df)} duplicate rows")

    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].astype(str).str.strip()
            # numeric coercion where possible
            coerced = pd.to_numeric(df[col], errors="coerce")
            if coerced.notna().sum() > max(3, 0.7 * len(df[col].dropna())):
                df[col] = coerced

    missing_before = int(df.isna().sum().sum())
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(df[col].median())
            q1, q3 = df[col].quantile([0.25, 0.75])
            iqr = q3 - q1
            if iqr > 0:
                lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
                df[col] = df[col].clip(lower, upper)
        else:
            mode = df[col].mode()
            fill = mode.iloc[0] if not mode.empty else "unknown"
            df[col] = df[col].replace({"": np.nan}).fillna(fill)

    missing_after = int(df.isna().sum().sum())
    logs.append(f"Missing values before/after: {missing_before}/{missing_after}")

    df = df.dropna(how="all")
    return df, logs


def merge_related_sheets(cleaned: dict[str, pd.DataFrame]) -> pd.DataFrame:
    if not cleaned:
        return pd.DataFrame()
    frames = list(cleaned.values())
    merged = frames[0].copy()

    for nxt in frames[1:]:
        common = [c for c in merged.columns if c in nxt.columns]
        if common:
            key = common[0]
            merged = merged.merge(nxt, on=key, how="outer", suffixes=("", "_r"))
        else:
            merged = pd.concat([merged.reset_index(drop=True), nxt.reset_index(drop=True)], axis=1)
    return merged
