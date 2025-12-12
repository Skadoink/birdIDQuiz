import csv
import datetime
import os
from os.path import isfile, join
import random
import urllib.request
from bs4 import BeautifulSoup
from pathlib import Path
import json

class Question:
    def __init__(self, speccode, image_URL, species_options):
        """
        Creates a question with the given species code, image ID, and species options.
        @param speccode: species code of the correct answer
        @param image_ID: image URL of the correct answer
        @param species_options: list of dicts of species codes and names for the options
        """
        self.speccode = speccode
        self.image_URL = image_URL
        self.species_options = species_options
        self.spec_name = Question.get_spec_name(speccode, species_options)  # get the common name of the species
        self.embed_URL = self.get_embed_URL(image_URL)

    def get_embed_URL(self, image_URL):
        """
        Gets the embed URL for the image.
        @param image_URL: URL of the image
        """
        image_ID = image_URL.split("/")[-2]
        embed_URL = "https://macaulaylibrary.org/asset/" + image_ID + "/embed"
        return embed_URL

    def get_spec_name(speccode, species_options):
        return [
            d["species_name"] for d in species_options if d["species_code"] == speccode
        ][
            0
        ]  # get the name of the species with the correct code

    def to_dict(self):
        return {
            "speccode": self.speccode,
            "image_URL": self.image_URL,
            "species_options": self.species_options,
            "spec_name": self.spec_name,
            "embed_URL": self.embed_URL,
        }
        
    def from_dict(d):
        return Question(d["speccode"], d["image_URL"], d["species_options"])

class QuizBuilder:
    def __init__(self, species_names, num_questions):
        """
        Makes a quiz with the given species and number of questions.
        @param species: list of species names
        @param num_questions: number of questions in the quiz
        """
        self.species_names = species_names
        self.num_questions = num_questions
        self.questions = [] 
        self.answered_questions = {}
        self.num_correct_answers = 0
        self.current_question_index = 0
        self.quiz_species_codes_to_names = self.find_spec_codes()
        self.create_questions()

    def build_species_dicts():
        """
        Makes a dictionary of species codes and names.
        Skips column labels (first row). 
        Species name is the 3rd column.row[19]
        """
        species_codes_to_names = {}
        species_names_to_codes = {}
        THIS_FOLDER = Path(__file__).parent.resolve()
        CSV_FOLDER = THIS_FOLDER / "nz_species_CSVs_202511"
        for file in os.listdir(CSV_FOLDER):
            with open(join(CSV_FOLDER, file), "r", encoding="utf8") as f:
                reader = csv.reader(f)
                next(reader)  # skip the first row
                for row in reader:
                    species_code = file.split(".")[0]
                    species_name = row[2].split(" (")[0] # remove the subspecies if present
                    species_codes_to_names[species_code] = species_name
                    species_names_to_codes[species_name] = species_code
                    break
        return species_codes_to_names, species_names_to_codes

    def find_spec_codes(self):
        """
        Makes a list of dictionaries of quiz's species codes to species names.
        """
        quiz_species_codes_to_names = []
        for species_name in self.species_names:
            quiz_species_codes_to_names.append(
                {
                    "species_code": species_names_to_codes[species_name],
                    "species_name": species_name,
                }
            )
        return quiz_species_codes_to_names

    def create_questions(self):
        """
        Creates the questions for the quiz.
        """
        for _ in range(self.num_questions):
            num_options = min(len(self.quiz_species_codes_to_names), 4)
            species_options = random.sample(list(self.quiz_species_codes_to_names), num_options)
            species_options = sorted(species_options, key=lambda x: x["species_name"]) # sort by species name
            speccode = random.choice(species_options)["species_code"]
            specImageURL = self.getRandomimageURL(speccode)
            question = Question(speccode, specImageURL, species_options)
            self.questions.append(question)

    def getRandomimageURL(self, speccode):
        """
        Gets a random image ID from the CSV file for the given species.
        @param speccode: species code
        """
        THIS_FOLDER = Path(__file__).parent.resolve()
        CSV_FOLDER = THIS_FOLDER / "nz_species_CSVs_202511"
        for file in os.listdir(CSV_FOLDER):
            if speccode == file.split(".")[0]:
                with open(join(CSV_FOLDER, file), "r", encoding="utf8") as f:
                    reader = csv.reader(f)
                    data = list(reader)[1:]
                    if len(data) == 0:
                        return None
                    imageID = random.choice(data)[0]
                    imageURL = "https://cdn.download.ams.birds.cornell.edu/api/v2/asset/" + imageID + "/1200"
                    return imageURL

    def get_current_question(self):
        return self.questions[self.current_question_index]

    def next_question(self):
        self.current_question_index += 1
        return self.current_question_index < len(self.questions)

    def to_dict(self):
        return {
            "species_names": self.species_names,
            "num_questions": self.num_questions,
            "questions": [q.to_dict() for q in self.questions],
            "answered_questions": self.answered_questions,
            "num_correct_answers": self.num_correct_answers,
            "current_question_index": self.current_question_index,
        }
        
    def from_dict(d):
        quiz = QuizBuilder(d["species_names"], d["num_questions"])
        quiz.questions = [Question.from_dict(q) for q in d["questions"]]
        # Restore answered_questions if present so answered state persists
        quiz.answered_questions = d.get("answered_questions", {})
        quiz.num_correct_answers = d["num_correct_answers"]
        quiz.current_question_index = d["current_question_index"]
        return quiz
    
    
# Template quizzes for quick access
# Format: { "id": str, "title": str, "subtitle": str, "section": str, "species": [str], "image_url": str }
def load_quiz_templates():
    """Load quiz templates from JSON file."""
    THIS_FOLDER = Path(__file__).parent.resolve()
    TEMPLATES_FILE = THIS_FOLDER / "quiz_templates.json"
    try:
        with open(TEMPLATES_FILE, "r", encoding="utf8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

QUIZ_TEMPLATES = load_quiz_templates()
SEABIRDS = [template for template in QUIZ_TEMPLATES if template.get("section") == "seabirds"]
SEABIRDS_ADVANCED = [template for template in QUIZ_TEMPLATES if template.get("section") == "seabirds-advanced"]
SHOREBIRDS = [template for template in QUIZ_TEMPLATES if template.get("section") == "shorebirds"]
SHOREBIRDS_ADVANCED = [template for template in QUIZ_TEMPLATES if template.get("section") == "shorebirds-advanced"]

#dictionary of species codes and names
species_codes_to_names, species_names_to_codes = QuizBuilder.build_species_dicts()