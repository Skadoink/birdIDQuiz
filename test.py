import requests

url = "https://media.ebird.org/api/v2/export.csv?taxonCode=magpet1&sort=rating_rank_desc&mediaType=photo&birdOnly=true&count=10000"
session = requests.Session()
headers ={"cookie": ""}

r = session.get(url, 
                 headers=headers)

print(r.content)
open('testdl.csv', 'wb').write(r.content)