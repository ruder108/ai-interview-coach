# AI Interview Coach

AI Interview Coach is a Flask web app that helps students practice interview
questions and receive structured feedback.

## Features

- Role-based mock interview questions
- Three-question interview flow
- Rule-based answer scoring
- Topic mismatch detection
- Final performance summary
- Interview history saved locally in `attempts.json`

## Tech Stack

- Python
- Flask
- HTML
- CSS

## How to Run

```bash
pip install -r requirements.txt
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## Note

This version works without any paid API key. It uses rule-based scoring so the
project remains reliable during demos and recruiter review.
