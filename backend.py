import csv
import datetime
import os
from os.path import isfile, join
import random
import re

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
        currentYear = datetime.datetime.now().year
        mypath = "species_CSVs"
        onlyfiles = [f for f in os.listdir(mypath) if isfile(join(mypath, f)) and f.endswith('.csv')]
        for spec in self.species:
            for i in range(len(onlyfiles)):
                file = onlyfiles[i]
                #correct species and up to date
                if spec in file and str(currentYear) in file:
                    break
                #correct species but not up to date
                elif spec in file and str(currentYear) not in file:
                    updateSuccess = self.updateCSV(spec)
                    if updateSuccess:
                        os.remove(join(mypath, file))
                    break
                elif i == len(onlyfiles) - 1: #if we've reached the end of the list and haven't found a match
                    self.updateCSV(spec) 
                
    def updateCSV(self, spec):
        """
        Gets the latest images CSV from exporting from the media page of the species.
        Should effectively click the export button on a page like 
        https://media.ebird.org/catalog?taxonCode=magpet1&sort=rating_rank_desc&mediaType=photo
        and save the file to the species_CSVs folder.
        """    
        return True

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
