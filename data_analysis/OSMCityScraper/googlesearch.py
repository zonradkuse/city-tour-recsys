import requests
import sys
import json

def googleserch(node):
    session = requests.Session()

    URL = "https://serpapi.com/search.json?q="+node+"&hl=en&gl=us"

    response = session.get(url=URL)
    DATA = response.json()

    if DATA['search_metadata']['status'] != "Success":
        print("No results for the query")
        return

    num_of_results = DATA['search_information']['total_results']
    if num_of_results == None:
        print("No results for the query")
        return

    return num_of_results

if __name__ == '__main__':
    args = sys.argv[1:]
    search_word = ""
    for items in args:
        search_word = search_word + str(items) + " "
    search_word=search_word[:-1]
    num = googleserch(search_word)
    print "Number of google search results for the node: ", num
