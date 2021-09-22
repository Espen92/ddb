import requests
from bs4 import BeautifulSoup

URL = "https://cedh-decklist-database.com/"


def getMoxfieldIdsFromDb(dbUrl):
    r = requests.get(dbUrl)
    soup = BeautifulSoup(r.content, "html.parser")
    listOfMoxfieldUrls = []
    for a in soup.find_all('a', href=True):
        link = a['href']
        if 'https://www.moxfield.com' in link:
            listOfMoxfieldUrls.append(link)
    print(listOfMoxfieldUrls)
    return map(lambda l: l.replace('https://www.moxfield.com/decks/', ''), listOfMoxfieldUrls)

print(getMoxfieldIdsFromDb(URL))
