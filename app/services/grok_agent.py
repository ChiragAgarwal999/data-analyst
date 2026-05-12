import json
import os


def decide_strategy(dataset_summary: dict) -> dict:
    """Decision engine stub.

    If GROK_API_KEY is configured, this function is where a real Grok API call should happen.
    For now, returns deterministic JSON policy compatible with production fallback behavior.
    """
    _ = os.getenv("GROK_API_KEY")

    columns = dataset_summary.get("columns", [])
    numeric_cols = dataset_summary.get("numeric_columns", [])
    target_candidates = [c for c in columns if any(k in c for k in ["target", "label", "sales", "price", "revenue", "cost"])]

    strategy = {
        "imputation": {c: "median" for c in numeric_cols},
        "drop_columns": [c for c in columns if c.startswith("unnamed")],
        "target_candidates": target_candidates[:5],
        "ml_model_type": "regression" if any(k in " ".join(columns) for k in ["price", "sales", "revenue", "cost"]) else "classification",
        "feature_suggestions": ["datetime decomposition", "row aggregations"],
    }
    return json.loads(json.dumps(strategy))
