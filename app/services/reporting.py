from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def generate_html_report(summary: dict, charts: list[str], out_path: Path):
    html = ["<html><head><title>Analytics Report</title></head><body>"]
    html.append("<h1>Executive Summary</h1>")
    html.append(f"<p>{summary.get('executive_summary', '')}</p>")
    html.append("<h2>Key Findings</h2><ul>")
    for item in summary.get("key_findings", []):
        html.append(f"<li>{item}</li>")
    html.append("</ul><h2>Recommendations</h2><ul>")
    for item in summary.get("recommendations", []):
        html.append(f"<li>{item}</li>")
    html.append("</ul><h2>Feature Importance</h2><ol>")
    for row in summary.get("feature_importance", [])[:10]:
        html.append(f"<li>{row['feature']}: {row['importance']:.4f}</li>")
    html.append("</ol>")
    for chart in charts:
        chart_name = Path(chart).name
        html.append(f"<h3>{chart_name}</h3><img src='{chart_name}' width='800' />")
    html.append("</body></html>")
    out_path.write_text("\n".join(html), encoding="utf-8")


def generate_pdf_report(summary: dict, out_path: Path):
    c = canvas.Canvas(str(out_path), pagesize=A4)
    width, height = A4
    y = height - 40
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y, "AI-Powered Data Analytics Report")
    y -= 25
    c.setFont("Helvetica", 10)
    for line in [
        f"Data Quality Score: {summary.get('data_quality_score', 'N/A')}",
        f"Prediction Readiness: {summary.get('prediction_readiness', 'N/A')}",
        "Key Findings:",
    ] + [f"- {k}" for k in summary.get("key_findings", [])]:
        if y < 40:
            c.showPage()
            y = height - 40
        c.drawString(40, y, str(line)[:120])
        y -= 16
    c.save()
