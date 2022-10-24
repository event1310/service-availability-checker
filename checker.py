import argparse
import json
import requests as req
from requests import RequestException


class ConnectionInstance:
    def __init__(self):
        serverstate: str

    def test_connection(self, serveraddress: str):
        with req.Session() as currsession:
            try:
                currrequest = currsession.get(serveraddress)
                if 200 <= int(''.join(i for i in str(currrequest) if i.isdigit())) < 300:
                    self.serverstate = "up"

            except RequestException:
                self.serverstate = "down"

            #print(f"{serveraddress} is {self.serverstate}")
            return self.serverstate


def process_site(argv):
    retval = None
    instancesstatuses = {}
    for a, val in argv.items():
        if val:
            classInstance = ConnectionInstance()
            instancesstatuses[val] = classInstance.test_connection(val)
            if "down" in instancesstatuses.values():
                retval = "down"
            else:
                retval = "up"

    instancesstatuses = json.dumps(instancesstatuses)
    print(instancesstatuses)
    return retval


def process_sites_from_file(servers):
    instancestatuses = []
    for server in servers:
        instancestatus = {}
        server = server.strip('\n')
        if len(server) > 3:
            classInstance = ConnectionInstance()
            instancestatus[server] = classInstance.test_connection(server)
            instancestatuses.append(instancestatus)

    instancestatuses = json.dumps(instancestatuses)
    print(instancestatuses)



def parse_args():
    my_parser = argparse.ArgumentParser(description="Enter website to check", prefix_chars='-')
    my_parser.add_argument('-site',
                           action='store')
    my_parser.add_argument('-two',
                           action='store',
                           help='allows to pass more than one website to check')
    my_parser.add_argument('-f',
                           type=argparse.FileType('r'))
    parsedargs = my_parser.parse_args()
    argv = vars(parsedargs)
    if parsedargs.f is not None:
        txtfile = parsedargs.f
        lines = txtfile.readlines()
        process_sites_from_file(lines)

    else:
        process_site(argv)


if __name__ == '__main__':
    parse_args()
