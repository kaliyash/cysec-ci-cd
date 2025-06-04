from flask import Flask, render_template
import sqlite3
import os

app = Flask(__name__)
DB_PATH = os.path.abspath("scan_results.db")  # absolute path for clarity

def get_scan_results():
    print(f"Opening DB at: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT scan_date, tool, issue_count
        FROM scan_results
        ORDER BY scan_date DESC
        LIMIT 50
    """)
    results = cursor.fetchall()
    print(f"Fetched {len(results)} records from DB")
    conn.close()
    return results

@app.route('/')
def index():
    results = get_scan_results()
    print(f"Passing {len(results)} results to template")
    return render_template('dashboard.html', results=results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
