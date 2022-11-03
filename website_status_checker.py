from concurrent.futures import ThreadPoolExecutor
import requests as req
import requests.exceptions
import validators


class ConnectionInstance:
    def __init__(self):
        self.websitestatus: str = "down"

    def send_get_request(self, url: str):
        try:
            with req.Session() as current_session:
                response = current_session.get(url, timeout=10)
                if 200 <= int(''.join(i for i in str(response) if i.isdigit())) < 300:
                    self.websitestatus = "up"
        except requests.exceptions.RequestException:
            self.websitestatus = "down"
        return self.websitestatus


def check_address_validity(url):
    url = url.strip("\n")
    valid_url = validators.url(url)
    valid_url_nohttp = validators.url("http://" + url)
    if valid_url:
        return url
    if valid_url_nohttp:
        return "http://" + url

def process_single_url(url):
    site_status = {}
    try:
        url = check_address_validity(url)
        if url:
            site_connection_instance = ConnectionInstance()
            site_status[url] = site_connection_instance.send_get_request(url)
            return {url: site_status[url]}

    except (ConnectionError, TimeoutError) as err:
        print(f"{err} invalid site format of site: {url}")


def process_multiple_urls(urls, urls_amount=0):
    sites_statuses = []
    try:
        with ThreadPoolExecutor(urls_amount) as executor:
            for checked_site in executor.map(process_single_url, urls, timeout=5):
                if checked_site:
                    sites_statuses.append(checked_site)
    except Exception:
        pass

    return sites_statuses
