from pathlib import Path
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def create_pdf_report(df: pd.DataFrame, cleaning_stats: dict, fi: list[dict], charts: list[str], out: Path):
    c = canvas.Canvas(str(out), pagesize=A4)
    w, h = A4
    y = h - 40

    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y, "AI Data Analyst Report")
    y -= 20
    c.setFont("Helvetica", 10)
    lines = [
        f"Rows: {len(df)} Columns: {len(df.columns)}",
        f"Data quality score: {cleaning_stats.get('quality_score', 'N/A')}",
        f"Duplicates removed: {cleaning_stats.get('duplicates_removed', 0)}",
        "Top features:",
    ] + [f"- {r['feature']}: {r['importance']:.4f}" for r in fi[:8]]

    for line in lines:
        c.drawString(40, y, line[:120])
        y -= 14
        if y < 60:
            c.showPage(); y = h - 40

    c.drawString(40, y, f"Charts generated: {len([c for c in charts if c])}")
    c.save()
