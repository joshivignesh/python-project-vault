# AI Resume Builder

Generate a clean, professional PDF resume from a JSON file.

## Setup

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py --input resume.json
python main.py --input resume.json --output my_resume.pdf
```

## Input

Edit `resume.json` with your details. Supported sections:

| Field | Required |
|-------|----------|
| name, title, contact | ✅ |
| summary, experience | ✅ |
| skills, education | optional |
| certifications, projects | optional |

## Output

A single PDF file named after your input or `--output` flag.
