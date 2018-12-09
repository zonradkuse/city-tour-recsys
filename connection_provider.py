import sqlite3

conn = None
dbpath = None

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def set_db_path(path):
    global dbpath
    dbpath = path

def set(_conn):
    # TODO make this a ProviderClass instead
    global conn
    conn = _conn

def get():
    assert(conn is not None)
    return conn

def get_fresh():
    fconn = sqlite3.connect(dbpath)
    # fconn.row_factory = dict_factory
    return fconn

def get_cursor():
    assert(conn is not None)
    return conn.cursor()

