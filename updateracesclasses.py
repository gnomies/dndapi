def create_tables():
    c.execute('''
        CREATE TABLE IF NOT EXISTS races
        (id INTEGER PRIMARY KEY, race TEXT)
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS classes
        (id INTEGER PRIMARY_KEY, class TEXT)
    ''')

    conn.commit()
