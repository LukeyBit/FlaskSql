import sqlite3, os

DB_PATH = 'my_server\databases\employed.db'

abs_path = os.path.join(os.getcwd(), DB_PATH)

def create_connection(db_file=abs_path):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    return conn

def command_sql(command, data=None):
    success = False
    conn = create_connection()
    cur = conn.cursor()
    try:
        cur.execute(command, data)
        success = True
        conn.commit()
    except Exception as e:
        print(e)
    conn.close()
    return success

def select_with_data(command, data):
    result = []
    conn = create_connection()
    cur = conn.cursor()
    try:
        output = cur.execute(command, data)
        result = output.fetchall()
    except Exception as e:
        print(e)
    conn.close()
    return result
    
def select_sql(values, table):
    data = []
    command = f'SELECT {values} FROM {table}'
    conn = create_connection()
    cur = conn.cursor()
    try:
        output = cur.execute(command)
        data = output.fetchall()
    except Exception as e:
        print(e)
    conn.close()
    return data
