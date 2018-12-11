from recommender_core.Recommender import Recommender
import connection_provider

import numpy as np
import json

DEBUG = True

class UserRecommender(Recommender):

    def recommend(self,city,user):
        liked_tags = self.get_liked_tags(user)
        liked_nodes = self.get_liked_nodes(user)

        newnodes = self.get_newnodes_based_on_tags(liked_tags,liked_nodes)


        result=[]
        for i in range(len(newnodes)):
            result.append(newnodes[i][0])

        
        return result

    def get_liked_nodes(self,user):
        conn = connection_provider.get_fresh()
        cursor = conn.cursor()

        cursor.execute("select NODES.NODE_ID FROM REVIEWS,NODES WHERE REVIEWS.USER='{}' AND NODES.NODE_ID=REVIEWS.NODE_ID".format(user))

        result = cursor.fetchall()
        conn.close()
        return result

    def get_liked_tags(self,user):
        conn = connection_provider.get_fresh_with_row()

        cursor = conn.cursor()
        resultset=[]

        cursor.execute("select t.TAG FROM REVIEWS as r,NODES as n,TAGS as t WHERE n.NODE_ID=r.NODE_ID AND t.NODE_ID=r.NODE_ID AND r.USER='{}'".format(user))

        resultset.extend(cursor.fetchall())
        conn.close()

        return resultset


    def get_newnodes_based_on_tags(self,liked_tags,liked_nodes):

        tags =""

        for i in range(len(liked_tags)):
            tags=tags+"'"+liked_tags[i][0]+"'"+", "
        tags=tags[:-2]

        nodes=""
        for i in range(len(liked_nodes)):
            nodes=nodes+str(liked_nodes[i][0])+", "
        nodes=nodes[:-2]

        conn = connection_provider.get_fresh_with_row()
        cursor = conn.cursor()

        cursor.execute("select NODE_ID from TAGS where TAG IN ({}) and NODE_ID NOT IN ({})".format(tags,nodes))
        result = cursor.fetchall()


        conn.close()
        return result
