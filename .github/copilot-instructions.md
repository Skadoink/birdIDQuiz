This repository is a small Flask web app (birdIDQuiz) that builds image-based multiple-choice quizzes from exported eBird CSVs.

Key points for an AI coding agent working in this repo
- Big picture
  - app.py is the Flask entrypoint. It renders templates under `templates/` and serves static CSS from `static/`.
  - `backend.py` contains the quiz domain model: `Question` and `QuizBuilder`. `QuizBuilder.build_species_dicts()` reads CSV files under `nz_species_CSVs_202501` to map species codes <-> names.
  - `nz_species_csv.py` is a helper script used to download/export eBird media CSVs. It is not used at runtime by the Flask app but explains how the CSVs were generated.

- Runtime / developer workflows
  - Run the app locally: the code uses `waitress.serve(app, host='0.0.0.0', port=8000)` in `app.py`. Use a Python venv and install `requirements.txt`, then run `python app.py`.
  - Tailwind: source file is `static/styles/style.css` and the built output is `static/styles/out.css`. `build-tailwind.sh` shows the command: `npx tailwindcss -i ./static/styles/style.css -o ./static/styles/out.css --watch`.
  - Session config lives in `instance/config.py` (contains SECRET_KEY and ebird_session placeholder). The Flask app loads it with `app.config.from_pyfile('config.py')`.

- Data shapes and conventions (important for edits)
  - Quiz state stored in Flask session as `session['quiz']` and is a dict produced by `QuizBuilder.to_dict()`. Key fields:
    - `species_names` (list of common names), `num_questions` (int)
    - `questions`: list of question dicts from `Question.to_dict()` with keys `speccode`, `image_URL`, `species_options`, `spec_name`, `embed_URL`
    - `correct_questions`, `incorrect_questions` (lists of question dicts)
    - `num_correct_answers`, `current_question_index` (ints)
  - `species_options` is a list of {"species_code": str, "species_name": str} used to render radio options in templates (`templates/question.html`).
  - CSVs: each file in `nz_species_CSVs_202501` is named `<speccode>.csv` and the first column of rows is an image asset ID (used to build Cornell CDN URLs). `build_species_dicts()` reads the 3rd column (index 2) for the common name.

- Patterns & gotchas (copy exactly when changing behavior)
  - `QuizBuilder.build_species_dicts()` reads only the first data row from each CSV to map code->name. Don't change that without checking the CSV format.
  - `Question.get_embed_URL()` expects the `image_URL` to have the asset id in the penultimate path segment to produce a Macaulay embed URL.
  - Session storage serializes plain dicts/lists (not objects). Use `to_dict()`/`from_dict()` helpers when converting.
  - `app.question()` uses a 307 redirect to `answer` so that the POST body is preserved. Preserve this behavior if refactoring answer flow.

- Files to inspect when modifying behavior
  - `app.py` — routing, session usage, rendering flow
  - `backend.py` — all quiz generation logic and CSV parsing
  - `templates/*.html` — input names and expected session/quiz shapes (`question.html`, `answer.html`, `index.html`, `quiz_end.html`)
  - `nz_species_csv.py` — CSV export/download script (useful for updating CSVs)
  - `instance/config.py` — secret and any environment keys

- Quick examples
  - To render options the templates expect option dicts with keys `species_code` and `species_name` (see `question.html`).
  - To persist updated quiz state after evaluating an answer, call `session['quiz'] = quiz.to_dict()` and set `session.modified = True`.

If anything here is unclear or you want the file to include more examples (e.g., exact session JSON example, test commands, or contribution rules), tell me which sections to expand and I will iterate.
