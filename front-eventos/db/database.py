import pyodbc
from flask import g

# Configurações do SQL Server
SQL_SERVER_CONFIG = {
    'driver': '{ODBC Driver 18 for SQL Server}',
    'server': '.\\SQLEXPRESS',
    'database': 'Projeto',
    'trusted_connection': 'yes',
}

CURRENT_SQL_SERVER_CONFIG = SQL_SERVER_CONFIG.copy()

def build_connection_string(config):
    driver = config['driver']
    server = config['server']
    database = config['database']
    if config.get('trusted_connection', 'no').lower() in ('yes', 'true', 'sspi'):
        return f"DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes;TrustServerCertificate=yes;"

    username = config['username']
    password = config['password']
    return f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};TrustServerCertificate=yes;"


def set_db_config(config):
    global CURRENT_SQL_SERVER_CONFIG
    CURRENT_SQL_SERVER_CONFIG = config


def get_db_config():
    return CURRENT_SQL_SERVER_CONFIG


def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        connection_string = build_connection_string(get_db_config())
        db = pyodbc.connect(connection_string, autocommit=False)
        g.db = db
    return db


def close_db(exception=None):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


def fetch_all(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def fetch_one(cursor):
    row = cursor.fetchone()
    if row is None:
        return None
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, row))


def init_db():
    pass
