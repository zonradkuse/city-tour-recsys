from frontend.api.App import app
import osmnx
import recommender_core

import json

@app.route('/api/v1/recommendation/<username>/<city>')
def recommend(username, city):
    # return an object or list with different recommendations
    result = recommender_core.recommend(username, city)


    #THIS IS NOW IN THE COLD START recommend method
    # tuples of names and coordinates
    #for origin, dest in recom.edges():
    #    or_values = (origin["NODE_ID"], origin["NAME"], origin["LON"], origin["LAT"])
    #    des_values = (dest["NODE_ID"], dest["NAME"], dest["LON"], dest["LAT"])
    #    result.append((or_values, des_values))


    
    return json.dumps(result)
