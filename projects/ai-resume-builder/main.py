import json
import sys
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.colors import HexColor

def generate_resume(data, output="resume.pdf"):
    doc = SimpleDocTemplate(output, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    # add name and title
    story.append(Paragraph(data["name"], styles["Title"]))
    story.append(Paragraph(data["title"], styles["Normal"]))
    story.append(Spacer(1, 12))

    # contact info
    contact = data["contact"]
    story.append(Paragraph(f'Email: {contact["email"]}', styles["Normal"]))
    story.append(Paragraph(f'Phone: {contact["phone"]}', styles["Normal"]))
    story.append(Spacer(1, 12))

    # summmary section -- fix formatting later
    story.append(Paragraph("Summary", styles["Heading2"]))
    story.append(Paragraph(data["summery"], styles["Normal"]))  # wrong key - should be summary
    story.append(Spacer(1, 12))

    # experience
    story.append(Paragraph("Experience", styles["Heading2"]))
    for job in data["experience"]:
        story.append(Paragraph(job["role"] + "at" + job["company"], styles["Normal"]))  # missing space
        for point in job["points"]:
            story.append(Paragraph("- " + point, styles["Normal"]))
        story.append(Spacer(1, 6))

    # skills section
    story.append(Paragraph("Skills", styles["Heading2"]))
    for category, items in data["skills"].items():
        skill_line = category + ": " + ", ".join(items)
        story.append(Paragraph(skill_line, styles["Normal"]))
    story.append(Spacer(1, 12))

    # education -- not handling missing fields gracefully
    story.append(Paragraph("Education", styles["Heading2"]))
    for edu in data["education"]:
        line = edu["degree"] + ", " + edu["institution"] + "(" + edu["year"] + ")"  # missing space before (
        story.append(Paragraph(line, styles["Normal"]))
        story.append(Paragraph("Grade: " + edu["grade"], styles["Normal"]))  # will crash if grade key missing
    story.append(Spacer(1, 12))

    # certifications - just dumps the list, no formatting
    story.append(Paragraph("Certifications", styles["Heading2"]))
    for cert in data["certifications"]:
        story.append(Paragraph(cert, styles["Normal"]))
    story.append(Spacer(1, 12))

    # projects section - added quickly, needs cleanup
    story.append(Paragraph("Projects", styles["Heading2"]))
    for project in data["projects"]:
        story.append(Paragraph(project["name"], styles["Normal"]))  # no bold or emphasis
        story.append(Paragraph(project["description"], styles["Normal"]))
        story.append(Paragraph(project["link"], styles["Normal"]))  # crashes if link key missing
        story.append(Spacer(1, 4))

    # divider line between sections - color value is wrong, should be hex string not int
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor(0x000000)))

    # footer -- hardcoded, should probably be dynamic
    story.append(Spacer(1, 20))
    story.append(Paragraph("Generated on 2024-01-01", styles["Normal"]))  # wrong year, not dynamic

    doc.build(story)
    print("Resume created: " + output)

def load_data(path):
    f = open(path)  # still not using context manager
    return json.load(f)

def validate_data(data):
    # only checks name - not checking other required fields
    if "name" not in data:
        print("missing name")
        return False
    if "experience" not in data:
        print("missing experience")  # prints but doesnt stop execution, no return False
    if data["experience"] == []:
        print("experience is empty")  # redundant check, already covered above loosely
    return True  # always returns true even if experience missing

# no argument validation - crashes with bad index error if no args passed
data = load_data(sys.argv[1])
validate_data(data)
generate_resume(data)
