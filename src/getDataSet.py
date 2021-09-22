from scrapeAmoxfielddeck import scrapeDeck
from scrapeURLS import getMoxfieldIdsFromDb



if __name__ == "__main__":
    decklistIds = getMoxfieldIdsFromDb("https://cedh-decklist-database.com/")
    for l in decklistIds:
        scrapeDeck(l)