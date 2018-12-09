from frontend.api.App import app
import osmnx

import connection_provider
import json


@app.route('/api/v1/city')
def get_all_cities():
    conn = connection_provider.get_fresh()
    cursor = conn.cursor()
    cursor.execute("select city from NODES group by city")
    result = cursor.fetchall()
    conn.close()
    print(result)

    return json.dumps(result)

@app.route('/api/v1/search/<query>')
def search_city(query):
    result = osmnx.osm_polygon_download(query)
    print(len(result))

    return json.dumps(result)
