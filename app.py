from flask import Flask, render_template, request
app = Flask(__name__)
questions = {
    "Data Analyst": [
        "What is Data Cleaning?",
        "What is SQL?",
        "What is Data Visualization?"
    ],
    "Software Developer": [
        "Explain OOP.",
        "What is Inheritance?",
        "What is a Class?"
    ],
    "AI/ML Engineer":[
        "What is supervised learning?",
        "What is overfitting?",
        "What is a neural network?"
    ]
}
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/interview",methods=["POST"])
def interview():
    username= request.form["username"]
    role= request.form["role"]
    question = questions[role][0]
    return render_template(
        "interview.html",
        username=username,
        role=role,
        question=question)
@app.route("/feedback", methods=["POST"])
def feedback(): 
    username = request.form["username"]
    question = request.form["question"]
    answer = request.form["answer"]

    if len(answer) > 30:
        score = 8
        feedback_text = "Good answer. Try adding more details."
    else:
        score = 4
        feedback_text = "Answer is too short."

    return render_template(
        "feedback.html",
        username=username,
        question=question,
        answer=answer,
        score=score,
        feedback_text=feedback_text
    )
if __name__ == "__main__":
    app.run(debug = True)