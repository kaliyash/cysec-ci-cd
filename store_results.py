import json
import sqlite3
from datetime import datetime

DB_PATH = 'scan_results.db'

def insert_scan(cursor, timestamp, tool, repo, commit_sha):
    cursor.execute('''
        INSERT INTO scans (timestamp, tool, repo, commit_sha)
        VALUES (?, ?, ?, ?)
    ''', (timestamp, tool, repo, commit_sha))
    return cursor.lastrowid

def insert_vulnerability(cursor, scan_id, cve_id, package_name, severity, description):
    cursor.execute('''
        INSERT INTO vulnerabilities (scan_id, cve_id, package_name, severity, description)
        VALUES (?, ?, ?, ?, ?)
    ''', (scan_id, cve_id, package_name, severity, description))

def parse_trivy_report(filepath, repo, commit_sha, conn):
    with open(filepath) as f:
        data = json.load(f)

    cursor = conn.cursor()
    timestamp = datetime.utcnow().isoformat()

    scan_id = insert_scan(cursor, timestamp, 'Trivy', repo, commit_sha)

    # Trivy JSON has 'Results' -> List -> 'Vulnerabilities' list
    for result in data.get('Results', []):
        vulnerabilities = result.get('Vulnerabilities', [])
        for vuln in vulnerabilities:
            cve_id = vuln.get('VulnerabilityID')
            package_name = vuln.get('PkgName')
            severity = vuln.get('Severity')
            description = vuln.get('Description', '')[:255]  # limit to 255 chars
            insert_vulnerability(cursor, scan_id, cve_id, package_name, severity, description)

    conn.commit()
    print(f"Inserted Trivy scan with {len(data.get('Results', []))} results.")

def parse_grype_report(filepath, repo, commit_sha, conn):
    with open(filepath) as f:
        data = json.load(f)

    cursor = conn.cursor()
    timestamp = datetime.utcnow().isoformat()

    scan_id = insert_scan(cursor, timestamp, 'Grype', repo, commit_sha)

    # Grype JSON vulnerabilities are under 'matches' list
    matches = data.get('matches', [])
    for match in matches:
        vuln = match.get('vulnerability', {})
        artifact = match.get('artifact', {})
        cve_id = vuln.get('id')
        package_name = artifact.get('name')
        severity = vuln.get('severity')
        description = vuln.get('description', '')[:255]
        insert_vulnerability(cursor, scan_id, cve_id, package_name, severity, description)

    conn.commit()
    print(f"Inserted Grype scan with {len(matches)} vulnerabilities.")

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 4:
        print("Usage: python store_results.py <tool> <repo> <commit_sha>")
        sys.exit(1)

    tool = sys.argv[1].lower()
    repo = sys.argv[2]
    commit_sha = sys.argv[3]

    conn = sqlite3.connect(DB_PATH)

    if tool == 'trivy':
        parse_trivy_report('trivy-report.json', repo, commit_sha, conn)
    elif tool == 'grype':
        parse_grype_report('grype-report.json', repo, commit_sha, conn)
    else:
        print("Unsupported tool. Use 'trivy' or 'grype'.")
        sys.exit(1)

    conn.close()
