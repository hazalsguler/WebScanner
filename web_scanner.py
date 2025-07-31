import argparse
import requests
import subprocess
from urllib.parse import urljoin

def port_scan(target):
    print(f"[+] Scanning ports on {target}...")
    try:
        result = subprocess.run([r"C:\Program Files (x86)\Nmap\nmap.exe", "-sS", "-Pn", "-T4", target],
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(result.stdout)
    except Exception as e:
        print(f"[-] Nmap failed: {e}")

def get_headers(url):
    print(f"[+] Fetching HTTP headers from {url}...")
    try:
        res = requests.get(url, timeout=5)
        print("[*] Response Headers:")
        for key, value in res.headers.items():
            print(f"{key}: {value}")
    except Exception as e:
        print(f"[-] Failed to get headers: {e}")

def dir_scan(url, wordlist):
    print(f"[+] Starting directory scan on {url} with {wordlist}...")
    try:
        with open(wordlist, 'r') as f:
            paths = f.read().splitlines()
            for path in paths:
                full_url = urljoin(url, path)
                try:
                    res = requests.get(full_url, timeout=3)
                    if res.status_code < 400:
                        print(f"[+] Found: {full_url} - {res.status_code}")
                except:
                    continue
    except FileNotFoundError:
        print("[-] Wordlist not found.")

def main():
    parser = argparse.ArgumentParser(description="Simple Web Scanner")
    parser.add_argument("-u", "--url", help="Target URL (http://example.com)", required=True)
    parser.add_argument("-t", "--target", help="Target IP/domain for port scan", required=True)
    parser.add_argument("-w", "--wordlist", help="Path to directory brute-force wordlist")
    
    args = parser.parse_args()
    
    port_scan(args.target)
    get_headers(args.url)
    
    if args.wordlist:
        dir_scan(args.url, args.wordlist)

if __name__ == "__main__":
    main()
