import re
import requests
from bs4 import BeautifulSoup
import validators

# Check if URL is valid
def is_valid_url(url):
    return validators.url(url)

# Check if URL contains suspicious keywords
def has_suspicious_keywords(url):
    keywords = ["login", "verify", "update", "free", "bonus", "secure", "bank"]
    return any(word in url for word in keywords)

# Check if URL is too long
def is_long_url(url):
    return len(url) > 75

# Check for IP-based URLs
def is_ip_address(url):
    return re.match(r"https?://\d+\.\d+\.\d+\.\d+", url) is not None

# Check HTML content
def scan_html(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.string if soup.title else ""
        if "login" in title.lower() or "verify" in title.lower():
            return True
    except:
        return False
    return False


def check_url(url):
    results = []

    if not is_valid_url(url):
        results.append("❌ Invalid URL format")

    if has_suspicious_keywords(url):
        results.append("⚠️ Suspicious keywords found")

    if is_long_url(url):
        results.append("⚠️ Very long URL")

    if is_ip_address(url):
        results.append("⚠️ URL uses IP instead of domain")

    if scan_html(url):
        results.append("⚠️ Suspicious HTML words detected")

    if not results:
        return "✅ URL appears safe"
    else:
        return "\n".join(results)


if __name__ == "__main__":
    url = input("Enter URL to scan: ")
    print("\n--- SCAN RESULTS ---")
    print(check_url(url))
