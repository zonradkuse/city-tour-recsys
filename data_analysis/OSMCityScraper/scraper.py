from osmapi import OsmApi
import sys
import argparse
import sqlite3

def scrape(dbcon, bounding_box):
    print("Initializing data scraping from OSM...")

    print("Preparing database schema...")
    check_and_migrate_schema(dbcon)

    print("Connection to OSM API...")
    api = OsmApi()

    print(f'Fetching data for coordinates {bounding_box}.')
    city_data = api.Map(*bounding_box)
    print(f'OSM gave us {len(city_data)} entries.')

    print("Extracting node data...")
    node_data = analyze_data(city_data)
    print(f'Found {len(node_data)} relevant nodes in extract.')

    print("Writing obtained data to database...")
    write_data_to_db(dbcon, node_data)

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
      NAME text
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

    # if you ever change anything in the schema, check here whether your desired change
    # is already applied and if not apply the change without dropping data!!
    # We don't want to mess around with manual db changes!

def analyze_data(data):
    relevant_nodes = []
    for elem in data:
        # we require the nodes to have at least one tag and a name or being amenity
        # we assume that tourist tags have names. Otherwise they are most likely useless.
        if elem["type"] == "node" and len(elem["data"]["tag"].keys()) > 0 and ("name" in elem["data"]["tag"] or "amenity" in elem["data"]["tag"]):
            relevant_nodes.append(elem["data"])

    return relevant_nodes

def write_data_to_db(dbcon, data):
    for elem in data:
        insert_node(dbcon, elem)

        if "amenity" in elem["tag"]:
            insert_amenity(dbcon, elem)

        if "tourism" in elem["tag"]:
            insert_tourism(dbcon, elem)

        if "shop" in elem["tag"]:
            insert_shop(dbcon, elem)

def insert_node(con, elem):
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
    insert into NODES (NAME, NODE_ID, IMAGE_LINK, WEBSITE, LON, LAT, DESCRIPTION, PHONE, EMAIL)
       VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, nid, image_link, website, lon, lat, descr, phone, email))

def insert_amenity(dbcon, elem):
    ntype = elem["tag"].get("amenity")
    nid = elem["id"]
    ndesc = elem["tag"].get("cuisine")
    dbcon.execute('insert into AMENITIES (NODE_ID, TYPE, DESCRIPTION) VALUES (?, ?, ?)', (nid, ntype, ndesc))


def insert_tourism(dbcon, elem):
    ntype = elem["tag"].get("tourism")
    nid = elem["id"]
    ndesc = elem["tag"].get("artwork_type")
    dbcon.execute('insert into TOURISM (NODE_ID, TYPE, DESCRIPTION) VALUES (?, ?, ?)', (nid, ntype, ndesc))

def insert_shop(dbcon, elem):
    ntype = elem["tag"].get("shop")
    nid = elem["id"]
    dbcon.execute('insert into SHOPS (NODE_ID, TYPE) VALUES (?, ?)', (nid, ntype))

