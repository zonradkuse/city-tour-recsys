from osmapi import OsmApi
import osmapi
import osmnx
import sqlite3
from shapely.geometry import shape, box, LineString
from shapely.ops import split
import time

DEBUG = True

all_amenities = None
#all_amenities = ['townhall']
#all_amenities = ['restaurant', 'bar', 'pub', 'toilets', 'post_office', 'post_box', 'police', 'marketplace', 'embassy', 'fire_station', 'coworking_space', 'theatre', 'social_centre', 'planetarium', 'gambling', 'fountain', 'cinema', 'arts_centre', 'atm', 'bank', 'bicycle_parking', 'cafe', 'food_court', 'townhall']
touristy_amenities = ['fountain', 'marketplace', 'townhall', 'theatre']

def scrape(dbcon, bounding_box, city):
    print("Initializing data scraping from OSM...")

    print("Preparing database schema...")
    check_and_migrate_schema(dbcon)

    print("Connection to OSM API...")
    api = OsmApi()

    city_data = None

    if bounding_box is not None:
        print(f'Fetching data for coordinates {bounding_box} using OsmApi.')
        city_data = recurse_osmapi(*bounding_box)
        print(f'OSM gave us {len(city_data)} entries.')
    elif city is not None:
        print(f'Fetching data for {city} using osmnx.')
        city_data = fetch_poi_osmnx(city)
    else:
        raise ValueError("Neither Bounding Box nor City specified!")


    print("Extracting node data...")
    node_data = analyze_data(city_data)
    print(f'Found {len(node_data)} relevant nodes in extract.')

    # construct_missing_coordinates(node_data)

    print("Writing obtained data to database...")
    write_data_to_db(dbcon, node_data, city)

    dbcon.commit()

    print("DONE! :-)")


def check_and_migrate_schema(conn):
    # create fully if a table does not exist
    conn.execute('''
    create table if not exists NODES
    (
      NODE_ID integer primary key,
      IMAGE_LINK text,
      WEBSITE text,
      LON real,
      LAT real,
      DESCRIPTION text,
      PHONE text,
      EMAIL text,
      NAME text,
      CITY text
    )
    ''')

    conn.execute('''
    create table if not exists AMENITIES
    (
      NODE_ID integer unique,
      DESCRIPTION text,
      TYPE text,
      FOREIGN KEY(NODE_ID) REFERENCES NODES(NODE_ID)
    )
    ''')

    conn.execute('''
    create table if not exists TOURISM
    (
      NODE_ID integer unique,
      DESCRIPTION text,
      TYPE text,
      FOREIGN KEY(NODE_ID) REFERENCES NODES(NODE_ID)
    )
    ''')

    conn.execute('''
    create table if not exists SHOPS
    (
      NODE_ID integer unique,
      TYPE text,
      FOREIGN KEY(NODE_ID) REFERENCES NODES(NODE_ID)
    )
    ''')


    # table just for storing many tags for one
    conn.execute('''
    create table if not exists TAGS
    (
      NODE_ID integer,
      KEY text,
      TAG text,
      FOREIGN KEY(NODE_ID) REFERENCES NODES(NODE_ID),
      PRIMARY KEY(NODE_ID, KEY, TAG)
    )
    ''')

    # table for node quality measures like wikipedia word count, google search results, etc...
    conn.execute('''
    create table if not exists QUALITY_MEASURES
    (
      NODE_ID integer,
      MEASURE_NAME text,
      VALUE integer,
      FOREIGN KEY(NODE_ID) REFERENCES NODES(NODE_ID),
      PRIMARY KEY(NODE_ID)
    )
    ''')

    conn.execute('''
    alter table NODES add column pageviews integer;
    ''')

    conn.execute('''
    alter table NODES add column googlesearch integer;
    ''')

    conn.execute('''
    alter table NODES add column wordcount integer;
    ''')

    # if you ever change anything in the schema, check here whether your desired change
    # is already applied and if not apply the change without dropping data!!
    # We don't want to mess around with manual db changes!

def fetch_poi_osmnx(city):
    # get initial bounding box from osmnx nodes
    result = osmnx.osm_polygon_download(city)
    if len(result) > 1:
        raise ValueError("Provided city is ambiguous!")

    if len(result) == 0:
        raise ValueError("Could not find provided city!")

    search_result = result[0]
    poly = shape(search_result['geojson'])
    bounding_box = poly.bounds

    # download pois using osmapi since osmnx data is not completely/weirdly tagged. Some
    # very important places miss lon/lat specifications. For this, use the bounding box of
    # the obtained polytope and recursively download all data using OsmApi.
    # NOTE: This might take ages - might be a good idea to scrape a list of cities over night.
    elems = recurse_osmapi(*bounding_box)

    return elems

def recurse_osmapi(minx, miny, maxx, maxy):
    api = OsmApi() # TODO make globally available if too slow

    if DEBUG:
        print(f"recursing into {(minx, miny, maxx, maxy)}")

    elems = []
    try:
        elems.extend(api.Map(minx, miny, maxx, maxy))
    except osmapi.ApiError as er:
        if er.status == 400:
            # we requested too many elements - split box in half and process separately
            splitter_x = LineString([((minx + maxx)/2, miny), ((minx + maxx)/2, maxy)])
            bounding_box = box(minx, miny, maxx, maxy)
            boxes_split_x = split(bounding_box, splitter_x)

            splitter_y = LineString([(minx, (miny + maxy)/2), (maxx, (miny + maxy)/2)])

            boxes = []
            for b in boxes_split_x:
                boxes.extend(split(b, splitter_y))

            for b in boxes:
                elems.extend(recurse_osmapi(*b.bounds))

        elif er.status == 509:
            # we shall wait and try again
            print("Waiting 30s because of API response...")
            time.sleep(30)
            recurse_osmapi(minx, miny, maxx, maxy)
        else:
            raise er

    return elems

def analyze_data(data):
    relevant_nodes = []
    relevant_ids = []
    for elem in data:

        # we require the nodes to have at least one tag and a name or being amenity
        # we assume that tourist tags have names. Otherwise they are most likely useless.
        if elem["type"] == "node" and len(elem["data"]["tag"].keys()) > 0 and ("name" in elem["data"]["tag"] or "amenity" in elem["data"]["tag"]):
            if elem["data"]["id"] not in relevant_ids:
                relevant_ids.append(elem["data"]["id"])
                relevant_nodes.append(elem["data"])

    return relevant_nodes

def write_data_to_db(dbcon, data, city):
    for elem in data:
        insert_node(dbcon, elem, city)

        if "amenity" in elem["tag"] or ("tourism" in elem["tag"] and elem["tag"].get("tourism") == "hotel"):
            insert_amenity(dbcon, elem)

        if "tourism" in elem["tag"] and elem["tag"].get("tourism") != "hotel":
            insert_tourism(dbcon, elem)

        if "shop" in elem["tag"]:
            insert_shop(dbcon, elem)

        insert_tags(dbcon, elem)


def insert_node(con, elem, city):
    name = elem["tag"].get("name")
    nid = elem.get("id")
    image_link = elem["tag"].get("image_link")
    website = elem["tag"].get("website")
    lon = elem.get("lon")
    lat = elem.get("lat")
    descr = elem["tag"].get("description")
    phone = elem["tag"].get("phone")
    email = elem["tag"].get("email")

    con.execute('''
    insert or replace into NODES (NAME, NODE_ID, IMAGE_LINK, WEBSITE, LON, LAT, DESCRIPTION, PHONE, EMAIL, CITY)
       VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, nid, image_link, website, lon, lat, descr, phone, email, city))

def insert_amenity(dbcon, elem):
    ntype = elem["tag"].get("amenity")
    nid = elem["id"]
    ndesc = elem["tag"].get("cuisine")
    dbcon.execute('insert or ignore into AMENITIES (NODE_ID, TYPE, DESCRIPTION) VALUES (?, ?, ?)', (nid, ntype, ndesc))


def insert_tourism(dbcon, elem):
    ntype = elem["tag"].get("tourism")
    nid = elem["id"]
    ndesc = elem["tag"].get("artwork_type")
    dbcon.execute('insert or ignore into TOURISM (NODE_ID, TYPE, DESCRIPTION) VALUES (?, ?, ?)', (nid, ntype, ndesc))

def insert_shop(dbcon, elem):
    ntype = elem["tag"].get("shop")
    nid = elem["id"]
    dbcon.execute('insert or ignore into SHOPS (NODE_ID, TYPE) VALUES (?, ?)', (nid, ntype))

def insert_tags(dbcon, elem):
    tags = elem["tag"]
    nid = elem["id"]
    for key, tag in tags.items():
        dbcon.execute('insert or ignore into TAGS (NODE_ID, KEY, TAG) VALUES (?, ?, ?)', (nid, key, tag))


def ignore_node(elem):
    lon = elem["data"].get("lon")
    lat = elem["data"].get("lat")
    name = elem["data"]["tags"].get("name")

    return lon is None or lat is None or name is None

def construct_missing_coordinates(data):
    coord_index = {}
    for elem in data:
        if elem["type"] == "node":
            coord_index[elem["id"]] = (elem["lon"], elem["lat"])

    for elem in data:
        if elem["type"] == "node":
            continue

        if "nodes" not in elem:
            continue

        if "lon" not in elem or "lat" not in elem:
            way_node = None
            for n in elem["nodes"]:
                if n in coord_index:
                    way_node = n

            if way_node is None:
                print(f'way with tags {elem["tags"]} has no known coordinates.')
                api = OsmApi()
                api_node = api.NodeGet(elem["nodes"][0])
                way_node = api_node["id"]
                coord_index[way_node] = (api_node["lon"], api_node["lat"])

            elem["lon"] = coord_index[way_node][0]
            elem["lat"] = coord_index[way_node][1]
