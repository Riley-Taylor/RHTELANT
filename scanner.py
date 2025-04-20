# scanner.py
import ipaddress
import socket
import subprocess
from concurrent.futures import ThreadPoolExecutor
import platform
import vulners
import requests


def ping_host(ip):
    '''
    Sends 1 ping packet to an ip address, Waits 1 second, if there's a reply return ip.
    :param ip:
    :return: IP address / Nothing
    '''
    try:
        system = platform.system().lower()

        # Adjust ping flags based on OS
        if system == "windows":
            result = subprocess.run(['ping', '-n', '1', str(ip)], stdout=subprocess.DEVNULL)
        else:
            result = subprocess.run(['ping', '-c', '1', '-W', '1', str(ip)], stdout=subprocess.DEVNULL)
        return str(ip) if result.returncode == 0 else None
    except:
        return None

def banner_snatcher(ip,port):
    '''
 Grabs a banner up to 512 bytes big. (arbitrary size but reasonable!)
    :param ip:
    :param port:
    :return:    banner information
    '''
    try:
        sock = socket.socket() #make socket
        sock.settimeout(1)
        sock.connect((ip, port)) #try to connect
        banner = sock.recv(1024).decode()
        return banner if banner else "Banner not shared!"
    except Exception:
        return "No banner"

#def cve_match(banner): #Want to use Vulners to search things based on banner info..
#This would require HEAVY Banner sanitization! otherwise you get ai slop from vulners
#    '''
#    uses banner information to try and match to a CVE.
#    :param banner:
#    :return:
#    '''
#    vulners_api =vulners.VulnersApi("ECX21PLW5TIPKDSJU92WJZOG2A6Y508JERC7X9QBWZ4OBNU7DJWVP7MONM2DKKJ9")
#    try:
#        vulnerables = vulners_api.search_cpe

def scan_port(ip, port):
    '''
    Tries to connect to port, if open 0, if anything else it is closed.
    '''
    try:
        sock = socket.socket() #make socket
        sock.settimeout(1)
        result = sock.connect_ex((ip, port)) #try to connect
        sock.close()
        if result == 0:
            return port #woo port is open
    except:
        pass
    return None # :c port is closed


def run_scanner(target_subnet, port_range):
    ip_net = ipaddress.ip_network(target_subnet, strict=False)
    print(f"[*] Scanning subnet: {target_subnet}")

    open_hosts = []
    with ThreadPoolExecutor(max_workers=100) as executor: #Threading is cool, makes this a lot faster.
        results = executor.map(ping_host, ip_net.hosts())
        open_hosts = list(filter(None, results))

    print(f"[+] Found {len(open_hosts)} live hosts.")

    port_start, port_end = map(int, port_range.split('-')) #map to a bunch of integers split by '-'
    ports = list(range(port_start, port_end + 1))
    final_results = {}
    final_results_banner = {}

    for ip in open_hosts:
        print(f"\n[~] Scanning {ip}...")
        open_ports = []
        open_ports_banner = []

        with ThreadPoolExecutor(max_workers=50) as executor: #oooh threads! so cool!
            results = executor.map(lambda p: scan_port(ip, p), ports) #scans ports

        for port in results:
            if port:
                banner = banner_snatcher(ip, port)

               # print(f"  [OPEN] {ip}:{port}")   #Printing looked tacky!
                open_ports.append(port)
                open_ports_banner.append({
                    "port": port,
                    "banner": banner
                })
        final_results[ip] = {
            "open_ports": open_ports
        }
        final_results_banner[ip] = { #messy.. but i want 2 separate outputs. CL & YAML
            "open_ports": open_ports_banner
        }

    return final_results,final_results_banner
