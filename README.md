# Cybersecurity CI/CD Security Automation Framework

## Overview

This project establishes a CI/CD security automation framework using GitHub Actions, integrating multiple static and container vulnerability scanning tools. It stores the scan results in a persistent SQLite database, sends Discord alerts upon detection of vulnerabilities, and presents a web-based dashboard using Flask for visualization.

## Project Objectives

- Automate code and container security scanning during every code push or pull request.
- Store scan results persistently for audit and historical analysis.
- Alert security teams in real-time through Discord.
- Provide a web interface for inspecting scan results using a dashboard.

## Tools and Technologies

- **GitHub Actions** for continuous integration workflow.
- **Bandit** for Python static code analysis.
- **Semgrep** for multi-language code analysis.
- **Trivy** for container image vulnerability scanning.
- **Grype** for deep container vulnerability detection.
- **SQLite** for persistent scan result storage.
- **Flask** for serving a web-based dashboard.
- **Discord Webhooks** for alerting.

## Folder Structure
cysec-ci-cd/
├── .github/
│   └── workflows/
│       └── security_full.yml         # GitHub Actions CI workflow
├── scans/                            # Stores raw scan outputs from tools
│   ├── code/                         # Bandit and Semgrep outputs
│   └── image/                        # Trivy and Grype outputs
├── templates/
│   └── dashboard.html                # HTML template for Flask dashboard
├── dashboard.py                      # Flask app to visualize scan results
├── scan_results.db                   # SQLite database (auto-generated)
├── store_scan_results.py            # Script to insert scan results into DB
├── requirements.txt                  # Python dependencies list
├── README.md                         # Project documentation

## Environment Setup

1. Install required Python dependencies:
   ```bash
      pip install bandit semgrep requests flask
   
2. Install and authenticate Git:
   Install Git CLI.
   Create a repository named cysec-ci-cd on GitHub.
   Create a GitHub Personal Access Token (PAT) and add it to the repo secrets as CYBERSEC_CI_CD_TOKEN.

3. Set up Discord alerts:
   Create a Discord webhook URL.
   Add it as a GitHub secret named DISCORD_WEBHOOK.


## Workflow Execution

1. Commit and push changes to GitHub:
   ```bash
   git add .github/workflows/security_full.yml
   git commit -m "Add complete security scanning CI workflow with alerts"
   git push origin master

2. On each push or pull request, GitHub Actions will:
   Run Bandit and Semgrep on source code.
   Run Trivy and Grype on a Docker image built from the repository.
   Store all scan results as JSON files in the scans/ directory.
   Insert extracted issue counts into scan_results.db.
   Upload the scan database as an artifact.
   Trigger a Discord alert if any issues are found.



3. To manually insert scan results into the database:
   ```bash
   python3 store_scan_results.py
  

4. To launch the Flask dashboard:
   ```bash
   python3 dashboard.py

Once running, access the dashboard at: http://localhost:5000


## Dashboard
The Flask dashboard reads from scan_results.db and displays the latest issue count for each tool in a tabular format. The dashboard template is located at templates/dashboard.html.




## Discord Alert Logic
If scan result JSON files contain any vulnerabilities, a formatted message is sent to the Discord webhook. If no vulnerabilities are found, no alert is sent.




## License
This project is for educational and demonstration purposes only.

## Contributing
We welcome contributions to enhance and expand this CI/CD Security Automation Framework.
