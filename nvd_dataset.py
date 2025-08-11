import requests
from urllib.parse import quote
import csv
import time

DEVICE_CPES = [
    "cpe:2.3:a:microsoft:edge:-",
    "cpe:2.3:a:apache:log4j:2.14.1",
    "cpe:2.3:a:openssl:openssl:3.0.0",
    "cpe:2.3:a:oracle:mysql:8.0.0",
    "cpe:2.3:a:postgresql:postgresql:14.0",
    "cpe:2.3:a:mongodb:mongodb:5.0.0",
    "cpe:2.3:a:redis:redis:6.2.0",
    "cpe:2.3:a:nodejs:node:18.0.0",
    "cpe:2.3:a:python:python:3.10.0",
    "cpe:2.3:a:php:php:8.1.0",
    "cpe:2.3:a:jenkins:jenkins:2.346.0",
    "cpe:2.3:a:docker:docker_engine:20.10.0",
    "cpe:2.3:a:kubernetes:kubernetes:1.24.0",
    "cpe:2.3:a:elasticsearch:elasticsearch:8.3.0",
    "cpe:2.3:a:hashicorp:vault:1.11.0"
]

def fetch_cves(cpe, results_per_page=50):
    encoded_cpe = quote(cpe)
    url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?cpeName={encoded_cpe}&resultsPerPage={results_per_page}"
    try:
        resp = requests.get(url, timeout=20)
        resp.raise_for_status()
        return resp.json()
    except:
        return None

def extract_data(cpe, data):
    rows = []
    for vuln in data.get('vulnerabilities', []):
        cve = vuln['cve']
        metrics = cve.get('metrics', {})
        cvss = (
            metrics.get('cvssMetricV31', [{}])[0].get('cvssData', {}) or
            metrics.get('cvssMetricV30', [{}])[0].get('cvssData', {}) or
            metrics.get('cvssMetricV2', [{}])[0].get('cvssData', {})
        )
        rows.append({
            "CPE ID": cpe,
            "CVE ID": cve.get('id', ''),
            "CVSS": cvss.get('baseScore', ''),
            "Severity": cvss.get('baseSeverity', ''),
            "Published": cve.get('published', ''),
            "Last Modified": cve.get('lastModified', '')
        })
    return rows

def main():
    all_rows = []
    for idx, cpe in enumerate(DEVICE_CPES, 1):
        data = fetch_cves(cpe)
        if data:
            all_rows.extend(extract_data(cpe, data))
        if idx % 5 == 0:
            time.sleep(10)
        else:
            time.sleep(2)

    if all_rows:
        with open("cve_filtered.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["CPE ID", "CVE ID", "CVSS", "Severity", "Published", "Last Modified"])
            writer.writeheader()
            writer.writerows(all_rows)

if __name__ == "__main__":
    main()
