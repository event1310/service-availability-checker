from concurrent.futures import ThreadPoolExecutor
import validators
import requests as req


class ConnectionInstance:
    def __init__(self):
        self.websitestatus: str = "down"

    def send_GET_request(self, url: str):
        with req.Session() as current_session:
            try:
                response = current_session.get(url, timeout=10)
                if 200 <= int(''.join(i for i in str(response) if i.isdigit())) < 300:
                    self.websitestatus = "up"
            except:
                self.websitestatus = "down"
        return self.websitestatus


def check_address_validity(url):
    url = url.strip("\n")
    valid_url = validators.url(url)
    valid_url_nohttp = validators.url("http://" + url)
    if valid_url:
        return url
    elif valid_url_nohttp:
        return "http://" + url

def process_single_url(url):
    site_status = {}
    try:
        url = check_address_validity(url)
        if url:
            site_connection_instance = ConnectionInstance()
            site_status[url] = site_connection_instance.send_GET_request(url)
            return {url: site_status[url]}

    except ConnectionError or TimeoutError as err:
        pass
        print(f"{err} invalid site format of site: {url}")


def process_multiple_urls(urls, urls_amount=0):
    sites_statuses = []
    with ThreadPoolExecutor(urls_amount) as executor:
        try:
            for checked_site in executor.map(process_single_url, urls, timeout=10):
                if checked_site:
                    sites_statuses.append(checked_site)
        except Exception as ex:
            print(f"{checked_site} not responding: {ex}")
            pass
    return sites_statuses