from recommender_core.Recommender import Recommender
from data_analysis.OSMCityScraper import wordcount
from data_analysis.OSMCityScraper import pageviews
from data_analysis.OSMCityScraper import googlesearch

from operator import itemgetter
import connection_provider

import numpy as np
import json

DEBUG = True

class UserRecommender(Recommender):

    def recommend(self,city,user):
        liked_tags = self.get_liked_tags(user)
        liked_nodes = self.get_liked_nodes(user)

        newnodes = self.get_newnodes_based_on_tags(liked_tags,liked_nodes)

        list_of_nodes=[]
        for i in range(len(newnodes)):
            list_of_nodes.append(newnodes[i][0])

        result=self.get_quality_measures(list_of_nodes)

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

    def get_quality_measures(self,in_nodes):
        conn = connection_provider.get_fresh_with_row()
        cursor = conn.cursor()

        nodes=""
        for i in range(len(in_nodes)):
            nodes=nodes+str(in_nodes[i])+", "
        nodes=nodes[:-2]

        cursor.execute("select NODE_ID,NAME from NODES where NODE_ID IN ({})".format(nodes))
        result = cursor.fetchall()

        node_names=[]
        for i in range(len(result)):
            node_names.append([result[i]["NODE_ID"],result[i]["NAME"]])

        wordcount_res=[]
        pageviews_res=[]
        googlesearch_res=[]

        for node in node_names:
            out = wordcount.wordcount(node[1])
            if (out != None):
                wordcount_res.append([node[0],out])
            out = pageviews.pageviews(node[1])
            if (out != None):
                pageviews_res.append([node[0],out])
            out = googlesearch.googlesearch(node[1])
            if (out != None):
                googlesearch_res.append([node[0],out])

        wordcount_res.sort(key=itemgetter(1),reverse=True)
        pageviews_res.sort(key=itemgetter(1),reverse=True)
        googlesearch_res.sort(key=itemgetter(1),reverse=True)

        final_nodes=[]
        count=0

        for x in range(0,10):
            if (x < len(wordcount_res) and (wordcount_res[i][0] in final_nodes)==False):
                final_nodes.append(wordcount_res[i][0])
                count=count+1
            if (count==10):
                break
            if (x < len(pageviews_res) and (pageviews_res[i][0] in final_nodes)==False):
                final_nodes.append(pageviews_res[i][0])
                count=count+1
            if (count==10):
                break
            if (x < len(googlesearch_res) and (googlesearch_res[i][0] in final_nodes)==False):
                final_nodes.append(googlesearch_res[i][0])
                count=count+1
            if (count==10):
                break


        return final_nodes
