# fetch_latest_news.py
import mysql.connector

def get_latest_news(limit=10):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="db_cisscrapper"
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM events ORDER BY data_time DESC LIMIT %s", (limit,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result
