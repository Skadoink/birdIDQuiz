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
                "index.html", no_image_species=[], selected_species=""
            )
        session["selected_species"] = request.form.get(
            "selectedSpeciesInput"
        )  # comma separated string
        num_questions = int(request.form.get("num_questions"))
        # Process the user input and start the quiz
        quiz = QuizBuilder(session["selected_species"].split(","), num_questions)
        if quiz.no_image_species: # redundant when we know all our CSVs have images, but might be useful again in the future
            for species in quiz.no_image_species:
                session["selected_species"] = session["selected_species"].replace(
                    species + ",", ""
                )
                session["selected_species"] = session["selected_species"].replace(
                    "," + species, ""
                )  # in case it's the last species
            return render_template(
                "index.html",
                no_image_species=quiz.no_image_species,
                selected_species=session.get("selected_species", ""),
            )
        # store the quiz in the session
        session["quiz"] = quiz.to_dict()
        return redirect(url_for("question"))

    return render_template(
        "index.html",
        all_species = ",".join(backend.species_names_to_codes.keys()),
        no_image_species=[],
        selected_species=session.get("selected_species", ""),
    )


@app.route("/question", methods=["GET", "POST"])
def question():
    current_question = QuizBuilder.from_dict(session["quiz"]).get_current_question()

    if request.method == "POST":
        #TODO: Only increment if the question hasn't been answered yet
        selected_option = request.form["option"]
        is_correct = selected_option == current_question.speccode
        session["is_correct"] = is_correct
        if is_correct:
            session["quiz"]["num_correct_answers"] += 1
            session["quiz"]["correct_questions"].append(current_question.to_dict())
        else:
            session["quiz"]["incorrect_questions"].append(current_question.to_dict())

        return redirect(url_for("answer"), code=307) # 307 uses POST to redirect, so we can identify the request as an answer submission

    return render_template(
        "question.html",
        current_question_index=session["quiz"]["current_question_index"],
        num_questions=session["quiz"]["num_questions"],
        image_url=current_question.image_URL,
        options=current_question.species_options,
    )


@app.route("/answer", methods=["GET", "POST"])
def answer():
    quiz = QuizBuilder.from_dict(session["quiz"])

    # Prevent direct GET requests to /answer
    if request.method != "POST":
        if quiz.current_question_index + 1 >= quiz.num_questions:
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
    if form_index == quiz.current_question_index and form_index not in quiz.answered_questions:
        selected_option = request.form.get("option")
        current_question = quiz.get_current_question()
        is_correct = selected_option == current_question.speccode
        quiz.answered_questions[form_index] = is_correct
        session["is_correct"] = is_correct
        quiz.next_question()
    else:
        # Prevent duplicate answers or skipped state
        session["is_correct"] = quiz.answered_questions.get(form_index, False)

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
    if request.method == "GET" and request.form.get("endButton") != None:
        return redirect(url_for("home"))
    quiz = QuizBuilder.from_dict(session["quiz"])
    return render_template(
        "quiz_end.html",
        num_correct_answers=quiz.num_correct_answers,
        num_questions=quiz.num_questions,
        incorrect_questions=quiz.incorrect_questions,
        correct_questions=quiz.correct_questions,
    )


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)
