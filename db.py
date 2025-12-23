import sqlite3

def get_connection():
    return sqlite3.connect(
        "candidates.db",
        timeout=10,
        check_same_thread=False
    )


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phone TEXT,
            experience TEXT,
            role TEXT,
            location TEXT,
            tech_stack TEXT,
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_id INTEGER,
            question TEXT,
            answer TEXT,
            FOREIGN KEY(candidate_id) REFERENCES candidates(id)
        )
    """)

    conn.commit()
    conn.close()
