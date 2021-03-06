import connection_provider as cp

class Recommender:

    def __init__(self, dbconn, max_dist):
        self.conn = dbconn
        self.max_dist = max_dist


    # Abstract Method responsible for recommendation.
    #
    # Input: city_name string, username string
    # Output: [(POI, value between 0 and 1 indicating match)]
    def recommend(city, user):
        assert(false) # abstract! - we do not actually call this but it's specialization
        pass

def initialize_recommender(clazz):
    instance = clazz(cp.get(), None)

    return instance

