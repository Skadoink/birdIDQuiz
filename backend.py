import csv
import datetime
import os
from os.path import isfile, join
import random
import urllib.request
from bs4 import BeautifulSoup

class Question:
    def __init__(self, speccode, image_ID, species_options):
        self.speccode = speccode
        self.image_ID = image_ID
        self.species_options = species_options

class QuizBuilder: 
    def __init__(self, species, num_questions):
        self.species = species
        self.num_questions = num_questions
        self.questions = []
        self.given_answers = []
        self.correct_answers = []
        self.check_CSVs()
        self.create_questions()

    def check_CSVs(self):
        currentYearMonth = datetime.datetime.now().strftime("%Y-%m")
        speciesPath = "species_CSVs"
        onlyfiles = [f for f in os.listdir(speciesPath) if isfile(join(speciesPath, f)) and f.endswith('.csv')]
        for spec in self.species:
            for i, file in enumerate(onlyfiles):
                #correct species and up to date
                if spec in file and str(currentYearMonth) in file:
                    break
                #correct species but not up to date
                elif spec in file and str(currentYearMonth) not in file:
                    self.updateCSV(spec)
                    os.remove(join(speciesPath, file))
                #if we've reached the end of the list and haven't found a match
                elif i == len(onlyfiles) - 1: 
                    self.updateCSV(spec) 
                
    def updateCSV(self, spec):
        """
        Gets the latest image IDs from the species' media page on eBird and saves it to a CSV file.
        """    
        html_page = urllib.request.urlopen("https://media.ebird.org/catalog?taxonCode=magpet1&sort=rating_rank_desc&mediaType=photo&view=list")
        soup = BeautifulSoup(html_page, "html.parser")
        images = []
        for img in soup.findAll('img'):
            src = img.get('src')
            if src.startswith("https://cdn.download.ams.birds.cornell.edu/api/v1/asset/"):
                images.append(src)

    def create_questions(self):
        for i in range(self.num_questions):
            num_options = min(len(self.species), 4)
            species_options = random.sample(self.species, num_options)
            speccode = random.choice(species_options)
            image_ID = self.getRandomImageID(speccode)
            question = Question(speccode, image_ID, species_options)
            self.questions.append(question)

    def getRandomImageID(self, speccode):
        """
        Gets a random image ID from the CSV file for the given species.
        """
        for file in os.listdir("species_CSVs"):
            if speccode in file:
                with open(join("species_CSVs", file), 'r') as f:
                    reader = csv.reader(f)
                    data = list(reader)
                    image_ID = random.choice(data)[0]
                    while image_ID.startswith(" "): #if the image ID is caused by a newline in the csv, it will start with a space
                        image_ID = random.choice(data)[0]
                    return image_ID
