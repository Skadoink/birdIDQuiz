from flask import Flask, redirect, render_template, request, url_for
from waitress import serve
from backend import Question, QuizBuilder

quiz = QuizBuilder(["snopet1"], 1)

app = Flask(__name__, static_folder='static')
app.config['STATIC_FOLDER'] = 'static'

# Define your routes and views here
@app.route("/")
def home():
    if request.method == "POST":
        species = request.form.get("species")
        num_questions = int(request.form.get("num_questions"))
        # Process the user input and start the quiz
        quiz = QuizBuilder(species, num_questions)
        return redirect(url_for('question'))
    return render_template("index.html")

@app.route('/question', methods=['GET', 'POST'])
def question():
    if request.method == 'POST':
        selected_option = request.form['option']
        current_question = quiz.get_current_question()

        is_correct = selected_option == current_question.correct_answer

        if not quiz.next_question():
            return redirect(url_for('quiz_end'))

        return render_template('answer.html', is_correct=is_correct, correct_answer=current_question.correct_answer)

    current_question = quiz.get_current_question()
    return render_template(
        'question.html',
        image_url=current_question.image_url,
        options=current_question.options
    )

@app.route('/quiz_end')
def quiz_end():
    return render_template('quiz_end.html')

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=8000)