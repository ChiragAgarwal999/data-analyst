from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def create_charts(df: pd.DataFrame, out_dir: Path) -> list[str]:
    charts = []
    num = df.select_dtypes(include=[np.number])
    if not num.empty:
        p1 = out_dir / "hist.png"
        num.hist(figsize=(10, 6))
        plt.tight_layout(); plt.savefig(p1); plt.close("all")
        charts.append(str(p1))
    if num.shape[1] > 1:
        p2 = out_dir / "corr.png"
        corr = num.corr(numeric_only=True)
        plt.figure(figsize=(7, 5)); plt.imshow(corr, cmap="coolwarm", aspect="auto"); plt.colorbar()
        plt.tight_layout(); plt.savefig(p2); plt.close("all")
        charts.append(str(p2))
    return charts


def feature_importance_plot(ranking: list[dict], out_dir: Path) -> str:
    p = out_dir / "feature_importance.png"
    top = ranking[:10]
    if top:
        names = [t["feature"] for t in top]
        values = [t["importance"] for t in top]
        plt.figure(figsize=(8, 4)); plt.barh(names[::-1], values[::-1]); plt.tight_layout(); plt.savefig(p); plt.close("all")
    return str(p)
