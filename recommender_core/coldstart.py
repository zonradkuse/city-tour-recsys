import recommender_core.misc
import connection_provider as cp
# import settings
import numpy as np
from sklearn.cluster import DBSCAN

EXCLUDE_TAGS_SQL_STRING = "('vending_machine', 'bicycle_parking')"
DEBUG = True

def coldstart_recommendations(city):
    # We want to find a good coldstart without requiring any user data.
    # For this purpose we assume that interesting POIs are surrounded by
    # restaurants, cafes and souvenir shops. Hence, we are looking for
    # clusters around the city. We use DBSCAN for this purpose.

    print(f'Creating coldstart recommendations for city {city}.')
    city_data = query_city_data(city)

    if DEBUG:
        print_city_data(city_data)

    coordinates = {}
    for point in city_data:
        coordinates[(point["LON"], point["LAT"])] = point

    # labels identify the clusters
    # TODO try different parameters - should be similar for multiple cities, otherwise
    # we have to solve a optimization problem as follows:
    # find parameters which maximize clusters while minimizing noise for regions of high
    # centrality.
    db = DBSCAN(eps=0.001, min_samples=3).fit(np.asarray(list(coordinates.keys())))

    labels = db.labels_
    print(f'DBSCAN found {len(set(labels))} clusters.')

    # label all the nodes with their appropriate cluster - list(tuple(data_point, cluster_id))
    labeled_data = label_data(city_data, labels)

    if DEBUG:
        print_clusters(labeled_data)

    # this is already sorted by importance
    attractions = extract_attractions(labeled_data)

    if DEBUG:
        print('-- Suggestions --')
        print_city_data(attractions)

    return attractions

def query_city_data(city_name):
    # create sql query for this
    c = cp.get().cursor()

    resultset = []

    # TODO filter by specific tags - we probably don't really need non-touristy stuff
    c.execute("select 'TRSM' as SRC, * from NODES as n, TOURISM as t where city=? and (n.NODE_ID = t.NODE_ID) COLLATE NOCASE", (city_name,))
    resultset.extend(c.fetchall())

    # TODO this is prone to sql injection but I could not find a way to use the 'in' statement
    c.execute(f"select 'AMNT' as SRC, * from NODES as n, AMENITIES as t where city=? and n.NODE_ID = t.NODE_ID and NAME is not null and not TYPE in {EXCLUDE_TAGS_SQL_STRING} COLLATE NOCASE", (city_name,))
    resultset.extend(c.fetchall())

    return resultset

def print_city_data(data):
    for item in data:
        print(f'Considering data {item["NAME"]}.')

def label_data(city_data, labels):
    # assert(len(labels) == len(city_data))

    result = {}
    for index in range(len(labels)):
        item = city_data[index]

        result[item] = labels[index]

    return result

def get_clusters(labeled_data):
    result = {}

    for cluster in set(labeled_data.values()):
        if cluster not in result:
            result[cluster] = []

    for item in labeled_data.keys():
        result[labeled_data[item]].append(item)

    return result

def print_clusters(labeled_data):
    clusters = get_clusters(labeled_data)

    for clusterid in clusters.keys():
        items = clusters[clusterid]

        itemdesc = ""
        for item in items:
            itemdesc += f'{item["NAME"]}, '

        print(f'cluster no. {clusterid} has items [{len(items)}: {itemdesc}]')

def extract_attractions(labeled_data):
    clusters = get_clusters(labeled_data)

    clustersizes = []
    for cid, items in clusters.items():
        if cid != -1:
            clustersizes.append((cid, len(items)))

    sortedsizes = sorted(clustersizes, key=lambda item: item[1], reverse=True)

    attractions = []
    for cid, ln in sortedsizes:
        # now we are extracting the attractions from this sorted list
        for item in clusters[cid]:
            if item['SRC'] == 'TRSM':
                attractions.append(item)

    return attractions

