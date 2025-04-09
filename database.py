import sqlite3
import time

conn = sqlite3.connect("posture_data.db", check_same_thread=False)

def init_db():
    conn.execute("""CREATE TABLE IF NOT EXISTS posture_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp REAL,
                    posture TEXT)""")
    conn.commit()

init_db()

def log_posture_event(status):
    conn.execute("INSERT INTO posture_events (timestamp, posture) VALUES (?, ?)", (time.time(), status))
    conn.commit()

def get_posture_history():
    import pandas as pd
    df = pd.read_sql_query("SELECT * FROM posture_events", conn)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    df['date'] = df['timestamp'].dt.date
    return df