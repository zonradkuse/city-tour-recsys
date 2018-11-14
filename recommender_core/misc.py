from geopy.distance import geodesic

def distance(src, dest):
    return geodesic(src, dest).km
