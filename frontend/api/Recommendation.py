from frontend.api.App import app
import osmnx
import recommender_core

from flask import request

import json

@app.route('/api/v1/recommendation/<username>/<city>')
def recommend(username, city):
    maxDistance = request.args.get("maxDistance")

    # return an object or list with different recommendations
    recom = recommender_core.recommend(username, city, maxDistance)
    result = []

    # tuples of names and coordinates
    for origin, dest in recom.edges():
        or_values = (origin["NODE_ID"], origin["NAME"], origin["LON"], origin["LAT"])
        des_values = (dest["NODE_ID"], dest["NAME"], dest["LON"], dest["LAT"])
        result.append((or_values, des_values))

    return json.dumps(result)
