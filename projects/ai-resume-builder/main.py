import json
import sys
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

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

    doc.build(story)
    print("Resume created: " + output)

# load json and run
f = open(sys.argv[1])
data = json.load(f)
generate_resume(data)
# f.close() missing - file handle never closed
