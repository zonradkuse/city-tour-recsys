from osmapi import OsmApi
import sys
import argparse

def run(args):
    print("Welcome!")
    print("Connection to OSM API...")
    api = OsmApi()

    print(f'Fetching data for coordinates {args.bounding_box}.')
    city_data = api.Map(*args.bounding_box)
    analyze_data(city_data)

def create_database():
    pass

def connect_database(url):
    pass

def write_data_to_db(db_connection):
    pass

def analyze_data(data):
    for elem in data:
        # we require the nodes to have at least one tag and a name or being amenity
        if elem["type"] == "node" and len(elem["data"]["tag"].keys()) > 0 and ("name" in elem["data"]["tag"] or "amenity" in elem["data"]["tag"]):
            print(f'NodeId {elem["data"]["id"]} has tags {elem["data"]["tag"]}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse OSM arguments.')
    parser.add_argument('bounding_box', type=float, nargs=4,
            help='four reals specifying a bounding box to download the data. See http://boundingbox.klokantech.com/. ')
    parser.add_argument('--sqlite', type=str,
            help='Path to SQLite Database to hold the data. Creates the database if not existing and writes into the database if specified.')


    args = parser.parse_args()
    run(args)

