from flask import Flask, redirect, render_template, request, url_for, session
from waitress import serve
from backend import Question, QuizBuilder
import backend

app = Flask(__name__, static_folder="static", instance_relative_config=True)
app.config["STATIC_FOLDER"] = "static"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config.from_pyfile("config.py")


# Define your routes and views here
@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "POST" and request.form.get("submitButton"):
        if request.form.get("selectedSpeciesInput") == "":
            return render_template(
                "index.html", selected_species=""
            )
        session["selected_species"] = request.form.get(
            "selectedSpeciesInput"
        )  # comma separated string
        num_questions = int(request.form.get("num_questions"))
        # Process the user input and start the quiz
        quiz = QuizBuilder(session["selected_species"].split(","), num_questions)
        # store the quiz in the session
        session["quiz"] = quiz.to_dict()
        return redirect(url_for("question"))

    return render_template(
        "index.html",
        all_species = ",".join(backend.species_names_to_codes.keys()),
        selected_species=session.get("selected_species", ""),
        quiz_templates=backend.QUIZ_TEMPLATES,
        species_codes_to_names=backend.species_codes_to_names,
        seabird_templates = backend.SEABIRDS,
        seabird_adv_templates = backend.SEABIRDS_ADVANCED,
        shorebird_templates = backend.SHOREBIRDS,
        shorebird_adv_templates = backend.SHOREBIRDS_ADVANCED,
    )


@app.route("/question", methods=["GET", "POST"])
def question():
    """
    Handles navigation to the current quiz question.
    If a POST request is received, it redirects to the /answer route using a 307 redirect.
    The 307 status code is used to preserve the original POST method and body, which is essential for answer submission
    because it ensures that form data is not lost during the redirect and the user's answer can be processed correctly.
    """
    if request.method == "POST":
        # Prevent direct POST requests to /question, handle via /answer instead
        return redirect(url_for("answer"), code=307) # 307 uses POST to redirect, so we can identify the request as an answer submission

    # Guard: redirect to home if quiz is not in session
    if "quiz" not in session:
        return redirect(url_for("home"))

    # GET request indicates legitimate navigation to the question page
    current_question = QuizBuilder.from_dict(session["quiz"]).get_current_question()
    return render_template(
        "question.html",
        current_question_index=session["quiz"]["current_question_index"],
        num_questions=session["quiz"]["num_questions"],
        image_url=current_question.image_URL,
        options=current_question.species_options,
    )


@app.route("/answer", methods=["GET", "POST"])
def answer():
    # Guard: redirect to home if quiz is not in session
    if "quiz" not in session:
        return redirect(url_for("home"))
    
    quiz = QuizBuilder.from_dict(session["quiz"])

    # Prevent direct GET requests to /answer
    if request.method != "POST":
        if quiz.current_question_index >= quiz.num_questions:
            return redirect(url_for("quiz_end"))
        return redirect(url_for("question"))

    # If it's the last question and they clicked End
    if request.form.get("endButton") is not None:
        return redirect(url_for("quiz_end"))
    
     # Read the question index the user submitted from the hidden form input
    try:
        form_index = int(request.form.get("question_index"))
    except (TypeError, ValueError):
        return redirect(url_for("question"))

    # If it's not already answered, evaluate and store
    if form_index == quiz.current_question_index and str(form_index) not in quiz.answered_questions:
        selected_option = request.form.get("option")
        current_question = quiz.get_current_question()
        is_correct = selected_option == current_question.speccode
        quiz.answered_questions[str(form_index)] = is_correct
        session["is_correct"] = is_correct
        quiz.next_question()
    else:
        # Prevent duplicate answers or skipped state
        # Just retrieve the previous answer state
        session["is_correct"] = quiz.answered_questions.get(str(form_index), False) #TODO: could use None to indicate not answered, and handle in template

    # Save the updated quiz state
    session["quiz"] = quiz.to_dict()
    session.modified = True

    return render_template(
        "answer.html",
        current_question_index=form_index + 1,
        num_questions=quiz.num_questions,
        is_correct=session["is_correct"],
        correct_answer=quiz.questions[form_index].spec_name,
        embed_url=quiz.questions[form_index].embed_URL,
    )



@app.route("/quiz_end", methods=["GET", "POST"])
def quiz_end():
    # Guard: redirect to home if quiz is not in session
    if "quiz" not in session:
        return redirect(url_for("home"))
    
    # Handle End button to go back to home
    if request.method == "GET" and request.form.get("endButton") != None:
        return redirect(url_for("home"))
    
    # Load end of quiz page
    quiz = QuizBuilder.from_dict(session["quiz"])
    return render_template(
        "quiz_end.html",
        num_correct_answers=list(quiz.answered_questions.values()).count(True),
        num_questions=quiz.num_questions,
        incorrect_questions=[quiz.questions[int(q)] for q in quiz.answered_questions.keys() if quiz.answered_questions[q] == False],
        correct_questions=[quiz.questions[int(q)] for q in quiz.answered_questions.keys() if quiz.answered_questions[q] == True],
    )


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)
