import sqlite3

def init_db():
    conn = sqlite3.connect("users.db", check_same_thread=False)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS drones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT
        )
    """)
    
    conn.commit()
    conn.close()


def register_user(username, password):
    try:
        conn = sqlite3.connect("users.db", check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def check_user(username, password):
    conn = sqlite3.connect("users.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None

def add_drone(name, description):
    """Yeni dronu bazaya əlavə edir"""
    conn = sqlite3.connect("users.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO drones (name, description) VALUES (?, ?)", (name, description))
    conn.commit()
    conn.close()

def get_drones():
    """Bütün dronları siyahı şəklində qaytarır"""
    conn = sqlite3.connect("users.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT name, description FROM drones")
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_drone(name):
    """Dronu adına görə bazadan silir"""
    conn = sqlite3.connect("users.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM drones WHERE name = ?", (name,))
    conn.commit()
    conn.close()

def update_drone(old_name, new_name, new_desc):
    """Dronun məlumatlarını köhnə adına əsasən yeniləyir"""
    conn = sqlite3.connect("users.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE drones SET name = ?, description = ? WHERE name = ?",
        (new_name, new_desc, old_name)
    )
    conn.commit()
    conn.close()