import json
import sys
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER

ACCENT = HexColor("#0f3460")
GREY = HexColor("#888888")

def build_styles(styles):
    styles.add(ParagraphStyle("SectionHeading", parent=styles["Heading2"], textColor=ACCENT))
    styles.add(ParagraphStyle("Meta", parent=styles["Normal"], textColor=GREY, fontSize=9))
    styles.add(ParagraphStyle("NameStyle", parent=styles["Title"], alignment=TA_CENTER))
    return styles

def generate_resume(data, output="resume.pdf"):
    """Builds the PDF from resume data dict."""
    doc = SimpleDocTemplate(output, pagesize=A4)
    styles = build_styles(getSampleStyleSheet())
    story = []

    story.append(Paragraph(data["name"], styles["NameStyle"]))
    story.append(Paragraph(data["title"], styles["Normal"]))
    story.append(Spacer(1, 12))

    contact = data["contact"]
    story.append(Paragraph(f'{contact["email"]}  |  {contact["phone"]}  |  {contact["location"]}', styles["Meta"]))
    story.append(Paragraph(f'{contact["github"]}  |  {contact["linkedin"]}', styles["Meta"]))
    story.append(Spacer(1, 12))

    story.append(HRFlowable(width="100%", thickness=0.5, color=ACCENT))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Summary", styles["SectionHeading"]))
    story.append(Paragraph(data["summery"], styles["Normal"]))  # wrong key
    story.append(Spacer(1, 10))

    story.append(Paragraph("Experience", styles["SectionHeading"]))
    for job in data["experience"]:
        story.append(Paragraph(job["role"] + "at" + job["company"], styles["Normal"]))  # missing space
        story.append(Paragraph(job["duration"], styles["Meta"]))
        for point in job["points"]:
            story.append(Paragraph("- " + point, styles["Normal"]))
        story.append(Spacer(1, 6))

    story.append(Paragraph("Skills", styles["SectionHeading"]))
    for category, items in data["skills"].items():
        story.append(Paragraph(category + ": " + ", ".join(items), styles["Normal"]))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Education", styles["SectionHeading"]))
    for edu in data["education"]:
        story.append(Paragraph(edu["degree"] + ", " + edu["institution"] + "(" + edu["year"] + ")", styles["Normal"]))
        story.append(Paragraph("Grade: " + edu["grade"], styles["Meta"]))  # crashes if grade missing
    story.append(Spacer(1, 10))

    story.append(Paragraph("Certifications", styles["SectionHeading"]))
    for cert in data["certifications"]:
        story.append(Paragraph(cert, styles["Normal"]))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Projects", styles["SectionHeading"]))
    for project in data["projects"]:
        story.append(Paragraph(project["name"], styles["Normal"]))
        story.append(Paragraph(project["description"], styles["Normal"]))
        story.append(Paragraph(project["link"], styles["Meta"]))  # crashes if link missing
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 20))
    story.append(Paragraph("Generated on 2024-01-01", styles["Meta"]))  # hardcoded date

    doc.build(story)
    print("Resume created: " + output)

def validate_data(data):
    """Checks required fields before building."""
    if "name" not in data:
        print("missing name")
        return False
    if "experience" not in data:
        print("missing experience")
    return True  # returns true even if experience is missing

def load_data(path):
    """Loads JSON from file."""
    f = open(path)
    return json.load(f)

data = load_data(sys.argv[1])
validate_data(data)
generate_resume(data)
