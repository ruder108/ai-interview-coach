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
if __name__ == "__main__":
    app.run(debug = True)