import connection_provider
import recommender_core.coldstart as coldstart
import recommender_core.userrecommender as userrecommender
from recommender_core.Recommender import initialize_recommender

def recommend(user, city, max_dist = None):
    recommenders = {}
    recommenders["user"] = initialize_recommender(userrecommender.UserRecommender)
    recommenders["cold"] = initialize_recommender(coldstart.ColdStartRecommender)

    for key, rec in recommenders.items():
        rec.max_dist = max_dist

    if (choose_user_recommendation(user)):
        user_recommender = recommenders["user"]
        return user_recommender.recommend(city, user)
    else:
        coldstart_recommender = recommenders["cold"]
        return coldstart_recommender.recommend(city,user)


def choose_user_recommendation(user):
    conn = connection_provider.get_fresh()
    cursor = conn.cursor()

    # TODO this doesn't work since it doesn't respect the selected city. Hence, recommendations are guaranteed to be random or empty.
    cursor.execute("select REVIEW_ID FROM REVIEWS WHERE USER='{}'".format(user))
    result = cursor.fetchone()

    conn.close()

    # TODO this should rather be the length of the resultset
    if result == None:
        return False
    else:
        return True
