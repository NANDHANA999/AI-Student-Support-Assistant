# AI Student Support Assistant

A Python terminal assistant for retrieving academic information from student
resources. This implementation demonstrates the workflow described in the
internship report:

**student query → resource retrieval → response**

It also includes optional OCR support for image-based notices using Tesseract.

## Features

- Natural-language-style terminal queries
- Keyword-based information retrieval from `.txt` and `.md` resources
- Sample examination schedule, student guidelines, and library hours
- Optional OCR extraction from scanned or image-based notices
- One-shot query mode for scripts and demonstrations
- No API keys or external services required

## Run it

```bash
python main.py
```

Try:

```text
What is the exam schedule?
What are the student guidelines?
What are the library hours?
```

Run a single query:

```bash
python main.py --query "What are the student guidelines?"
```

## OCR setup

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

Install the Tesseract system application separately, then run:

```bash
python main.py --ocr examination_notice.png
```

The extracted text is saved as `resources/examination_notice_ocr.txt` and is
available to the assistant on the next run.

## Project structure

```text
AI-Student-Support-Assistant/
├── main.py
├── ocr_module.py
├── requirements.txt
├── resources/
│   ├── examination_schedule.txt
│   ├── library_hours.txt
│   └── student_guidelines.txt
├── docs/
│   └── AI_Student_Support_Assistant_Internship_Report.pdf
└── README.md
```

The files in `resources/` are demonstration data. Replace them with
institution-approved notices and support documents for real use.