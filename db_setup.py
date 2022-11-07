from my_server.db_handler import create_connection

departments = [
    ('H', 'Högkvarteret'),
    ('S', 'Säkerhet'),
    ('C', 'Data')
]

employees = [
    ('Stina', '2677', 30000, None, 'H'),
    ('Saddam', '1088', 22000, 1, 'S'),
    ('Lotta', '4590', 28000, 2, 'H'),
    ('Olle', '2688', 20000, 3, 'S'),
    ('Maria', '2690', 25000, 4, 'C'),
    ('Ulrik', '2698', 26000, 3, 'C'),
    ('Petter', '2645', 22000, 3, 'C')
]

db = create_connection('./my_server/databases/employed.db')

cur = db.cursor()

cur.execute('''
    CREATE TABLE IF NOT EXISTS department(
        dept_id TEXT PRIMARY KEY,
        name TEXT
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS employed(
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        phone_nr TEXT,
        salary INTEGER,
        manager INTEGER REFERENCES employed(id),
        department TEXT REFERENCES department(dept_id)
    )
''')
cur.executemany('INSERT INTO department (dept_id, name) VALUES (?,?)', departments)

cur.executemany('INSERT INTO employed (name, phone_nr, salary, manager, department) VALUES (?,?,?,?,?)', employees)

db.commit()
db.close()