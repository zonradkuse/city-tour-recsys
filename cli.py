import sys
import argparse
import sqlite3
import user_management
import recommender_core
import connection_provider

from data_analysis import OSMCityScraper as OSMScraper


def dispatch(args):
    conn = connect_to_db(args.sqlite_db)
    conn.row_factory = sqlite3.Row

    connection_provider.set(conn)
    user_management.initialize(conn)

    if args.bounding_box is not None:
        print(f'Scraping data from OSM for box {args.bounding_box}')
        OSMScraper.scrape(conn, args.bounding_box, args.city)

    if args.user is not None:
        assert(args.city is not None)

        recommender_core.recommend(args.user, args.city)

def connect_to_db(url):
    return sqlite3.connect(url)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse OSM arguments.')
    parser.add_argument('--bounding-box', type=float, nargs=4,
            help='four reals specifying a bounding box to download the data. See http://boundingbox.klokantech.com/. ')
    parser.add_argument('sqlite_db', type=str,
            help='Path to SQLite Database to hold the data. Creates the database if not existing and writes into the database if specified.')
    parser.add_argument('--user', type=str, help="Specify a user to give recommendations for.")
    parser.add_argument('--city', type=str, help="Specify a city to give recommendations for.")

    args = parser.parse_args()

    dispatch(args)

