from dataclasses import dataclass
from requests import RequestException
import requests as req
import argparse


class ConnectionInstance:
    serverstate: str
    def test_connection(self, serveraddress):
            with req.Session() as currsession:
                try:
                    currrequest = currsession.get(serveraddress)
                    if 200 <= int(''.join(i for i in str(currrequest) if i.isdigit())) < 300:
                        self.serverstate = "up"
                except RequestException:
                    self.serverstate = "down"
            print(f"{serveraddress} is {self.serverstate}")

if __name__ == '__main__':
    my_parser = argparse.ArgumentParser(description="Enter website to check", prefix_chars='-')
    my_parser.add_argument('site')
    my_parser.add_argument('-two',
                           action='store',
                           help='allows to pass more than one website to check')
    parsedargs = my_parser.parse_args()

    if parsedargs.two is not None:
        server1 = ConnectionInstance()
        server2 = ConnectionInstance()
        server1.test_connection(parsedargs.site)
        server2.test_connection(parsedargs.two)
    else:
        server1 = ConnectionInstance()
        server1.test_connection(parsedargs.site)

