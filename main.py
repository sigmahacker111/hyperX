import sys
from core.engine import run_hyperx_scan
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <url_or_file>")
        sys.exit(1)

    target_input = sys.argv[1]
    run_hyperx_scan(target_input)
