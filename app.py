from flask import Flask, render_template, request
app = Flask(__name__)
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/interview",methods=["POST"])
def interview():
    username= request.form["username"]
    role= request.form["role"]
    if role == "Data Analyst":
        question = "What is Data Cleaning?"
    elif role == "Software Developer":
        question = "Explain OOP."
    elif role == "AI/ML Engineer":
        question = "What is supervised learning?"
        
    return render_template(
        "interview.html",
        username=username,
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

    return f"""
    <h1>Interview Feedback</h1>

    <p><strong>Name:</strong> {username}</p>

    <p><strong>Question:</strong> {question}</p>

    <p><strong>Your Answer:</strong> {answer}</p>

    <p><strong>Score:</strong> {score}/10</p>

    <p><strong>Feedback:</strong> {feedback_text}</p>
    """
if __name__ == "__main__":
    app.run(debug = True)