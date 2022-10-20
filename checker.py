from dataclasses import dataclass
import requests as req
from requests import RequestException


@dataclass
class ConnectionInstance:
    address: str

    def check_site(self):
        try:
            resp = req.get(self.address)
            respcode = ''.join(i for i in str(resp) if i.isdigit())
            print(respcode)
            if respcode == "200":
                print(f"Site {self.address} is up")
            return resp
        except RequestException:
            print("site is not working")

if __name__ == '__main__':
    conn1 = ConnectionInstance("https://www.gdadoogle.com")
    conn1.check_site()
