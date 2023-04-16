import csv
import datetime
import os
from os.path import isfile, join
import random
import re

class quizBuilder: 
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
                if spec in file and str(currentYear) in file:
                    break
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
            speccode = random.choice(self.species)
            image_ID = self.getRandomImageID(speccode)

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
                    while image_ID.startswith(" "):
                        image_ID = random.choice(data)[0]
                    return image_ID
