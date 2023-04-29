import urllib.request
from bs4 import BeautifulSoup

html_page = urllib.request.urlopen("https://media.ebird.org/catalog?taxonCode=magpet1&sort=rating_rank_desc&mediaType=photo&view=list")
soup = BeautifulSoup(html_page, "html.parser")
images = []
for img in soup.findAll('img'):
    print(img.get('src'))

print(images)