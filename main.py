#Initial Commit!

from colorama import *
import argparse
from scanner import *
from yaml import *

init(autoreset=True) #reset color values after each print.

def parser_args():
    parser = argparse.ArgumentParser(description="RHTELANT - RHT'S ELA Network Tool")
    parser.add_argument("--target", required=True, help="Target IP address")
    parser.add_argument("--port", required=True, help="Target port(s)")
    return parser.parse_args()

def main():
    arguments = parser_args()
    print(Fore.CYAN + f"\n[*] Starting scan on {arguments.target}")
    scan_results = run_scanner(arguments.target, arguments.port)


    print(Fore.GREEN + "\n[+] Scan complete.")
    for host, info in scan_results.items():
        print(Fore.YELLOW + f"\nHost: {host}")
        print(Fore.MAGENTA + "Open Ports:", info['open_ports'])

if __name__ == "__main__":
    main()