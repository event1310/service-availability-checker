from requests import RequestException
import requests as req
import argparse


class ConnectionInstance:
    def __init__(self):
        self.serverstate: str

    def test_connection(self, serveraddress: str):
        with req.Session() as currsession:
            try:
                currrequest = currsession.get(serveraddress)
                if 200 <= int(''.join(i for i in str(currrequest) if i.isdigit())) < 300:
                    self.serverstate = "up"

            except RequestException:
                self.serverstate = "down"

            print(f"{serveraddress} is {self.serverstate}")
            return self.serverstate


def process_sites(argv):
    retval = None
    instancesStatuses = {}
    for a, siteaddress in argv.items():
        if siteaddress:
            classInstance = ConnectionInstance()
            instancesStatuses[siteaddress] = classInstance.test_connection(siteaddress)
            if "down" in instancesStatuses.values():
                retval = "down"
            else:
                retval = "up"

    print(instancesStatuses)
    return retval


def parse_args():
    my_parser = argparse.ArgumentParser(description="Enter website to check", prefix_chars='-')
    my_parser.add_argument('site')
    my_parser.add_argument('-two',
                           action='store',
                           help='allows to pass more than one website to check')
    parsedargs = my_parser.parse_args()
    argv = vars(parsedargs)
    process_sites(argv)


def mock_single_argument_parser(firstsite):
    parsedargs = {'site': firstsite}
    return process_sites(parsedargs)


def mock_multiple_argument_parser(firstsite, secondsite):
    parsedargs = {'site': firstsite, 'two': secondsite}
    return process_sites(parsedargs)


if __name__ == '__main__':
    parse_args()
