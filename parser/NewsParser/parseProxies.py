import requests
import re
from bs4 import BeautifulSoup

def get_my_ip():
    """Get the public IP address."""
    try:
        response = requests.get('https://api.ipify.org?format=text')
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error: {e}")
        return None

def get_proxies_from_spys_me(url="https://spys.me/proxy.txt"):
    """Scrape proxies from spys.me."""
    response = requests.get(url)
    response.raise_for_status()
    return re.findall(r"[0-9]+(?:\\.[0-9]+){3}:[0-9]+", response.text)

def get_proxies_from_free_proxy_list(url="https://free-proxy-list.net/"):
    """Scrape proxies from free-proxy-list.net."""
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")
    proxies = []

    for row in soup.select(".fpl-list .table tbody tr"):
        columns = row.find_all("td")
        if len(columns) >= 2:
            ip = columns[0].get_text(strip=True)
            port = columns[1].get_text(strip=True)
            proxies.append(f"{ip}:{port}")
    return proxies

def add_actual_ip_every_second_line(proxies, actual_ip=None):
    """Insert the actual IP every second line."""
    if actual_ip is None:
        actual_ip = get_my_ip() + ":8080" if get_my_ip() else "127.0.0.1:8080"
    
    result = []
    for i, proxy in enumerate(proxies, start=1):
        result.append(proxy)
        if i % 2 == 0:  # Every second line
            result.append(actual_ip)
    return result

def save_proxies_to_file(proxies, filename="proxies_list.txt"):
    """Save the proxies to a file."""
    with open(filename, "w") as file:
        for proxy in proxies:
            file.write(proxy + "\n")

def main():
    """Main function to get proxies and save them."""
    proxies = get_proxies_from_spys_me() + get_proxies_from_free_proxy_list()
    proxies_with_actual_ip = add_actual_ip_every_second_line(proxies)
    save_proxies_to_file(proxies_with_actual_ip)

if __name__ == "__main__":
    main()
