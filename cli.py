import sys
import argparse
import sqlite3
import networkx as nx
import matplotlib.pyplot as plt
import osmnx as ox
from sklearn.neighbors import KDTree

ox.config(use_cache=True)

import user_management
import recommender_core
import connection_provider

from data_analysis import OSMCityScraper as OSMScraper


def dispatch(args):
    conn = connect_to_db(args.sqlite_db)
    conn.row_factory = sqlite3.Row

    connection_provider.set(conn)
    user_management.initialize(conn)

    if args.bounding_box is not None or not has_city_data(args.city):
        print(f'Scraping data from OSM for box {args.bounding_box}')
        OSMScraper.scrape(conn, args.bounding_box, args.city)

    if args.user is not None:
        assert(args.city is not None)

        # we will need this to plot a city map, move this code later on to frontend

        tour = recommender_core.recommend(args.user, args.city)
        print(tour.degree())

        if args.render_map:
            plot_tour(tour, args.city)

def has_city_data(city):
    try:
        conn = connection_provider.get_cursor()

        conn.execute('select 1 from NODES where city = ?', (city,))

        return len(conn.fetchall()) > 0
    except sqlite3.OperationalError:
        return False

def plot_tour(tour, city):
    # first get a map of the city and afterwards plot the obtained data points on that map
    city_graph = ox.graph_from_place(city, network_type = 'drive')

    closest_nodes = get_closest_nodes(city_graph, tour)

    paths = []
    for e in tour.edges():
        if closest_nodes[e[0]] not in city_graph.nodes() or closest_nodes[e[1]] not in city_graph.nodes():
            continue

        from_node = closest_nodes[e[0]]
        to_node = closest_nodes[e[1]]
        path = nx.shortest_path(city_graph, from_node, to_node)
        paths.append(path)

    fig, ax = ox.plot_graph_routes(city_graph, paths, route_color='blue', show=False, close=False)

    for rcm in tour.nodes():
        # plot the actual poi
        ax.scatter(rcm["LON"], rcm["LAT"], c='green')
        ax.annotate(rcm["NAME"], (rcm["LON"], rcm["LAT"]))

    ax.set_title(city)

    plt.show()

def get_closest_nodes(city_graph, tour):
    nodes, _ = ox.graph_to_gdfs(city_graph)
    tree = KDTree(nodes[['y', 'x']], metric='euclidean')

    # collect closest nodes
    closest_nodes = {}
    for rcm in tour.nodes():
        # get the closest node in the city graph
        closest_id = tree.query([(rcm["LAT"], rcm["LON"])], k=1, return_distance=False)[0]
        closest_osm_id = nodes.iloc[closest_id].index.values[0]
        closest_x = city_graph.node[closest_osm_id]['x']
        closest_y = city_graph.node[closest_osm_id]['y']

        # ax.scatter(closest_x, closest_y, c='red')
        # ax.annotate(rcm["NAME"], (closest_x, closest_y))

        # save the closest node id for later access
        closest_nodes[rcm] = closest_osm_id

    return closest_nodes


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
    parser.add_argument('--render-map', type=bool, help="Indicator whether to render a map or not.")

    args = parser.parse_args()

    dispatch(args)

