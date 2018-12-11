from recommender_core.Recommender import Recommender
import connection_provider

import numpy as np

DEBUG = True

class UserRecommender(Recommender):

    def recommend(self,city,user):
        liked_tags = self.get_liked_tags(user)
        liked_nodes = self.get_liked_nodes(user)

        newnodes = self.get_newnodes_based_on_tags(liked_tags,liked_nodes)
        return newnodes

    def get_liked_nodes(self,user):
        conn = connection_provider.get_fresh()
        cursor = conn.cursor()

        cursor.execute("select NODES.NODE_ID FROM REVIEWS,NODES WHERE REVIEWS.USER='"+user+"' AND NODES.NODE_ID=REVIEWS.NODE_ID")

        result = cursor.fetchall()
        conn.close()
        return result

    def get_liked_tags(self,user):
        conn = connection_provider.get_fresh_with_row()
        cursor = conn.cursor()
        resultset=[]

        #cursor.execute("select t.TAG FROM REVIEWS as r,NODES as n,TAGS as t WHERE n.NODE_ID=r.NODE_ID AND t.NODE_ID=r.NODE_ID AND r.USER=?",(user,))
        #cursor.execute("select NODES.NODE_ID from NODES INNER JOIN REVIEWS ON NODES.NODE_ID=REVIEWS.NODE_ID ")
        cursor.execute("select n.NODE_ID from REVIEWS as r,NODES as n where r.NODE_ID=n.NODE_ID")

        resultset.extend(cursor.fetchall())
        conn.close()
        print("Get liked tags:")
        print(resultset)

        return resultset


    def get_newnodes_based_on_tags(self,liked_tags,liked_nodes):

        tags =""
        for i in range(len(liked_tags)):
            tags=tags+"'"+liked_tags[i]+"'"+", "
        tags=tags[:-2]

        nodes=""
        for i in range(len(liked_nodes)):
            nodes=nodes+liked_nodes[i]+", "
        nodes=nodes[:-2]

        print("Liked nodes: "+nodes)
        conn = connection_provider.get_fresh_with_row()
        cursor = conn.cursor()

        cursor.execute("select NODE_ID from TAGS where TAG IN ("+tags+") and NODE_ID NOT IN ("+nodes+")")
        result = cursor.fetchall()
        conn.close()
        return result
