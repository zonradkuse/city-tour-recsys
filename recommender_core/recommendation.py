import recommender_core.coldstart as coldstart
from recommender_core.Recommender import initialize_recommender

def recommend(user, city):
    # TODO decide which strategy to choose, for now just use the coldstart

    coldstart_recommender = initialize_recommender(coldstart.ColdStartRecommender)
    return coldstart_recommender.recommend(city, user)

