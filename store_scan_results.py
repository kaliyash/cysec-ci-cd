import sqlite3
import os

DB_PATH = os.path.abspath("scan_results.db")

def show_scan_results():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT scan_date, tool, issue_count FROM scan_results ORDER BY scan_date DESC")
    rows = c.fetchall()
    for row in rows:
        print(f"Date: {row[0]}, Tool: {row[1]}, Issues: {row[2]}")
    conn.close()

if __name__ == "__main__":
    show_scan_results()
