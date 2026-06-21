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

    categories = {
        "relevance": 0,
        "detail": 0,
        "clarity": 0,
        "structure": 0,
    }
    strengths = []
    improvements = []

    categories["relevance"] = min(len(matched_keywords), 4)
    if matched_keywords:
        strengths.append(f"You included useful terms: {', '.join(matched_keywords)}.")
    else:
        improvements.append("Your answer seems unrelated to the question. Focus on the topic asked.")
        improvements.append("Include more important role-related keywords in your answer.")

    if len(words) >= 25:
        categories["detail"] = 2
        strengths.append("Your answer has enough detail for a basic interview response.")
    elif len(words) >= 12:
        categories["detail"] = 1
        improvements.append("Add a little more explanation to make the answer stronger.")
    else:
        improvements.append("Add more explanation. A good interview answer should not be too short.")

    if "." in answer or "," in answer:
        categories["clarity"] = 2
        strengths.append("Your answer uses sentence structure instead of only keywords.")
    elif len(words) >= 8:
        categories["clarity"] = 1
        improvements.append("Use punctuation and complete sentences to sound more professional.")
    else:
        improvements.append("Write in complete sentences to sound more professional.")

    example_words = ["example", "because", "such as", "for instance", "helps", "important"]
    has_reason_or_example = any(word in lower_answer for word in example_words)
    if len(words) >= 50 or has_reason_or_example:
        categories["structure"] = 2
        strengths.append("Your answer includes reasoning or example-style explanation.")
    elif len(words) >= 25:
        categories["structure"] = 1
        improvements.append("Add an example or reason to make your answer stronger.")
    else:
        improvements.append("Try to add an example or reason to make your answer stronger.")

    score = sum(categories.values())
    if not matched_keywords:
        score = min(score, 3)
        categories["relevance"] = 0

    return {
        "score": min(score, 10),
        "categories": categories,
        "strengths": strengths,
        "improvements": improvements,
        "matched_keywords": matched_keywords,
    }


def get_category_summary(answers):
    if not answers:
        return {}

    category_names = ["relevance", "detail", "clarity", "structure"]
    summary = {}

    for category in category_names:
        total = sum(answer.get("categories", {}).get(category, 0) for answer in answers)
        summary[category] = total

    return summary


def normalize_attempt(attempt):
    for answer in attempt.get("answers", []):
        answer.setdefault(
            "categories",
            {
                "relevance": 0,
                "detail": 0,
                "clarity": 0,
                "structure": 0,
            },
        )
    attempt.setdefault("category_summary", get_category_summary(attempt.get("answers", [])))
    return attempt


def load_attempts():
    if not HISTORY_FILE.exists():
        return []

    with open(HISTORY_FILE, "r") as file:
        attempts = json.load(file)

    return [normalize_attempt(attempt) for attempt in attempts]


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


def build_dashboard_stats(attempts):
    if not attempts:
        return {
            "total_attempts": 0,
            "average_score": 0,
            "best_score": 0,
            "latest_score": 0,
            "latest_performance": "No attempts yet",
            "category_averages": {
                "relevance": 0,
                "detail": 0,
                "clarity": 0,
                "structure": 0,
            },
            "role_counts": {},
            "recent_attempts": [],
            "best_attempt": None,
        }

    total_attempts = len(attempts)
    total_score = sum(attempt["total_score"] for attempt in attempts)
    latest_attempt = attempts[-1]
    best_attempt = max(attempts, key=lambda attempt: attempt["total_score"])

    category_names = ["relevance", "detail", "clarity", "structure"]
    category_averages = {}
    for category in category_names:
        category_total = sum(
            attempt.get("category_summary", {}).get(category, 0)
            for attempt in attempts
        )
        category_averages[category] = round(category_total / total_attempts, 1)

    role_counts = {}
    for attempt in attempts:
        role = attempt["role"]
        role_counts[role] = role_counts.get(role, 0) + 1

    return {
        "total_attempts": total_attempts,
        "average_score": round(total_score / total_attempts, 1),
        "best_score": best_attempt["total_score"],
        "latest_score": latest_attempt["total_score"],
        "latest_performance": latest_attempt["performance"],
        "category_averages": category_averages,
        "role_counts": role_counts,
        "recent_attempts": list(reversed(attempts[-5:])),
        "best_attempt": best_attempt,
    }


def build_comparison(first_attempt, second_attempt):
    category_names = ["relevance", "detail", "clarity", "structure"]
    category_differences = {}

    for category in category_names:
        first_score = first_attempt.get("category_summary", {}).get(category, 0)
        second_score = second_attempt.get("category_summary", {}).get(category, 0)
        category_differences[category] = second_score - first_score

    score_difference = second_attempt["total_score"] - first_attempt["total_score"]

    if score_difference > 0:
        summary = f"Improved by {score_difference} marks."
    elif score_difference < 0:
        summary = f"Score decreased by {abs(score_difference)} marks."
    else:
        summary = "Score stayed the same."

    strongest_category = max(category_differences, key=lambda item: category_differences[item])
    weakest_category = min(
        second_attempt.get("category_summary", {}),
        key=lambda item: second_attempt["category_summary"][item],
    )

    return {
        "first": first_attempt,
        "second": second_attempt,
        "score_difference": score_difference,
        "category_differences": category_differences,
        "summary": summary,
        "strongest_category": strongest_category,
        "weakest_category": weakest_category,
    }


@app.route("/")
def home():
    return render_template("index.html", roles=questions.keys())


@app.route("/dashboard")
def dashboard():
    attempts = load_attempts()
    stats = build_dashboard_stats(attempts)
    return render_template("dashboard.html", stats=stats)


@app.route("/compare", methods=["GET", "POST"])
def compare():
    attempts = load_attempts()
    comparison = None
    error = None

    if request.method == "POST":
        first_id = request.form.get("first_attempt")
        second_id = request.form.get("second_attempt")

        if first_id == second_id:
            error = "Please select two different attempts."
        else:
            first_attempt = next((attempt for attempt in attempts if attempt["id"] == first_id), None)
            second_attempt = next((attempt for attempt in attempts if attempt["id"] == second_id), None)

            if first_attempt and second_attempt:
                comparison = build_comparison(first_attempt, second_attempt)
            else:
                error = "Could not find the selected attempts."

    return render_template(
        "compare.html",
        attempts=list(reversed(attempts)),
        comparison=comparison,
        error=error,
    )


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
            "categories": result["categories"],
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
    current_attempt["category_summary"] = get_category_summary(current_attempt["answers"])
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
            return render_template("history_detail.html", attempt=normalize_attempt(attempt))

    abort(404)


if __name__ == "__main__":
    app.run(debug=True)
