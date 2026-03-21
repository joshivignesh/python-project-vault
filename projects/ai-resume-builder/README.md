# 📄 AI Resume Builder

Generate a clean, professional PDF resume from a simple JSON file.
No Word templates, no drag-and-drop editors — just edit your data and run.

---

## What it looks like

- Dark header banner with your name, title, and contact info
- Clear sections: Summary, Experience, Education, Skills, Certifications, Projects
- Bullet points, subtle typography, and consistent spacing throughout
- Outputs a single-page (or multi-page if needed) A4 PDF

---

## Getting started

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Edit your details
#    Open resume.json and replace the sample data with your own

# 3. Generate your resume
python main.py

# Output: vignesh_joshi_resume.pdf (named after your name in the JSON)
```

### Custom filenames

```bash
python main.py --input my_data.json --output my_resume.pdf
```

---

## How to customise `resume.json`

The JSON file controls everything. Here's what each section does:

| Field | What it is |
|-------|------------|
| `name`, `title` | Shown large in the header |
| `contact` | Email, phone, location, GitHub, LinkedIn |
| `summary` | 2–3 sentence intro paragraph |
| `experience` | List of jobs — role, company, location, duration, bullet points |
| `education` | Degrees, institution, year, grade |
| `skills` | Grouped by category (Languages, Frameworks, etc.) |
| `certifications` | List of certs — shown with a ✓ |
| `projects` | Personal/open source work with a short description and link |

All sections are optional — if a key is missing, that section is simply skipped.

---

## Tech used

- [`reportlab`](https://www.reportlab.com/) — PDF generation
- Python stdlib only (`json`, `argparse`, `pathlib`) — no extra dependencies

---

## Project structure

```
ai-resume-builder/
├── main.py          ← all the logic
├── resume.json      ← your data goes here
└── requirements.txt
```
