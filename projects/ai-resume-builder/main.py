"""
ai-resume-builder
-----------------
Generates a clean, professional PDF resume from a JSON file.

Usage:
    python main.py                        # uses resume.json in current directory
    python main.py --input my_data.json   # custom input file
    python main.py --output cv.pdf        # custom output filename
"""

import json
import argparse
from pathlib import Path
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT


# ── Colour palette ────────────────────────────────────────────────────────────
DARK        = HexColor("#1a1a2e")   # header background
ACCENT      = HexColor("#0f3460")   # section headings
LIGHT_GREY  = HexColor("#f5f5f5")   # skill tag background
MID_GREY    = HexColor("#888888")   # secondary text
RULE_COLOUR = HexColor("#dddddd")   # horizontal rules

# ── Page margins ──────────────────────────────────────────────────────────────
LEFT   = 18 * mm
RIGHT  = 18 * mm
TOP    = 14 * mm
BOTTOM = 14 * mm


def build_styles():
    base = getSampleStyleSheet()

    def style(name, **kwargs):
        return ParagraphStyle(name, parent=base["Normal"], **kwargs)

    return {
        "name": style(
            "Name",
            fontSize=26,
            textColor=white,
            fontName="Helvetica-Bold",
            alignment=TA_CENTER,
            spaceAfter=2,
        ),
        "title": style(
            "Title",
            fontSize=12,
            textColor=HexColor("#aac4e8"),
            fontName="Helvetica",
            alignment=TA_CENTER,
            spaceAfter=6,
        ),
        "contact": style(
            "Contact",
            fontSize=8.5,
            textColor=HexColor("#ccddee"),
            fontName="Helvetica",
            alignment=TA_CENTER,
            spaceAfter=0,
        ),
        "section": style(
            "Section",
            fontSize=11,
            textColor=ACCENT,
            fontName="Helvetica-Bold",
            spaceBefore=10,
            spaceAfter=3,
        ),
        "job_title": style(
            "JobTitle",
            fontSize=10,
            textColor=black,
            fontName="Helvetica-Bold",
            spaceAfter=1,
        ),
        "job_meta": style(
            "JobMeta",
            fontSize=8.5,
            textColor=MID_GREY,
            fontName="Helvetica",
            spaceAfter=3,
        ),
        "bullet": style(
            "Bullet",
            fontSize=9,
            textColor=HexColor("#333333"),
            fontName="Helvetica",
            leftIndent=12,
            spaceAfter=2,
            bulletIndent=4,
            bulletText="•",
        ),
        "body": style(
            "Body",
            fontSize=9,
            textColor=HexColor("#444444"),
            fontName="Helvetica",
            spaceAfter=4,
            leading=13,
        ),
        "skill_label": style(
            "SkillLabel",
            fontSize=9,
            textColor=ACCENT,
            fontName="Helvetica-Bold",
            spaceAfter=2,
        ),
        "skill_value": style(
            "SkillValue",
            fontSize=8.5,
            textColor=HexColor("#333333"),
            fontName="Helvetica",
            spaceAfter=4,
        ),
        "cert": style(
            "Cert",
            fontSize=9,
            textColor=HexColor("#333333"),
            fontName="Helvetica",
            spaceAfter=2,
            leftIndent=12,
            bulletIndent=4,
            bulletText="✓",
        ),
        "project_name": style(
            "ProjectName",
            fontSize=9.5,
            textColor=ACCENT,
            fontName="Helvetica-Bold",
            spaceAfter=1,
        ),
        "project_desc": style(
            "ProjectDesc",
            fontSize=8.5,
            textColor=HexColor("#444444"),
            fontName="Helvetica",
            spaceAfter=1,
            leftIndent=12,
        ),
        "project_link": style(
            "ProjectLink",
            fontSize=8,
            textColor=MID_GREY,
            fontName="Helvetica-Oblique",
            spaceAfter=5,
            leftIndent=12,
        ),
    }


def rule(width="100%"):
    return HRFlowable(width=width, thickness=0.5, color=RULE_COLOUR, spaceAfter=4, spaceBefore=0)


def section_heading(text, styles):
    return [
        Paragraph(text.upper(), styles["section"]),
        rule(),
    ]


def header_block(data, styles, page_width):
    """Dark banner with name, title, and contact info."""
    name       = data.get("name", "")
    title      = data.get("title", "")
    contact    = data.get("contact", {})

    contact_parts = []
    if contact.get("email"):    contact_parts.append(contact["email"])
    if contact.get("phone"):    contact_parts.append(contact["phone"])
    if contact.get("location"): contact_parts.append(contact["location"])
    contact_line1 = "   |   ".join(contact_parts)

    link_parts = []
    if contact.get("github"):   link_parts.append(contact["github"])
    if contact.get("linkedin"): link_parts.append(contact["linkedin"])
    contact_line2 = "   |   ".join(link_parts)

    inner_width = page_width - LEFT - RIGHT

    banner = Table(
        [
            [Paragraph(name, styles["name"])],
            [Paragraph(title, styles["title"])],
            [Paragraph(contact_line1, styles["contact"])],
            [Paragraph(contact_line2, styles["contact"])],
        ],
        colWidths=[inner_width],
    )
    banner.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), DARK),
        ("TOPPADDING",    (0, 0), (-1, -1), 14),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, -1), (-1, -1), 14),
    ]))
    return banner


def experience_block(experience, styles):
    elements = []
    for job in experience:
        elements.append(Paragraph(job.get("role", ""), styles["job_title"]))
        meta = f"{job.get('company', '')}  ·  {job.get('location', '')}  ·  {job.get('duration', '')}"
        elements.append(Paragraph(meta, styles["job_meta"]))
        for point in job.get("points", []):
            elements.append(Paragraph(point, styles["bullet"]))
        elements.append(Spacer(1, 4))
    return elements


def education_block(education, styles):
    elements = []
    for edu in education:
        degree = edu.get("degree", "")
        inst   = edu.get("institution", "")
        year   = edu.get("year", "")
        grade  = edu.get("grade", "")
        elements.append(Paragraph(degree, styles["job_title"]))
        meta = f"{inst}  ·  Graduated {year}"
        if grade:
            meta += f"  ·  {grade}"
        elements.append(Paragraph(meta, styles["job_meta"]))
    return elements


def skills_block(skills, styles):
    elements = []
    for category, items in skills.items():
        elements.append(Paragraph(category, styles["skill_label"]))
        elements.append(Paragraph("  ·  ".join(items), styles["skill_value"]))
    return elements


def certifications_block(certs, styles):
    return [Paragraph(cert, styles["cert"]) for cert in certs]


def projects_block(projects, styles):
    elements = []
    for proj in projects:
        elements.append(Paragraph(proj.get("name", ""), styles["project_name"]))
        elements.append(Paragraph(proj.get("description", ""), styles["project_desc"]))
        if proj.get("link"):
            elements.append(Paragraph(proj["link"], styles["project_link"]))
    return elements


def build_pdf(data: dict, output_path: str):
    page_width, page_height = A4

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=LEFT,
        rightMargin=RIGHT,
        topMargin=TOP,
        bottomMargin=BOTTOM,
        title=f"{data.get('name', 'Resume')} — Resume",
        author=data.get("name", ""),
    )

    styles = build_styles()
    story  = []

    # Header banner
    story.append(header_block(data, styles, page_width))
    story.append(Spacer(1, 8))

    # Summary
    if data.get("summary"):
        story += section_heading("Summary", styles)
        story.append(Paragraph(data["summary"], styles["body"]))

    # Experience
    if data.get("experience"):
        story += section_heading("Experience", styles)
        story += experience_block(data["experience"], styles)

    # Education
    if data.get("education"):
        story += section_heading("Education", styles)
        story += education_block(data["education"], styles)

    # Skills
    if data.get("skills"):
        story += section_heading("Skills", styles)
        story += skills_block(data["skills"], styles)

    # Certifications
    if data.get("certifications"):
        story += section_heading("Certifications", styles)
        story += certifications_block(data["certifications"], styles)

    # Projects
    if data.get("projects"):
        story += section_heading("Projects", styles)
        story += projects_block(data["projects"], styles)

    doc.build(story)
    print(f"✅  Resume saved → {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate a PDF resume from a JSON file."
    )
    parser.add_argument(
        "--input", "-i",
        default="resume.json",
        help="Path to your resume JSON file (default: resume.json)",
    )
    parser.add_argument(
        "--output", "-o",
        default=None,
        help="Output PDF filename (default: <your_name>_resume.pdf)",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"❌  Could not find input file: {input_path}")
        return

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if args.output:
        output_path = args.output
    else:
        safe_name = data.get("name", "resume").lower().replace(" ", "_")
        output_path = f"{safe_name}_resume.pdf"

    build_pdf(data, output_path)


if __name__ == "__main__":
    main()
