import requests
import sys
import json
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def pageviews(node):

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
        print("No results for the query")
        return

    title = DATA['query']['search'][0]['title']
    print("Found: "+title)

    if similar(title.lower(),node.lower())>=0.3:
        r = requests.get("https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/de.wikipedia/all-access/all-agents/"+title+"/monthly/2001010100/2017123100")

        string = r.content.decode('utf-8')
        json_obj = json.loads(string)


        if ('title' in json_obj):
            if(json_obj['title'] == "Not found."):
                print("No pageviews data for given node")
                return

        if ('items' in json_obj):
            number_of_views = 0
            for item in json_obj['items']:
                views_per_item = item['views']

                number_of_views = number_of_views + views_per_item

            return number_of_views
        return

if __name__ == '__main__':
    args = sys.argv[1:]
    search_word = ""
    for items in args:
        search_word = search_word + str(items) + "_"
    search_word=search_word[:-1]
    number_of_views = pageviews(search_word)
    print "Number of views (2001.-2017.): ", number_of_views
