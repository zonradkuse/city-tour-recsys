import requests
import sys
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def wordcount(node):
    session = requests.Session()

    URL = "https://en.wikipedia.org/w/api.php"

    parameters = {
        'action':"query",
        'list':"search",
        'srsearch': node,
        'format':"json"
    }

    response = session.get(url=URL, params=parameters)
    DATA = response.json()

    if DATA['query']['searchinfo']['totalhits'] == 0:
        print("No data for the given node")
        return


    if similar(DATA['query']['search'][0]['title'].lower(),node.lower())>=0.6:
        return DATA['query']['search'][0]['wordcount']


if __name__ == '__main__':
    args = sys.argv[1:]
    search_word = ""
    for items in args:
        search_word = search_word + str(items) + " "
    search_word=search_word[:-1]
    num_of_results = wordcount(search_word)
    print "Wiki - Wordcount: ", num_of_results
