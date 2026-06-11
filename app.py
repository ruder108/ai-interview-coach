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
        question=question,
        question_index=0,
        total_score=0
        )
    
@app.route("/feedback", methods=["POST"])
def feedback(): 
    username = request.form["username"]
    question = request.form["question"]
    answer = request.form["answer"]
    role = request.form["role"]
    question_index = int(request.form["question_index"])
    next_index = question_index + 1
    print(request.form)
    total_score= int(request.form["total_score"])
    if len(answer) > 30:
        score = 8
    else:
        score = 4

    total_score += score
    
    if next_index < len(questions[role]):
        next_question = questions[role][next_index] 
    
        return render_template(
            "interview.html",
            username=username,
            role=role,
            question=next_question,
            question_index=next_index,
            total_score=total_score
            )
    if total_score >= 20:
        performance = "excelent"
    elif total_score >= 12:
        performance = "Good"
    else:
        performance = "Needs Improvement"
          
    return render_template(
        "feedback.html",
        username=username, 
        question=question, 
        answer=answer, 
        score=total_score,
        performance=performance,
        feedback_text="Interview Completed!"
        )    

if __name__ == "__main__":
    app.run(debug = True)