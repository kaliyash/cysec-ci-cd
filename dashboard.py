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
        SELECT tool, MAX(scan_date) as latest_scan, issue_count
        FROM scan_results
        GROUP BY tool
        ORDER BY latest_scan DESC
    """)
    results = cursor.fetchall()
    print(f"Fetched {len(results)} latest records from DB")
    conn.close()
    return results

@app.route('/')
def index():
    results = get_scan_results()
    print(f"Passing {len(results)} results to template")
    return render_template('dashboard.html', results=results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
