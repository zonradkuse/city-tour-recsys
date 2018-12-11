from frontend.api.App import app
import osmnx
import recommender_core

import json

@app.route('/api/v1/recommendation/<username>/<city>')
def recommend(username, city):
    # return an object or list with different recommendations
    return json.dumps(recommender_core.recommend(username, city))
