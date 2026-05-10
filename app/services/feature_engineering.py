import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder


def build_features(df: pd.DataFrame, suggestions: list[str]) -> pd.DataFrame:
    out = df.copy()
    for col in out.select_dtypes(include=["object"]).columns:
        dt = pd.to_datetime(out[col], errors="coerce")
        if dt.notna().mean() > 0.6:
            out[f"{col}_year"] = dt.dt.year
            out[f"{col}_month"] = dt.dt.month

    if "row aggregations" in " ".join(suggestions).lower():
        nums = out.select_dtypes(include=[np.number]).columns
        if len(nums) > 1:
            out["row_mean"] = out[nums].mean(axis=1)
            out["row_std"] = out[nums].std(axis=1)

    for col in out.select_dtypes(include=["object"]).columns:
        out[col] = LabelEncoder().fit_transform(out[col].astype(str))
    return out
