import recommender_core.coldstart as coldstart
import recommender_core.userrecommender as userrecommender
from recommender_core.Recommender import initialize_recommender

def recommend(user, city):
    # TODO decide which strategy to choose, for now just use the coldstart

    coldstart_recommender = initialize_recommender(coldstart.ColdStartRecommender)
    user_recommender = initialize_recommender(userrecommender.UserRecommender)
    return user_recommender.recommend(city, user)
