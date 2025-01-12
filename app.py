from flask import Flask, redirect, render_template, request, url_for, session
from flask_session import Session
from waitress import serve
from backend import Question, QuizBuilder

app = Flask(__name__, static_folder="static")
app.config["STATIC_FOLDER"] = "static"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# session["quiz"] = QuizBuilder(["Snow Petrel"], 1) #outside request context

# Define your routes and views here
@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def home():
    # global quiz # disabled as now quiz is stored in session
    
    if request.method == "POST" and request.form.get("submitButton"):
        selected_species = request.form.get("selectedSpecies")
        num_questions = int(request.form.get("num_questions"))
        # Convert the string to a list
        selected_species = selected_species.split(",")
        # Process the user input and start the quiz
        quiz = QuizBuilder(selected_species, num_questions)
        # store the quiz in the session
        session["quiz"] = quiz
        return redirect(url_for("question"))
    
    return render_template("index.html")


@app.route("/question", methods=["GET", "POST"])
def question():
    if request.method == "POST":
        selected_option = request.form["option"]
        current_question = session["quiz"].get_current_question()

        is_correct = selected_option == current_question.speccode
        if is_correct:
            session["quiz"].correct_answers += 1
            session.modified = True

        session["quiz"].next_question()
        session.modified = True

        return render_template(
            "answer.html",
            current_question_index=session["quiz"].current_question_index,
            num_questions=session["quiz"].num_questions,
            is_correct=is_correct,
            correct_answer=current_question.spec_name,
            embed_url=current_question.embed_URL,
        )

    current_question = session["quiz"].get_current_question()
    return render_template(
        "question.html",
        current_question_index=session["quiz"].current_question_index + 1,
        num_questions=session["quiz"].num_questions,
        image_url=current_question.image_URL,
        options=current_question.species_options,
    )


@app.route("/answer", methods=["GET", "POST"])
def answer():
    if request.method == "POST" and request.form.get("endButton") != None:
        return render_template(
            "quiz_end.html",
            correct_answers=session["quiz"].correct_answers,
            num_questions=session["quiz"].num_questions,
        )
    return redirect(url_for("home"))


@app.route("/quiz_end")
def quiz_end():
    return render_template("quiz_end.html")


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)
