from frontend.api.App import app

from flask import request

import connection_provider

import json

@app.route('/api/v1/review/<nodeid>', methods = ["PUT"])
def evaluate(nodeid):
    # return an object or list with different recommendations
    value = request.json['review']
    user = request.json['username']

    conn = connection_provider.get_fresh()
    cursor = conn.cursor()
    # replace since this is put - we could change our mind.
    cursor.execute("insert or replace into REVIEWS(NODE_ID,USER,REVIEW_VALUE) VALUES (?,?,?)",(nodeid,user,value));
    conn.commit()
    conn.close()

    return json.dumps({})
