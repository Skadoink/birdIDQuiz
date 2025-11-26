import os
import urllib.request
from bs4 import BeautifulSoup
import requests
import time

"""Goes through the NZ species page on ebird and gets the species code for each, then exports the images csv for each."""

def images_exist(spec):
    """Checks if the CSV for the species exists and has at least 1 image."""
    spec_csv = "species_CSVs/" + spec + ".csv"
    if os.path.exists(spec_csv):
        with open(spec_csv, "r", encoding="utf8") as f:
            if sum(1 for line in f) > 2: #will retry if there is only the header line and one date line
                return True
    return False

# get the species codes for each species
bird_list_url = "https://ebird.org/region/NZ/bird-list"
page = urllib.request.urlopen(bird_list_url)
soup = BeautifulSoup(page, "html.parser")
species_codes = []
for a in soup.find_all("a", href=True):
    if "/species/" in a["href"]:
        species_codes.append(a["href"].split("/")[-2])

# get the image URLs for each species
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
    "Cookie": ""
    } # replace with cookie from ebird - click "export" on the images page while logged in, then copy the cookie from the request headers in dev tools

for spec in species_codes:
    #first check if the species has already been exported to a CSV and has at least 2 images
    if images_exist(spec):
        print(f"{spec}.csv already exists and has images.")
        continue

    export_button_url = (
        "https://media.ebird.org/api/v2/export.csv?taxonCode="
        + spec
        + "&sort=rating_rank_desc&mediaType=photo&birdOnly=true&count=5000" #had some csv errors with 10000
    )
    response = requests.get(export_button_url, headers=headers)
    with open("species_CSVs/" + spec + ".csv", "wb") as f:
        f.write(response.content)

    print(f"Exported {spec}.csv")
    if not images_exist(spec):
        print(f"No images found for {spec}.")
    
    time.sleep(2) # to avoid rate limiting 
    

print("Done!")
