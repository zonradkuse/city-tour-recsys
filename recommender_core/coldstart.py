from recommender_core.Recommender import Recommender
from recommender_core.Tour import TourSolver
import connection_provider

import numpy as np
from sklearn.cluster import DBSCAN

EXCLUDE_TAGS_SQL_STRING = "('vending_machine', 'bicycle_parking')"
DEBUG = True

class ColdStartRecommender(Recommender):

    def recommend(self, city, user):
        recom=self.coldstart_recommendations(city)
        result = []

        # tuples of names and coordinates
        for origin, dest in recom.edges():
            or_values = (origin["NODE_ID"], origin["NAME"], origin["LON"], origin["LAT"])
            des_values = (dest["NODE_ID"], dest["NAME"], dest["LON"], dest["LAT"])
            result.append((or_values, des_values))

        return result


    def coldstart_recommendations(self, city):
        # We want to find a good coldstart without requiring any user data.
        # For this purpose we assume that interesting POIs are surrounded by
        # restaurants, cafes, souvenir shops, etc. Hence, we are looking for
        # clusters around the city. We use DBSCAN for this purpose.

        print(f'Creating coldstart recommendations for city {city}.')
        city_data = self.query_city_data(city)

        if DEBUG:
            self.print_city_data(city_data)

        coordinates = {}
        for point in city_data:
            if point["LON"] is not None and point["LAT"] is not None:
                coordinates[(point["LON"], point["LAT"])] = point
            else:
                print(f'[WARN] Found point without coordinates: {point}')


        # labels identify the clusters
        # TODO try different parameters - should be similar for multiple cities, otherwise
        # we have to solve a optimization problem as follows:
        # find parameters which maximize clusters while minimizing noise for regions of high
        # centrality.
        db = DBSCAN(eps=0.0015, min_samples=3).fit(np.asarray(list(coordinates.keys())))

        labels = db.labels_
        print(f'DBSCAN found {len(set(labels))} clusters.')

        # label all the nodes with their appropriate cluster - list(tuple(data_point, cluster_id))
        labeled_data = self.label_data(city_data, labels)

        if DEBUG:
            self.print_clusters(labeled_data)

        # this is already sorted by importance
        attractions = self.extract_attractions(labeled_data)

        if DEBUG:
            print('-- Suggestions --')
            self.print_city_data(attractions)

        solver = TourSolver()
        for atr in attractions:
            solver.add_poi(atr)

        tour = solver.solve()

        if DEBUG:
            print(tour)

        return tour

    def query_city_data(self, city_name):
        # create sql query for this
        conn = connection_provider.get_fresh_with_row()
        c = conn.cursor()

        resultset = []

        # TODO filter by specific tags - we probably don't really need non-touristy stuff
        c.execute("select 'TRSM' as SRC, * from NODES as n, TOURISM as t where city=? and (n.NODE_ID = t.NODE_ID) COLLATE NOCASE", (city_name,))
        resultset.extend(c.fetchall())

        # TODO this is prone to sql injection but I could not find a way to use the 'in' statement
        c.execute(f"select 'AMNT' as SRC, * from NODES as n, AMENITIES as t where city=? and n.NODE_ID = t.NODE_ID and NAME is not null and not TYPE in {EXCLUDE_TAGS_SQL_STRING} COLLATE NOCASE", (city_name,))
        resultset.extend(c.fetchall())

        return resultset

    def print_city_data(self, data):
        for item in data:
            print(f'Considering data {item["NAME"]}.')

    def label_data(self, city_data, labels):
        # assert(len(labels) == len(city_data))

        result = {}
        for index in range(len(labels)):
            item = city_data[index]

            result[item] = labels[index]

        return result

    def get_clusters(self, labeled_data):
        result = {}

        for cluster in set(labeled_data.values()):
            if cluster not in result:
                result[cluster] = []

        for item in labeled_data.keys():
            result[labeled_data[item]].append(item)

        return result

    def print_clusters(self, labeled_data):
        clusters = self.get_clusters(labeled_data)

        for clusterid in clusters.keys():
            items = clusters[clusterid]

            itemdesc = ""
            for item in items:
                itemdesc += f'{item["NAME"]}, '

            print(f'cluster no. {clusterid} has items [{len(items)}: {itemdesc}]')

    def extract_attractions(self, labeled_data):
        clusters = self.get_clusters(labeled_data)

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
