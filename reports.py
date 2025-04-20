#this did not belong in scanner... so i broke it out.
#LOVE YAML.. (actually only used it once at work, but its human-readable and easy to parse.

import yaml

def yaml_save(results, filename="scan_results.yaml"):
    try:
        with open(filename, 'a') as outfile:
            yaml.dump(results, outfile, default_flow_style=False)
        print(f"[+] Results saved to {filename}")
    except Exception as e:
        print(f"Error saving results: {e}")