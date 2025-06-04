import json
import sqlite3
import os
from datetime import datetime, timezone

# Use absolute path to avoid confusion
DB_PATH = os.path.abspath("scan_results.db")

def load_json(path):
    if os.path.exists(path):
        with open(path, 'r') as f:
            content = f.read().strip()
            if not content:
                print(f"[WARN] {path} is empty.")
                return None
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                print(f"[ERROR] Failed to parse JSON from {path}")
                return None
    print(f"[WARN] {path} does not exist.")
    return None

def count_bandit_issues(data):
    count = len(data.get('results', [])) if data else 0
    print(f"[DEBUG] Bandit issue count: {count}")
    return count

def count_semgrep_issues(data):
    count = len(data.get('results', [])) if data else 0
    print(f"[DEBUG] Semgrep issue count: {count}")
    return count

def count_trivy_issues(data):
    if not data or 'Results' not in data:
        print(f"[DEBUG] Trivy data is empty or malformed.")
        return 0
    count = 0
    for result in data['Results']:
        vulns = result.get('Vulnerabilities', [])
        count += len(vulns)
    print(f"[DEBUG] Trivy issue count: {count}")
    return count

def count_grype_issues(data):
    if not data or 'matches' not in data:
        print(f"[DEBUG] Grype data is empty or malformed.")
        return 0
    count = len(data['matches'])
    print(f"[DEBUG] Grype issue count: {count}")
    return count

def init_db():
    print(f"Using DB path: {DB_PATH}")
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
    print(f"[INFO] Inserting result: {tool} = {count}")
    c = conn.cursor()
    c.execute('INSERT INTO scan_results (scan_date, tool, issue_count) VALUES (?, ?, ?)',
              (datetime.now(timezone.utc).isoformat(), tool, count))
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
    print("[SUCCESS] Scan results stored in SQLite database.")

if __name__ == "__main__":
    main()
