import sqlite3

# make sure that tables exist - in case of changes after deployment add migrations here
def initialize(db):
    if db is None:
        raise ValueError('db is None! Initialize DB first!')

    create_or_migrate_schema(db)

def create_or_migrate_schema(conn):
    create_or_migrate_users(conn)
    create_or_migrate_reviews(conn)

def create_or_migrate_users(conn):
    conn.execute('''
    create table if not exists USERS
    (
      NAME text primary key,
      DESCRIPTION text
    )''')

def create_or_migrate_reviews(conn):
    conn.execute(
    '''
    create table if not exists REVIEWS
    (
      REVIEW_ID integer primary key,
      NODE_ID integer,
      USER text,
      REVIEW_VALUE integer,
      FOREIGN KEY(NODE_ID) REFERENCES NODES(NODE_ID),
      FOREIGN KEY(USER) REFERENCES USERS(NAME),
      CONSTRAINT review_user_uniquity UNIQUE(NODE_ID, USER, REVIEW_VALUE)
    )'''
    )

