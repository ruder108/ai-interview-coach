import json
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from flask import Flask, abort, render_template, request, session


app = Flask(__name__)
app.secret_key = "ai-interview-coach-dev-key"

HISTORY_FILE = Path("attempts.json")

questions = {
    "Data Analyst": [
        {
            "question": "What is data cleaning?",
            "keywords": ["missing values", "duplicates", "accuracy", "quality", "inconsistent"],
            "sample_answer": "Data cleaning means fixing or removing missing, duplicate, incorrect, or inconsistent data so analysis becomes more accurate.",
        },
        {
            "question": "What is SQL?",
            "keywords": ["database", "query", "tables", "select", "data"],
            "sample_answer": "SQL is a language used to store, manage, and query data from relational databases using commands like SELECT, INSERT, UPDATE, and DELETE.",
        },
        {
            "question": "What is data visualization?",
            "keywords": ["charts", "graphs", "patterns", "insights", "dashboard"],
            "sample_answer": "Data visualization means representing data using charts, graphs, or dashboards so patterns and insights can be understood easily.",
        },
    ],
    "Software Developer": [
        {
            "question": "Explain OOP.",
            "keywords": ["class", "object", "inheritance", "encapsulation", "polymorphism"],
            "sample_answer": "OOP is a programming approach based on classes and objects. It helps organize code using concepts like inheritance, encapsulation, and polymorphism.",
        },
        {
            "question": "What is inheritance?",
            "keywords": ["parent", "child", "class", "reuse", "extends"],
            "sample_answer": "Inheritance allows one class to use properties and methods of another class, helping developers reuse code.",
        },
        {
            "question": "What is a class?",
            "keywords": ["blueprint", "object", "methods", "attributes", "template"],
            "sample_answer": "A class is a blueprint for creating objects. It defines attributes and methods that objects can use.",
        },
    ],
    "AI/ML Engineer": [
        {
            "question": "What is supervised learning?",
            "keywords": ["labeled", "training", "input", "output", "classification"],
            "sample_answer": "Supervised learning is a machine learning method where the model learns from labeled input-output examples.",
        },
        {
            "question": "What is overfitting?",
            "keywords": ["training data", "generalize", "test data", "noise", "model"],
            "sample_answer": "Overfitting happens when a model learns the training data too closely and performs poorly on new or test data.",
        },
        {
            "question": "What is a neural network?",
            "keywords": ["neurons", "layers", "weights", "input", "output"],
            "sample_answer": "A neural network is a machine learning model inspired by the brain. It uses layers of connected neurons to learn patterns from data.",
        },
    ],
}


def evaluate_answer(answer, keywords):
    words = answer.split()
    lower_answer = answer.lower()
    matched_keywords = [keyword for keyword in keywords if keyword.lower() in lower_answer]

    score = 0
    strengths = []
    improvements = []

    if len(words) >= 25:
        score += 3
        strengths.append("Your answer has enough detail for a basic interview response.")
    else:
        improvements.append("Add more explanation. A good interview answer should not be too short.")

    score += min(len(matched_keywords), 4)

    if matched_keywords:
        strengths.append(f"You included useful terms: {', '.join(matched_keywords)}.")
    else:
        improvements.append("Your answer seems unrelated to the question. Focus on the topic asked.")
        improvements.append("Include more important role-related keywords in your answer.")

    if "." in answer or "," in answer:
        score += 1
        strengths.append("Your answer uses sentence structure instead of only keywords.")
    else:
        improvements.append("Write in complete sentences to sound more professional.")

    if len(words) >= 50:
        score += 2
        strengths.append("Your answer gives a more complete explanation.")
    else:
        improvements.append("Try to add an example or reason to make your answer stronger.")

    if not matched_keywords:
        score = min(score, 3)

    return {
        "score": min(score, 10),
        "strengths": strengths,
        "improvements": improvements,
        "matched_keywords": matched_keywords,
    }


def load_attempts():
    if not HISTORY_FILE.exists():
        return []

    with open(HISTORY_FILE, "r") as file:
        return json.load(file)


def save_attempt(attempt):
    attempts = load_attempts()
    attempts.append(attempt)

    with open(HISTORY_FILE, "w") as file:
        json.dump(attempts, file, indent=4)


def get_performance(total_score):
    if total_score >= 24:
        return (
            "Excellent",
            "Outstanding performance! You demonstrated strong interview skills.",
        )
    if total_score >= 16:
        return (
            "Good",
            "Good performance. With more practice, you can improve further.",
        )

    return (
        "Needs Improvement",
        "Keep practicing. Focus on giving more detailed answers.",
    )


@app.route("/")
def home():
    return render_template("index.html", roles=questions.keys())


@app.route("/interview", methods=["POST"])
def interview():
    username = request.form["username"].strip()
    role = request.form["role"]
    question_data = questions[role][0]
    session["current_attempt"] = {
        "id": str(uuid4()),
        "username": username,
        "role": role,
        "answers": [],
    }

    return render_template(
        "interview.html",
        username=username,
        role=role,
        question=question_data["question"],
        question_index=0,
        total_score=0,
    )


@app.route("/feedback", methods=["POST"])
def feedback():
    username = request.form["username"]
    question = request.form["question"]
    answer = request.form["answer"]
    role = request.form["role"]
    question_index = int(request.form["question_index"])
    next_index = question_index + 1
    total_score = int(request.form["total_score"])
    current_question = questions[role][question_index]
    result = evaluate_answer(answer, current_question["keywords"])
    score = result["score"]
    total_score += score
    current_attempt = session.get("current_attempt")

    if not current_attempt:
        current_attempt = {
            "id": str(uuid4()),
            "username": username,
            "role": role,
            "answers": [],
        }

    current_attempt["answers"].append(
        {
            "question": question,
            "answer": answer,
            "score": score,
            "strengths": result["strengths"],
            "improvements": result["improvements"],
            "sample_answer": current_question["sample_answer"],
        }
    )
    session["current_attempt"] = current_attempt

    if next_index < len(questions[role]):
        next_question = questions[role][next_index]

        return render_template(
            "interview.html",
            username=username,
            role=role,
            question=next_question["question"],
            question_index=next_index,
            total_score=total_score,
        )

    performance, feedback_text = get_performance(total_score)
    current_attempt["total_score"] = total_score
    current_attempt["performance"] = performance
    current_attempt["feedback_text"] = feedback_text
    current_attempt["created_at"] = datetime.now().strftime("%d %b %Y, %I:%M %p")
    save_attempt(current_attempt)
    session.pop("current_attempt", None)

    return render_template(
        "feedback.html",
        username=username,
        score=total_score,
        performance=performance,
        feedback_text=feedback_text,
        attempt=current_attempt,
    )


@app.route("/history")
def history():
    return render_template(
        "history.html",
        attempts=load_attempts(),
    )


@app.route("/history/<attempt_id>")
def history_detail(attempt_id):
    for attempt in load_attempts():
        if attempt["id"] == attempt_id:
            return render_template("history_detail.html", attempt=attempt)

    abort(404)


if __name__ == "__main__":
    app.run(debug=True)
