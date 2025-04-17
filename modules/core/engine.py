import os, threading, queue
from core.config import THREADS, OUTPUT_DIR, load_targets, save_output
from modules import tls_scan, js_extractor, tech_detect, misconfig_checker, security_headers
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urlparse

os.makedirs(OUTPUT_DIR, exist_ok=True)
url_queue = queue.Queue()
results = []

def scan_target(url):
    try:
        response = requests.get(url, timeout=10, verify=False, allow_redirects=True)
        parsed = urlparse(url)
        hostname = parsed.hostname

        html = response.text
        title = BeautifulSoup(html, 'html.parser').title
        result = {
            "url": url,
            "status": response.status_code,
            "title": title.string if title else "No Title",
            "tech": tech_detect.detect(response.headers, html),
            "headers": security_headers.check(response.headers),
            "js_links": js_extractor.extract(html, url),
            "misconfigs": misconfig_checker.check(url),
            "tls": tls_scan.fingerprint(hostname) if url.startswith("https") else {},
            "time": str(datetime.utcnow())
        }
        results.append(result)
        print(f"[+] {url} - {result['title']}")
    except Exception as e:
        print(f"[!] Error scanning {url}: {e}")

def run_hyperx_scan(source):
    targets = load_targets(source)
    for t in targets:
        if not t.startswith("http"): t = "http://" + t
        url_queue.put(t)

    threads = [threading.Thread(target=worker) for _ in range(THREADS)]
    for t in threads: t.start()
    for t in threads: t.join()

    save_output(results)

def worker():
    while not url_queue.empty():
        url = url_queue.get()
        scan_target(url)
        url_queue.task_done()