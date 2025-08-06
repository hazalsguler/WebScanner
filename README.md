# WebScanner Tool

WebScanner is a Python-based command-line tool for performing basic web security assessments. It includes features such as port scanning, HTTP header inspection, directory brute-force scanning, SQL injection testing, and XSS detection.

Features:
- Port scanning (based on nmap)
- HTTP header fetching
- Directory brute-forcing using wordlists
- Basic SQL injection detection
- Basic XSS testing

Installation:
First, create and activate a virtual environment:
python -m venv venv
venv\Scripts\activate

Then install the tool locally:
pip install .

Once installed, you can run the tool globally from the terminal:
webscanner --help

Usage Examples:
Port scan:
webscanner --target example.com --scan-ports

Fetch HTTP headers:
webscanner --url http://example.com --get-headers

Directory brute-force scan:
webscanner --url http://example.com --wordlist wordlist.txt

Test for SQL injection:
webscanner --url "http://example.com/page.php?id=1" --sqli

Test for XSS vulnerabilities:
webscanner --url "http://example.com/page.php?q=" --xss

Project Structure:
webscanner/
├── __init__.py
├── core.py
├── cli.py
setup.py
pyproject.toml
README.md

Disclaimer: This tool is intended for educational and authorized testing purposes only. Unauthorized scanning or exploitation of systems may be illegal and unethical.
