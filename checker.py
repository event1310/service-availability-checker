import argparse
from concurrent.futures import ThreadPoolExecutor
from requests import RequestException
import requests as req
import db.database as database

class ConnectionInstance:
    def __init__(self):
        self.serverstate: str = "down"

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

    try:
        site = check_site_validity(site)

        site_connection_instance = ConnectionInstance()
        instancesstatuses[site] = site_connection_instance.test_connection(site)
    #print(json.dumps(instancesstatuses))
        return {site: instancesstatuses[site]}

    except:
        raise ConnectionError("invalid site format")
def appendtoinstancestatus(server):
    try:
        site = check_site_validity(server)
        print(site)
        if site:
            instancestatus = {}
            if len(site) > 3:
                site_connection_instance = ConnectionInstance()
                instancestatus[site] = site_connection_instance.test_connection(site)
                print(instancestatus)
                return {site: instancestatus[site]}
        else:
            pass
    except TimeoutError:
        return

    except ConnectionError:
        pass
        print(f"invalid site format of site: {server}")

    #print(json.dumps(instancestatuses))
def process_sites_from_file(servers, txtfilelen=0):
    retval = []
    with ThreadPoolExecutor(txtfilelen) as executor:
        for result in executor.map(appendtoinstancestatus, servers, timeout=5):
            if result:
                retval.append(result)

    return retval

def check_site_validity(site):
    site = site.strip("\n")
    if site.endswith(".com") or site.endswith(".com"):

        if (site.startswith('http://') or site.startswith('https://')):
            return site
        else:
            newsite = "http://" + site
            return newsite
    else:
        pass

def alter_site_name(sitename):
    sitename = "http://" + sitename
    return sitename

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
    result = ""
    if parsedargs.l:
        sites = parsedargs.l
        sitesamount = len(sites)
        result = process_sites_from_file(sites, sitesamount)
        if parsedargs.db:
            db_instance = database.Database()
            db_instance.connect()
            db_instance.save_many(result)
            db_instance.close()

    elif parsedargs.f:
        txtfile = parsedargs.f
        lines = txtfile.readlines()
        txtfilelen = len(lines)
        result = process_sites_from_file(lines, txtfilelen)
        if parsedargs.db:
            db_instance = database.Database()
            db_instance.connect()
            db_instance.save_many(result)
            db_instance.close()


    elif parsedargs.site:
        result = process_site(parsedargs.site)
        if result is not None:
            if parsedargs.db:
                db_instance = database.Database()
                db_instance.connect()
                db_instance.save(result)
                db_instance.close()

    if result:
        print(result)
    return result

if __name__ == '__main__':
    parse_args()
