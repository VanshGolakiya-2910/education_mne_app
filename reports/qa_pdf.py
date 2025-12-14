from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def generate_qa_pdf(path, qa_report, severity):
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(path)
    story = []

    story.append(Paragraph("<b>Data Quality Assurance Report</b>", styles["Title"]))
    story.append(Paragraph(f"Total rows: {qa_report['total_rows']}", styles["Normal"]))
    story.append(Paragraph(f"Severity level: {severity}", styles["Normal"]))

    story.append(Paragraph("<b>Missing Values (%)</b>", styles["Heading2"]))
    for k, v in qa_report["missing_values_percent"].items():
        story.append(Paragraph(f"{k}: {v}%", styles["Normal"]))

    story.append(Paragraph(
        f"Bound violations: {qa_report['bound_violations']}", styles["Normal"]
    ))
    story.append(Paragraph(
        f"Logic violations: {qa_report['logic_violations']}", styles["Normal"]
    ))

    doc.build(story)
