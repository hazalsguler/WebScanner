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

def test_sqli(url):
    print(f"[+] Testing SQL Injection on {url}...")
    payloads = ["'", "' OR '1'='1", "\" OR \"1\"=\"1", "'--", "\"--", "'#", "\"#"]
    found = False

    for payload in payloads:
        test_url = url + payload
        try:
            res = requests.get(test_url, timeout=5)
            if any(error in res.text.lower() for error in ["sql", "syntax", "mysql", "query", "warning"]):
                print(f"[!] Potential SQLi vulnerability detected with payload: {payload}")
                found = True
        except:
            continue

    if not found:
        print("[*] No obvious SQLi vulnerability detected.")

def test_xss(url):
    print(f"[+] Testing XSS on {url}...")
    payloads = [
        "<script>alert(1)</script>",
        "\" onmouseover=alert(1)",
        "<img src=x onerror=alert(1)>",
        "<svg onload=alert(1)>",
        "<body onload=alert(1)>"
    ]
    found = False

    for payload in payloads:
        test_url = url + payload
        try:
            res = requests.get(test_url, timeout=5)
            if payload in res.text:
                print(f"[!] Potential XSS vulnerability detected with payload: {payload}")
                found = True
        except:
            continue

    if not found:
        print("[*] No obvious XSS vulnerability detected.")

def main():
    parser = argparse.ArgumentParser(description="Simple Web Scanner with optional SQLi and XSS testing")
    parser.add_argument("-u", "--url", help="Target URL (e.g., http://example.com/page.php?id=1)", required=True)
    parser.add_argument("-t", "--target", help="Target IP/domain for port scan", required=True)
    parser.add_argument("-w", "--wordlist", help="Path to directory brute-force wordlist")
    parser.add_argument("--sqli", action="store_true", help="Enable SQL Injection testing on the URL")
    parser.add_argument("--xss", action="store_true", help="Enable XSS testing on the URL")

    args = parser.parse_args()

    port_scan(args.target)
    get_headers(args.url)

    if args.wordlist:
        dir_scan(args.url, args.wordlist)

    if args.sqli:
        test_sqli(args.url)

    if args.xss:
        test_xss(args.url)

if __name__ == "__main__":
    main()
