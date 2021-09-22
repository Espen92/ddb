import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from pathlib import Path
import json

def getColorId(commanders):
    colorsInId = []
    for c in commanders:
        r = requests.get('https://api.scryfall.com/cards/named?exact={}'.format(c)).json()
        colorsInId = r['color_identity'] + colorsInId
    wubrg = {
        "W": False,
        "U": False,
        "B": False,
        "R": False,
        "G": False,
    }
    for c in colorsInId:
        wubrg[c] = True
    colorstring = ''
    for c in wubrg:
        if wubrg[c]:
            colorstring = colorstring + c
    return colorstring

def getCommandersFromTitle(title):
    result = re.search(r'\((.*?)\)', title).group(1)
    return result.split('/')

def scrapeDeck(moxfieldId):
    URL = 'https://www.moxfield.com/decks/' + moxfieldId
    driver = webdriver.Chrome('/Applications/chromedriver')
    driver.get(URL)
    commanders = getCommandersFromTitle(driver.title)
    colorId = getColorId(commanders)

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "subheader-more"))
    )
    element.click()
    exportButton = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Export"))
    )
    exportButton.click()
    textField = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "mtga"))
    )
    decklistArray = textField.text.split('\n')
    deckObject = json.dumps({
        'decklist': decklistArray,
        'commanders': commanders,
        'URL': URL,
    })
    Path("../data/{}".format(colorId)).mkdir(parents=True, exist_ok=True)
    filename = "../data/{}/{}.json".format(colorId, moxfieldId)
    f = open(filename, "w")
    f.write(deckObject)
    f.close()
    driver.close()