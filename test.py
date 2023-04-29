# import backend

# testBE = backend.QuizBuilder(['magpet1', 'snopet1', 'nezkak1', 'kea1', 'gagcoc1', 'shoebi1'], 5)
# print([(q.imageURL, q.speccode, q.species_options) for q in testBE.questions])


#make dict from ebirdtaxonomy csv with common name as key and species code as value
import csv
import os
from os.path import isfile, join
import urllib.request
from bs4 import BeautifulSoup

def make_dict():
    """
    Makes a dictionary from the eBird taxonomy CSV file with common name as key and species code as value.
    @return: dictionary with common name as key and species code as value
    """
    with open('ebird_taxonomy_v2022.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)
        dict = {}
        for row in reader:
            if row[1] == "species":
                dict[row[3]] = row[2]
    return dict

def get_species_codes(species):
    """
    Gets the species codes for the given species.
    @param species: list of species names
    @return: list of species codes
    """
    dict = make_dict()
    species_codes = []
    for spec in species:
        species_codes.append(dict[spec])
    return species_codes

codes = get_species_codes(["Gray-hooded Warbler"])
print(codes)