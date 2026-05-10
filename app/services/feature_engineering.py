import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for col in out.columns:
        if out[col].dtype == "object":
            parsed = pd.to_datetime(out[col], errors="coerce")
            if parsed.notna().sum() > 0.6 * len(out):
                out[f"{col}_year"] = parsed.dt.year
                out[f"{col}_month"] = parsed.dt.month
                out[f"{col}_day"] = parsed.dt.day

    numeric_cols = out.select_dtypes(include=[np.number]).columns.tolist()
    if len(numeric_cols) >= 2:
        out["row_numeric_mean"] = out[numeric_cols].mean(axis=1)
        out["row_numeric_std"] = out[numeric_cols].std(axis=1)

    for col in out.select_dtypes(include=["object"]).columns:
        le = LabelEncoder()
        out[col] = le.fit_transform(out[col].astype(str))

    return out


def compute_feature_importance(df: pd.DataFrame):
    numeric = df.select_dtypes(include=[np.number]).copy()
    if numeric.shape[1] < 2:
        return []

    target = numeric.columns[-1]
    X = numeric.drop(columns=[target]).fillna(0)
    y = numeric[target].fillna(0)

    if len(X.columns) == 0:
        return []

    model = RandomForestRegressor(n_estimators=120, random_state=42)
    model.fit(X, y)

    ranking = sorted(
        [{"feature": col, "importance": float(imp)} for col, imp in zip(X.columns, model.feature_importances_)],
        key=lambda x: x["importance"],
        reverse=True,
    )
    return ranking[:20]
