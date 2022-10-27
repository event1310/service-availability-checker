import argparse
import json
import requests as req
from requests import RequestException
import db.database as database
from concurrent.futures import ThreadPoolExecutor


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

            return self.serverstate


def process_site(site):
    instancesstatuses = {}
    #print(site)
    if site.startswith('http://') or site.startswith('https://'):
        classInstance = ConnectionInstance()
        instancesstatuses[site] = classInstance.test_connection(site)

    #print(json.dumps(instancesstatuses))
    return instancesstatuses[site]

def appendtoinstancestatus(server):
    if check_site_validity(server):
        instancestatus = {}
        server = server.strip('\n')
        if len(server) > 3:
            classInstance = ConnectionInstance()
            instancestatus[server] = classInstance.test_connection(server)
            return {server: instancestatus[server]}

    #print(json.dumps(instancestatuses))
def process_sites_from_file(servers, txtfilelen = 0):
    retval = []
    with ThreadPoolExecutor(txtfilelen) as executor:
        for result in executor.map(appendtoinstancestatus, servers):
            if result:
                retval.append(result)

    return retval

def check_site_validity(site):
    if site.startswith('http://') or site.startswith('https://'):
        return True
    else:
        print(f"invalid site format for {site}")
        #print(f"{site} is not a valid site starting with https:// or http://")
        return False


def parse_args():
    my_parser = argparse.ArgumentParser(description="Enter website to check", prefix_chars='-')
    my_parser.add_argument('-site',
                           action='store')
    my_parser.add_argument('-l',
                           nargs='*',
                           action='store',
                           help='allows to pass more than one website to check')
    my_parser.add_argument('-f',
                           type=argparse.FileType('r'))
    my_parser.add_argument('-db',
                           action='store_true',
                           help='store returned values in db')
    parsedargs = my_parser.parse_args()
    argv = vars(parsedargs)
    if parsedargs.l:
        sites = parsedargs.l
        sitesamount = len(sites)
        result = process_sites_from_file(sites, sitesamount)
        print(result)
        if parsedargs.db:
            db = database.Database()
            db.connect()
            db.save_many(result)
            db.close()

    elif parsedargs.f:
        txtfile = parsedargs.f
        lines = txtfile.readlines()
        txtfilelen = len(lines)
        result = process_sites_from_file(lines, txtfilelen)
        print(result)
        if parsedargs.db:
            db = database.Database()
            db.connect()
            db.save_many(result)
            db.close()

    elif parsedargs.site:
        result = {parsedargs.site: process_site(parsedargs.site)}
        print(result)
        if parsedargs.db:
            db = database.Database()
            db.connect()
            db.save(result)
            db.close()


if __name__ == '__main__':
    parse_args()
