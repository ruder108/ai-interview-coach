# AI Interview Coach

AI Interview Coach is a Flask-based web application that helps students practice
mock interviews, receive structured feedback, track performance, and compare
previous attempts.

The project is designed for students preparing for internships and entry-level
technical interviews.

## Features

- Role-based interview practice
- Difficulty selection: Easy, Medium, Hard
- Three-question mock interview flow
- Rule-based answer evaluation
- Category-wise scoring
- Topic mismatch detection
- Complete final interview report
- Interview history with detailed attempt reports
- Progress dashboard
- Attempt comparison
- Works without any paid API key

## Supported Roles

- Data Analyst
- Software Developer
- AI/ML Engineer
- HR Interview
- Python Developer
- Cyber Security Intern
- Data Scientist

## Scoring System

Each answer is scored out of 10 marks using four categories:

| Category | Marks | What It Checks |
| --- | ---: | --- |
| Relevance | 4 | Whether the answer matches important topic keywords |
| Detail | 2 | Whether the answer has enough explanation |
| Clarity | 2 | Whether the answer uses readable sentences |
| Structure | 2 | Whether the answer includes reasoning or examples |

Each interview has 3 questions, so the total score is out of 30.

## Tech Stack

- Python
- Flask
- HTML
- CSS
- JSON file-based local history storage

## Project Structure

```text
ai-interview-coach/
|-- app.py
|-- requirements.txt
|-- README.md
|-- static/
|   `-- style.css
`-- templates/
    |-- index.html
    |-- interview.html
    |-- feedback.html
    |-- dashboard.html
    |-- history.html
    |-- history_detail.html
    `-- compare.html
```

## How to Run

Clone the repository:

```bash
git clone https://github.com/ruder108/ai-interview-coach.git
cd ai-interview-coach
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the Flask app:

```bash
python app.py
```

Open in browser:

```text
http://127.0.0.1:5000
```

## Screenshots

```text
Home Page
Progress Dashboard
Final Feedback Report
Attempt Comparison
```

## How It Works

1. The user enters their name, selects a role, and chooses a difficulty level.
2. The app asks three interview questions based on the selected role and difficulty.
3. The user submits answers one by one.
4. The system evaluates each answer using keyword relevance, detail, clarity, and structure.
5. A final report shows the total score, category scores, strengths, improvements, and sample answers.
6. Completed attempts are saved locally in `attempts.json`.
7. The dashboard summarizes progress and allows users to compare attempts.

## Why No API Key Is Required

This project intentionally works without Gemini, OpenAI, or any paid API key.
It uses rule-based evaluation so the app remains reliable during demos, GitHub
review, and recruiter testing.

Future versions can add optional AI-powered feedback while keeping the current
rule-based system as a fallback.

## Future Improvements

- Optional AI-powered feedback using an API key
- Resume-based question generation
- User login system
- More roles and question sets
- Charts for progress visualization
- Deployment on Render or Railway

## Author

Ruder Mittal  
AI & ML Student, The NorthCap University
