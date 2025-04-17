import os, json
THREADS = 50
OUTPUT_DIR = "outputs"

def load_targets(source):
    if os.path.isfile(source):
        with open(source) as f:
            return [x.strip() for x in f.readlines() if x.strip()]
    return [source]

def save_output(results):
    name = f"hyperx-scan-{len(results)}-{THREADS}.json"
    with open(os.path.join(OUTPUT_DIR, name), 'w') as f:
        json.dump(results, f, indent=2)
    print(f"[+] Results saved to outputs/{name}")