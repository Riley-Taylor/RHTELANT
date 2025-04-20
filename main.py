#Initial Commit!

from colorama import *
import argparse
from scanner import *
from reports import *

init(autoreset=True) #reset color values after each print.

def parser_args():
    parser = argparse.ArgumentParser(description="RHTELANT - RHT'S ELA Network Tool")
    parser.add_argument("--target", required=True, help="Target IP address")
    parser.add_argument("--port", required=True, help="Target port(s)")
    parser.add_argument("-v", action="store_true",required=False, help="verbose")

    return parser.parse_args()

def main():
    arguments = parser_args()
    print(Fore.CYAN + f"\n[*] Starting scan on {arguments.target}")
    scan_results,scan_results_banner = run_scanner(arguments.target, arguments.port)


    print(Fore.GREEN + "\n[+] Scan complete.")
    for host, info in scan_results.items():
        print(Fore.YELLOW + f"\nHost: {host}")
        print(Fore.MAGENTA + "Open Ports:", info['open_ports'])

    print(Fore.GREEN + "\n Saving to YAML file...")
    yaml_save(scan_results_banner)
if __name__ == "__main__":
    main()