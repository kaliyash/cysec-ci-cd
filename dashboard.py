from flask import Flask, render_template
import sqlite3

app = Flask(__name__)
DB_PATH = "scan_results.db"

def get_scan_results():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT scan_date, tool, issue_count
        FROM scan_results
        ORDER BY scan_date DESC
        LIMIT 50
    """)
    results = cursor.fetchall()
    conn.close()
    return results

@app.route('/')
def index():
    results = get_scan_results()
    return render_template('dashboard.html', results=results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
