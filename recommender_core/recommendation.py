import connection_provider
import recommender_core.coldstart as coldstart
import recommender_core.userrecommender as userrecommender
from recommender_core.Recommender import initialize_recommender

def recommend(user, city):
    # TODO decide which strategy to choose, for now just use the coldstart

    if (choose_user_recommendation(user)==True):
        user_recommender = initialize_recommender(userrecommender.UserRecommender)
        return user_recommender.recommend(city, user)
    else:
        coldstart_recommender = initialize_recommender(coldstart.ColdStartRecommender)
        return coldstart_recommender.recommend(city,user)


def choose_user_recommendation(user):
    conn = connection_provider.get_fresh()
    cursor = conn.cursor()

    cursor.execute("select REVIEW_ID FROM REVIEWS WHERE USER='{}'".format(user))
    result = cursor.fetchone()
    
    conn.close()

    if result == None:
        return False
    else:
        return True
