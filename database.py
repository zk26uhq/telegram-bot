import sqlite3

conn = sqlite3.connect("payments.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS payments (
    telegram_id INTEGER,
    memo TEXT UNIQUE,
    paid INTEGER DEFAULT 0,
    delivered INTEGER DEFAULT 0
)
""")

conn.commit()

def add_user(telegram_id, memo):
    cursor.execute(
        "INSERT OR IGNORE INTO payments (telegram_id, memo) VALUES (?, ?)",
        (telegram_id, memo)
    )
    conn.commit()
