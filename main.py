#Initial Commit!

from colorama import *
import argparse
from yaml import *

init(autoreset=True) #reset color values after each print.

def parser_args():
    parser = argparse.ArgumentParser(description="RHTELANT - RHT'S ELA Network Tool")
    parser.add_argument("--target", required=True, help="Target IP address")
    parser.add_argument("--port", required=True, help="Target port")
    return parser.parse_args()

def main():
    arguments = parser_args()
    print(Fore.CYAN + "Hello!")



if __name__ == "__main__":
    main()