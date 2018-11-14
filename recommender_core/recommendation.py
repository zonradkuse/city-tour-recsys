import recommender_core.coldstart as coldstart

def recommend(user, city):
    # TODO decide which strategy to choose, for now just use the coldstart

    return coldstart.coldstart_recommendations(city)

