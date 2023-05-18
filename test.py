# import backend

# testBE = backend.QuizBuilder(['magpet1', 'snopet1', 'nezkak1', 'kea1', 'gagcoc1', 'shoebi1'], 5)
# print([(q.imageURL, q.speccode, q.species_options) for q in testBE.questions])


#make dict from ebirdtaxonomy csv with common name as key and species code as value
import csv
import os
from os.path import isfile, join
import urllib.request
from bs4 import BeautifulSoup

def make_species():
    """
    Makes a dictionary from the eBird taxonomy CSV file with common name as key 
    and species code as value.
    Also saves a CSV file with the common names and species codes.
    @return: dictionary with common name as key and species code as value
    """
    if not os.path.exists("species_CSVs"):
        os.makedirs("species_CSVs")
    with open('ebird_taxonomy_v2022.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)
        names_codes = {}
        with open("species.csv", "w", newline='') as f:
            w = csv.writer(f)    
            for row in reader:
                if row[1] == "species": #to exclude other taxonomic levels
                    w.writerow([row[2], row[3]]) #common name, species code
                    names_codes[row[3]] = row[2] #common name is key, species code is value
    return names_codes

def get_species_codes(species):
    """
    Gets the species codes for the given species.
    @param species: list of species names
    @return: list of species codes
    """
    names_codes = make_species()
    species_codes = []
    for spec in species:
        species_codes.append(names_codes[spec])
    return species_codes

codes = get_species_codes(["Gray-hooded Warbler"])
print(codes)