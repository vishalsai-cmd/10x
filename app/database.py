import sqlite3

def get_db_connection():
    conn = sqlite3.connect("trajectory.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trajectories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            wall_width REAL,
            wall_height REAL,
            trajectory TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON trajectories (timestamp)")
    conn.commit()
    conn.close()
