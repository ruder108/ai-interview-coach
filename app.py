from flask import Flask, render_template, request
app = Flask(__name__)
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/interview",methods=["POST"])
def interview():
    username= request.form["username"]
    role= request.form["role"]
    return f"Welcome {username}! you selected {role}"

if __name__ == "__main__":
    app.run(debug = True)