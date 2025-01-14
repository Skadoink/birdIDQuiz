import csv
import datetime
import os
from os.path import isfile, join
import random
import urllib.request
from bs4 import BeautifulSoup


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
        # embed_URL = '<iframe src="https://macaulaylibrary.org/asset/'+image_ID+'/embed" height="507" width="640" frameborder="0" allowfullscreen></iframe>'
        return embed_URL

    def get_spec_name(speccode, species_options):
        return [
            d["species_name"] for d in species_options if d["species_code"] == speccode
        ][
            0
        ]  # get the name of the species with the correct code


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
        self.correct_questions = []
        self.incorrect_questions = []
        self.num_correct_answers = 0
        self.species, self.species_codes = self.find_spec_codes()
        self.no_image_species = []
        self.current_question_index = 0
        self.check_CSVs()
        if self.no_image_species:
            return
        self.create_questions()

    def find_spec_codes(self):
        """
        Makes a dictionary of species codes and names.
        """
        species_csv = csv.reader(open("static/species2024.csv", "r"))
        species_codes = []  # list of species codes
        species = []  # list of dictionaries with species code and common name
        for row in species_csv:
            if row[1] in self.species_names:
                species_codes.append(row[0])
                species.append({"species_code": row[0], "species_name": row[1]})
            if len(self.species_names) == len(species):
                break
        return species, species_codes

    def check_CSVs(self):
        """
        Checks if the CSV files for the species are up to date. If not, updates them.
        """
        currentYearMonth = datetime.datetime.now().strftime("%Y-%m")
        species_path = "species_CSVs"
        if not os.path.exists(species_path):
            os.makedirs(species_path)
        onlyfiles = [
            f
            for f in os.listdir(species_path)
            if isfile(join(species_path, f)) and f.endswith(".csv")
        ]
        for spec in self.species_codes:
            if len(onlyfiles) == 0:
                self.updateCSV(spec)
            for i, file in enumerate(onlyfiles):
                # correct species and up to date
                if spec in file and str(currentYearMonth) in file:
                    break
                # correct species but not up to date
                elif spec in file and str(currentYearMonth) not in file:
                    self.updateCSV(spec)
                    os.remove(
                        join(species_path, file)
                    )  # TODO should only do this if the update is successful
                # if we've reached the end of the list and haven't found a match
                elif i == len(onlyfiles) - 1:
                    self.updateCSV(spec)

    def updateCSV(self, spec):
        """
        Gets the latest image URLs from the species' media page on eBird and saves it to a CSV file.
        @param spec: species code
        """
        url = (
            "https://media.ebird.org/catalog?taxonCode="
            + spec
            + "&sort=rating_rank_desc&mediaType=photo&view=list"
        )
        html_page = urllib.request.urlopen(url)
        soup = BeautifulSoup(html_page, "html.parser")
        images = []
        for img in soup.findAll("img"):
            src = img.get("src")
            if src.startswith(
                "https://cdn.download.ams.birds.cornell.edu/api/v2/asset/"
            ):
                images.append(src)
        if len(images) == 0:
            self.no_image_species.append(Question.get_spec_name(spec, self.species))
            return
        with open(
            join(
                "species_CSVs",
                spec + "_" + datetime.datetime.now().strftime("%Y-%m") + ".csv",
            ),
            "w",
            newline="",
        ) as f:
            writer = csv.writer(f)
            for image in images:
                writer.writerow([image])

    def create_questions(self):
        """
        Creates the questions for the quiz.
        """
        for _ in range(self.num_questions):
            num_options = min(len(self.species), 4)
            species_options = random.sample(self.species, num_options)
            species_options = sorted(species_options, key=lambda x: x["species_name"])
            speccode = random.choice(species_options)["species_code"]
            specImageURL = self.getRandomimageURL(speccode)
            question = Question(speccode, specImageURL, species_options)
            self.questions.append(question)

    def getRandomimageURL(self, speccode):
        """
        Gets a random image ID from the CSV file for the given species.
        @param speccode: species code
        """
        for file in os.listdir("species_CSVs"):
            print(file, speccode)
            if speccode in file:
                with open(join("species_CSVs", file), "r") as f:
                    reader = csv.reader(f)
                    data = list(reader)
                    if len(data) == 0:
                        return None
                    imageURL = random.choice(data)[0]
                    return imageURL

    def get_current_question(self):
        return self.questions[self.current_question_index]

    def next_question(self):
        self.current_question_index += 1
        return self.current_question_index < len(self.questions)
