import sqlite3

def create_table():
    import sqlite3
    conn = sqlite3.connect("scenarios.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS scenarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        price_current REAL,
        marketing_current REAL,
        customers_current REAL,
        price_new REAL,
        marketing_new REAL,
        customers_new REAL,
        revenue_current REAL,
        revenue_new REAL,
        diff REAL
    )
    """)

    conn.commit()
    conn.close()

def insert_data(username, price_current, marketing_current, customers_current,
                price_new, marketing_new, customers_new,
                revenue_current, revenue_new, diff):

    import sqlite3
    conn = sqlite3.connect("scenarios.db")
    c = conn.cursor()

    c.execute("""
    INSERT INTO scenarios (
        username,
        price_current, marketing_current, customers_current,
        price_new, marketing_new, customers_new,
        revenue_current, revenue_new, diff
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        username,
        price_current, marketing_current, customers_current,
        price_new, marketing_new, customers_new,
        revenue_current, revenue_new, diff
    ))

    conn.commit()
    conn.close()

def get_data(username):
    import sqlite3
    conn = sqlite3.connect("scenarios.db")
    c = conn.cursor()

    c.execute("SELECT * FROM scenarios WHERE username = ?", (username,))
    rows = c.fetchall()

    conn.close()
    return rows

def create_user_table():
    import sqlite3
    conn = sqlite3.connect("scenarios.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()


    def add_user(username, password):
        import sqlite3
        conn = sqlite3.connect("scenarios.db")
        c = conn.cursor()

        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()


def login_user(username, password):
    import sqlite3
    conn = sqlite3.connect("scenarios.db")
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    data = c.fetchone()

    conn.close()
    return data   

def add_user(username, password):
    import sqlite3
    conn = sqlite3.connect("scenarios.db")
    c = conn.cursor()

    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))

    conn.commit()
    conn.close()

def login_user(username, password):
    import sqlite3
    conn = sqlite3.connect("scenarios.db")
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    data = c.fetchone()

    conn.close()
    return data