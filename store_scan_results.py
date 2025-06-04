import json
import sqlite3
import os
from datetime import timezone
(datetime.now(timezone.utc).isoformat(), tool, count)

DB_PATH = "scan_results.db"

def load_json(path):
    if os.path.exists(path):
        with open(path, 'r') as f:
            content = f.read().strip()
            if not content:
                return None
            return json.loads(content)
    return None

def count_bandit_issues(data):
    return len(data.get('results', [])) if data else 0

def count_semgrep_issues(data):
    return len(data.get('results', [])) if data else 0

def count_trivy_issues(data):
    if not data or 'Results' not in data:
        return 0
    count = 0
    for result in data['Results']:
        count += len(result.get('Vulnerabilities', []))
    return count

def count_grype_issues(data):
    if not data or 'matches' not in data:
        return 0
    return len(data['matches'])

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS scan_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scan_date TEXT,
            tool TEXT,
            issue_count INTEGER
        )
    ''')
    conn.commit()
    return conn

def insert_result(conn, tool, count):
    c = conn.cursor()
    c.execute('INSERT INTO scan_results (scan_date, tool, issue_count) VALUES (?, ?, ?)',
              (datetime.utcnow().isoformat(), tool, count))
    conn.commit()

def main():
    bandit_data = load_json("scans/code/bandit.json")
    semgrep_data = load_json("scans/code/semgrep.json")
    trivy_data = load_json("scans/image/trivy.json")
    grype_data = load_json("scans/image/grype.json")

    conn = init_db()

    insert_result(conn, "bandit", count_bandit_issues(bandit_data))
    insert_result(conn, "semgrep", count_semgrep_issues(semgrep_data))
    insert_result(conn, "trivy", count_trivy_issues(trivy_data))
    insert_result(conn, "grype", count_grype_issues(grype_data))

    conn.close()
    print("Scan results stored in SQLite database.")

if __name__ == "__main__":
    main()

