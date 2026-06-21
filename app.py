import json
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from flask import Flask, abort, render_template, request, session


app = Flask(__name__)
app.secret_key = "ai-interview-coach-dev-key"

HISTORY_FILE = Path("attempts.json")
DIFFICULTIES = ["Easy", "Medium", "Hard"]

questions = {
    "Data Analyst": [
        {
            "question": "What is data cleaning?",
            "keywords": ["missing values", "duplicates", "accuracy", "quality", "inconsistent"],
            "sample_answer": "Data cleaning is the process of identifying and correcting errors, inconsistencies, duplicate records, and missing values in a dataset to improve its quality and accuracy.",
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
    "HR Interview": [
        {
            "question": "Tell me about yourself.",
            "keywords": ["education", "skills", "project", "goal", "strength"],
            "sample_answer": "A good answer briefly introduces your education, important skills, one relevant project, your career goal, and a strength related to the role.",
        },
        {
            "question": "Why should we hire you?",
            "keywords": ["skills", "learn", "project", "team", "value"],
            "sample_answer": "You should connect your skills, learning attitude, project experience, teamwork, and the value you can bring to the company.",
        },
        {
            "question": "What are your strengths and weaknesses?",
            "keywords": ["strength", "weakness", "improve", "example", "learning"],
            "sample_answer": "A strong answer gives one real strength with an example and one weakness with steps you are taking to improve it.",
        },
    ],
    "Python Developer": [
        {
            "question": "What are Python lists and tuples?",
            "keywords": ["list", "tuple", "mutable", "immutable", "ordered"],
            "sample_answer": "Lists and tuples are ordered collections in Python. Lists are mutable, so they can be changed, while tuples are immutable.",
        },
        {
            "question": "What is a Python function?",
            "keywords": ["function", "def", "parameters", "return", "reuse"],
            "sample_answer": "A Python function is a reusable block of code created using def. It can take parameters and return a result.",
        },
        {
            "question": "What is exception handling in Python?",
            "keywords": ["try", "except", "error", "handle", "program"],
            "sample_answer": "Exception handling uses try and except blocks to handle errors safely so the program does not stop unexpectedly.",
        },
    ],
    "Cyber Security Intern": [
        {
            "question": "What is phishing?",
            "keywords": ["fake", "email", "password", "attack", "security"],
            "sample_answer": "Phishing is a cyber attack where attackers use fake emails or websites to trick users into sharing passwords or sensitive information.",
        },
        {
            "question": "What is two-factor authentication?",
            "keywords": ["password", "otp", "verification", "security", "login"],
            "sample_answer": "Two-factor authentication adds an extra verification step, such as an OTP, along with a password to make login more secure.",
        },
        {
            "question": "What is malware?",
            "keywords": ["software", "harmful", "virus", "system", "damage"],
            "sample_answer": "Malware is harmful software such as viruses or spyware that can damage systems, steal data, or disrupt normal computer activity.",
        },
    ],
    "Data Scientist": [
        {
            "question": "What is feature engineering?",
            "keywords": ["features", "data", "model", "transform", "performance"],
            "sample_answer": "Feature engineering is the process of creating or transforming input data features to improve a machine learning model's performance.",
        },
        {
            "question": "What is model evaluation?",
            "keywords": ["accuracy", "precision", "recall", "test data", "performance"],
            "sample_answer": "Model evaluation means checking how well a model performs on test data using metrics like accuracy, precision, recall, or F1-score.",
        },
        {
            "question": "What is the difference between classification and regression?",
            "keywords": ["classification", "regression", "category", "continuous", "prediction"],
            "sample_answer": "Classification predicts categories, such as pass or fail, while regression predicts continuous values, such as marks or price.",
        },
    ],
}

easy_questions = {
    "Data Analyst": [
        {
            "question": "What is data?",
            "keywords": ["facts", "information", "numbers", "records", "values"],
            "sample_answer": "Data is a collection of facts, numbers, records, or information that can be used for analysis and decision-making.",
        },
        {
            "question": "What is a table in a database?",
            "keywords": ["rows", "columns", "database", "records", "data"],
            "sample_answer": "A table stores data in rows and columns inside a database. Each row is a record and each column represents a field.",
        },
        {
            "question": "Why are charts useful?",
            "keywords": ["visual", "data", "understand", "patterns", "compare"],
            "sample_answer": "Charts are useful because they make data easier to understand, compare, and identify patterns visually.",
        },
    ],
    "Software Developer": [
        {
            "question": "What is programming?",
            "keywords": ["instructions", "computer", "code", "software", "problem"],
            "sample_answer": "Programming is the process of writing instructions for a computer to solve problems or build software.",
        },
        {
            "question": "What is a variable?",
            "keywords": ["store", "value", "data", "name", "memory"],
            "sample_answer": "A variable is a named storage location used to store a value or data in a program.",
        },
        {
            "question": "What is debugging?",
            "keywords": ["error", "fix", "bug", "code", "test"],
            "sample_answer": "Debugging is the process of finding and fixing errors or bugs in code.",
        },
    ],
    "AI/ML Engineer": [
        {
            "question": "What is artificial intelligence?",
            "keywords": ["machine", "human", "intelligence", "learn", "decision"],
            "sample_answer": "Artificial intelligence is the ability of machines to perform tasks that normally require human intelligence, such as learning or decision-making.",
        },
        {
            "question": "What is machine learning?",
            "keywords": ["data", "learn", "model", "patterns", "prediction"],
            "sample_answer": "Machine learning is a part of AI where models learn patterns from data and make predictions or decisions.",
        },
        {
            "question": "What is training data?",
            "keywords": ["data", "model", "learn", "examples", "training"],
            "sample_answer": "Training data is the data used to teach a machine learning model how to recognize patterns and make predictions.",
        },
    ],
    "HR Interview": [
        {
            "question": "Introduce yourself briefly.",
            "keywords": ["name", "education", "skills", "project", "goal"],
            "sample_answer": "A brief introduction should include your name, education, skills, one project, and your career goal.",
        },
        {
            "question": "Why do you want this internship?",
            "keywords": ["learn", "experience", "skills", "career", "company"],
            "sample_answer": "A good answer explains that you want to learn, gain real experience, improve your skills, and contribute to the company.",
        },
        {
            "question": "What is one of your strengths?",
            "keywords": ["strength", "example", "skill", "work", "learn"],
            "sample_answer": "Mention one real strength and support it with a small example from your studies, project, or teamwork.",
        },
    ],
    "Python Developer": [
        {
            "question": "What is Python?",
            "keywords": ["programming", "language", "simple", "readable", "code"],
            "sample_answer": "Python is a popular programming language known for simple syntax, readability, and use in web development, data analysis, and AI.",
        },
        {
            "question": "What is a loop in Python?",
            "keywords": ["repeat", "for", "while", "code", "iteration"],
            "sample_answer": "A loop is used to repeat code. Python commonly uses for loops and while loops.",
        },
        {
            "question": "What is an if statement?",
            "keywords": ["condition", "decision", "true", "false", "code"],
            "sample_answer": "An if statement is used to make decisions in code by running a block only when a condition is true.",
        },
    ],
    "Cyber Security Intern": [
        {
            "question": "What is cyber security?",
            "keywords": ["protect", "systems", "data", "attacks", "security"],
            "sample_answer": "Cyber security is the practice of protecting systems, networks, and data from digital attacks.",
        },
        {
            "question": "What is a strong password?",
            "keywords": ["long", "unique", "letters", "numbers", "symbols"],
            "sample_answer": "A strong password is long, unique, and uses a mix of letters, numbers, and symbols.",
        },
        {
            "question": "What is an OTP?",
            "keywords": ["one", "time", "password", "verification", "login"],
            "sample_answer": "An OTP is a one-time password used for verification during login or transactions.",
        },
    ],
    "Data Scientist": [
        {
            "question": "What does a data scientist do?",
            "keywords": ["data", "analysis", "model", "insights", "prediction"],
            "sample_answer": "A data scientist analyzes data, builds models, finds insights, and helps make predictions or decisions.",
        },
        {
            "question": "What is a dataset?",
            "keywords": ["collection", "data", "rows", "columns", "records"],
            "sample_answer": "A dataset is a collection of data, usually organized in rows and columns for analysis or model building.",
        },
        {
            "question": "What is prediction?",
            "keywords": ["future", "estimate", "model", "data", "output"],
            "sample_answer": "Prediction means using data and a model to estimate an unknown or future value.",
        },
    ],
}

hard_questions = {
    "Data Analyst": [
        {
            "question": "How would you handle missing values in a dataset?",
            "keywords": ["missing values", "drop", "impute", "mean", "median"],
            "sample_answer": "Missing values can be handled by removing rows, imputing values using mean or median, or using domain knowledge depending on the data and problem.",
        },
        {
            "question": "Explain the difference between INNER JOIN and LEFT JOIN.",
            "keywords": ["inner join", "left join", "matching", "rows", "tables"],
            "sample_answer": "INNER JOIN returns only matching rows from both tables, while LEFT JOIN returns all rows from the left table and matching rows from the right table.",
        },
        {
            "question": "How do dashboards help business decision-making?",
            "keywords": ["dashboard", "metrics", "trends", "insights", "decisions"],
            "sample_answer": "Dashboards help by showing important metrics, trends, and insights in one place so teams can make faster data-driven decisions.",
        },
    ],
    "Software Developer": [
        {
            "question": "Explain polymorphism with an example.",
            "keywords": ["polymorphism", "same", "method", "different", "classes"],
            "sample_answer": "Polymorphism allows the same method name to behave differently for different classes, such as different objects having their own implementation of a speak method.",
        },
        {
            "question": "What is the difference between stack and heap memory?",
            "keywords": ["stack", "heap", "memory", "local", "dynamic"],
            "sample_answer": "Stack memory stores local variables and function calls, while heap memory is used for dynamically allocated objects.",
        },
        {
            "question": "What makes code maintainable?",
            "keywords": ["readable", "modular", "comments", "testing", "naming"],
            "sample_answer": "Maintainable code is readable, modular, well-named, tested, and organized so future changes are easier and safer.",
        },
    ],
    "AI/ML Engineer": [
        {
            "question": "How can overfitting be reduced?",
            "keywords": ["regularization", "cross validation", "dropout", "data", "simpler"],
            "sample_answer": "Overfitting can be reduced using more data, simpler models, regularization, cross-validation, dropout, or early stopping.",
        },
        {
            "question": "What is the bias-variance tradeoff?",
            "keywords": ["bias", "variance", "underfitting", "overfitting", "generalization"],
            "sample_answer": "The bias-variance tradeoff balances underfitting and overfitting. High bias causes underfitting, while high variance causes overfitting.",
        },
        {
            "question": "Why is train-test split important?",
            "keywords": ["train", "test", "generalization", "evaluate", "unseen"],
            "sample_answer": "Train-test split is important because it evaluates a model on unseen data and shows how well it generalizes.",
        },
    ],
    "HR Interview": [
        {
            "question": "Describe a time you failed and what you learned.",
            "keywords": ["failed", "learned", "improved", "example", "responsibility"],
            "sample_answer": "A strong answer explains a real failure, takes responsibility, describes what you learned, and shows how you improved afterward.",
        },
        {
            "question": "Where do you see yourself in five years?",
            "keywords": ["career", "skills", "growth", "learning", "contribute"],
            "sample_answer": "A good answer connects your future growth with learning, building skills, contributing to projects, and becoming stronger in your field.",
        },
        {
            "question": "How do you handle pressure or deadlines?",
            "keywords": ["pressure", "deadline", "prioritize", "plan", "calm"],
            "sample_answer": "Explain that you handle pressure by staying calm, prioritizing tasks, planning clearly, and communicating early if there are blockers.",
        },
    ],
    "Python Developer": [
        {
            "question": "What are decorators in Python?",
            "keywords": ["decorator", "function", "wrap", "modify", "behavior"],
            "sample_answer": "Decorators are functions that wrap another function to modify or extend its behavior without changing the original function code.",
        },
        {
            "question": "Explain list comprehension in Python.",
            "keywords": ["list comprehension", "loop", "condition", "concise", "list"],
            "sample_answer": "List comprehension is a concise way to create lists using an expression, loop, and optional condition in one line.",
        },
        {
            "question": "What is the difference between shallow copy and deep copy?",
            "keywords": ["shallow", "deep", "copy", "nested", "object"],
            "sample_answer": "A shallow copy copies the outer object but shares nested objects, while a deep copy creates independent copies of nested objects too.",
        },
    ],
    "Cyber Security Intern": [
        {
            "question": "What is the difference between encryption and hashing?",
            "keywords": ["encryption", "hashing", "reversible", "one-way", "data"],
            "sample_answer": "Encryption is reversible with a key, while hashing is one-way and commonly used to store passwords securely.",
        },
        {
            "question": "What is SQL injection?",
            "keywords": ["sql injection", "query", "input", "database", "attack"],
            "sample_answer": "SQL injection is an attack where malicious input is inserted into database queries to access or modify unauthorized data.",
        },
        {
            "question": "What is a firewall?",
            "keywords": ["firewall", "network", "traffic", "allow", "block"],
            "sample_answer": "A firewall monitors network traffic and allows or blocks traffic based on security rules.",
        },
    ],
    "Data Scientist": [
        {
            "question": "How do you handle imbalanced datasets?",
            "keywords": ["imbalanced", "resampling", "class weight", "precision", "recall"],
            "sample_answer": "Imbalanced datasets can be handled using resampling, class weights, suitable metrics like precision and recall, or collecting more minority-class data.",
        },
        {
            "question": "Explain precision and recall.",
            "keywords": ["precision", "recall", "positive", "false", "metric"],
            "sample_answer": "Precision measures how many predicted positives are correct, while recall measures how many actual positives were found by the model.",
        },
        {
            "question": "Why is feature scaling important?",
            "keywords": ["scaling", "features", "model", "distance", "gradient"],
            "sample_answer": "Feature scaling is important because some models are affected by feature magnitude, especially distance-based and gradient-based models.",
        },
    ],
}

question_sets = {
    "Easy": easy_questions,
    "Medium": questions,
    "Hard": hard_questions,
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
    attempt.setdefault("difficulty", "Medium")
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
    return render_template("index.html", roles=questions.keys(), difficulties=DIFFICULTIES)


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
    difficulty = request.form["difficulty"]
    role_questions = question_sets[difficulty][role]
    question_data = role_questions[0]
    session["current_attempt"] = {
        "id": str(uuid4()),
        "username": username,
        "role": role,
        "difficulty": difficulty,
        "answers": [],
    }

    return render_template(
        "interview.html",
        username=username,
        role=role,
        difficulty=difficulty,
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
    difficulty = request.form["difficulty"]
    question_index = int(request.form["question_index"])
    next_index = question_index + 1
    total_score = int(request.form["total_score"])
    role_questions = question_sets[difficulty][role]
    current_question = role_questions[question_index]
    result = evaluate_answer(answer, current_question["keywords"])
    score = result["score"]
    total_score += score
    current_attempt = session.get("current_attempt")

    if not current_attempt:
        current_attempt = {
            "id": str(uuid4()),
            "username": username,
            "role": role,
            "difficulty": difficulty,
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

    if next_index < len(role_questions):
        next_question = role_questions[next_index]

        return render_template(
            "interview.html",
            username=username,
            role=role,
            difficulty=difficulty,
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
