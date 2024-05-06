import requests
import time


def security_scan(target_url):
    # Make a request to OWASP ZAP API to scan the target URL
    scan_url = f"http://zap_api_endpoint/JSON/ascan/action/scan/?url={target_url}"
    response = requests.get(scan_url)
    scan_id = response.json()['scan']

    # Wait for the scan to finish
    status_url = f"http://zap_api_endpoint/JSON/ascan/view/status/?scanId={scan_id}"
    scan_status = 'running'
    while scan_status == 'running':
        time.sleep(10)
        response = requests.get(status_url)
        scan_status = response.json()['status']

    # Get scan results
    results_url = f"http://zap_api_endpoint/HTML/ascan/view/status/?scanId={scan_id}"
    response = requests.get(results_url)
    scan_results = response.text

    return scan_results

if __name__ == "__main__":
    target_url = "http://localhost:8501"
    scan_results = security_scan(target_url)
    print(scan_results)
