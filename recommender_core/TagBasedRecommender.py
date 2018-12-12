from recommender_core.Recommender import Recommender
from recommender_core.Tour import TourSolver

import connection_provider

class TagBasedRecommender(Recommender):

    def use_dice_coeff(self):
        self.coefficient_method = self.dice

    def use_jaccard_coeff(self):
        self.coefficient_method = self.jaccard

    def recommend(self, city, user):
        # get all nodes
        pois = self.get_city_items(city)
        pois_by_id = {}

        # get all tags a user might like
        user_tags = self.get_liked_tags(user)
        print(user_tags)

        # get poi tags
        poi_tags = {}
        for poi in pois:
            nodeid = poi["NODE_ID"]
            poi_tags[nodeid] = self.get_poi_tags(nodeid)
            pois_by_id[nodeid] = poi

        # compute for all city items the confidence
        confidences = []
        for poi in pois:
            nodeid = poi["NODE_ID"]
            confidences.append((self.coefficient_method(poi_tags[nodeid], user_tags), pois_by_id[nodeid]))

        solver = TourSolver()
        # sort the vector descending
        # add 15 most important items to solver
        for confidence, poi in sorted(confidences, key = lambda item: item[0], reverse = True):
            if len(solver.pois) == 15:
                break

            solver.add_poi(poi)

        if self.max_dist is not None:
            print(f'Restricting tour length to {self.max_dist}km.')
            solver.restrict_tour_length(self.max_dist)

        # return the tour
        return solver.solve()

    def jaccard(self, set_a, set_b):
        return len(set_a.intersection(set_b))/len(set_a.union(set_b))

    def dice(self, set_a, set_b):
        return 2*len(set_a.intersection(set_b))/(len(set_a) + len(set_b))

    def get_liked_tags(self,user):
        conn = connection_provider.get_fresh_with_row()
        cursor = conn.cursor()

        cursor.execute("select t.TAG as TAG FROM REVIEWS as r,NODES as n,TAGS as t WHERE n.NODE_ID=r.NODE_ID AND t.NODE_ID=r.NODE_ID AND r.USER='{}' group by TAG COLLATE NOCASE".format(user))

        resultset = []
        for row in cursor.fetchall():
            resultset.append(row["TAG"])

        conn.close()

        return set(resultset)

    def get_city_items(self, city):
        conn = connection_provider.get_fresh_with_row()
        cursor = conn.cursor()

        cursor.execute("select * FROM NODES where city = ? and name != ''", (city,))

        resultset = cursor.fetchall()
        conn.close()

        return resultset

    def get_poi_tags(self, nodeid):
        conn = connection_provider.get_fresh_with_row()
        cursor = conn.cursor()

        cursor.execute("select TAG FROM TAGS where NODE_ID = ? COLLATE NOCASE group by TAG", (nodeid,))

        resultset = []
        for row in cursor.fetchall():
            resultset.append(row["TAG"])

        conn.close()

        return set(resultset)
