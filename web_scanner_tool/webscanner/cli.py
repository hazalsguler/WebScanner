import argparse
from webscanner.core import port_scan, get_headers, dir_scan, test_sqli, test_xss

def main():
    parser = argparse.ArgumentParser(description="🛡 Webscanner CLI Tool")

    parser.add_argument("--url", help="Target URL (e.g. http://example.com)")
    parser.add_argument("--target", help="Target IP or domain for port scan")
    parser.add_argument("--wordlist", help="Path to wordlist for directory brute-force")
    parser.add_argument("--scan-ports", action="store_true", help="Run port scan")
    parser.add_argument("--get-headers", action="store_true", help="Get HTTP headers")
    parser.add_argument("--sqli", action="store_true", help="Test for SQL Injection")
    parser.add_argument("--xss", action="store_true", help="Test for XSS")

    args = parser.parse_args()

    if args.scan_ports and args.target:
        port_scan(args.target)

    if args.get_headers and args.url:
        get_headers(args.url)

    if args.wordlist and args.url:
        dir_scan(args.url, args.wordlist)

    if args.sqli and args.url:
        test_sqli(args.url)

    if args.xss and args.url:
        test_xss(args.url)

    if not any([args.scan_ports, args.get_headers, args.wordlist, args.sqli, args.xss]):
        print("✅ Webscanner CLI başarıyla çalışıyor!")
