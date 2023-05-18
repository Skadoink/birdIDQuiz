from flask import Flask, render_template, request

app = Flask(__name__, static_folder='static')
app.config['STATIC_FOLDER'] = 'static'

# Define your routes and views here
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        species = request.form.get("species")
        num_questions = int(request.form.get("num_questions"))
        # Process the user input and start the quiz
        return "Quiz started!"
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
