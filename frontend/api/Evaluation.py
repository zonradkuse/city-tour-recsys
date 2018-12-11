from frontend.api.App import app

from flask import request

import json

@app.route('/api/v1/evaluate/<nodeid>', methods = ["PUT"])
def evaluate(nodeid):
    # return an object or list with different recommendations
    value = request.json['evaluation']
    user = request.json['username']

    # TODO write this to database

    return json.dumps(value)
