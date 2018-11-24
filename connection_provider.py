conn = None

def set(_conn):
    # TODO make this a ProviderClass instead
    global conn
    conn = _conn

def get():
    assert(conn is not None)
    return conn

def get_cursor():
    assert(conn is not None)
    return conn.cursor()

