import json
import checker

validtestaddress = "https://google.com"
validtestaddress2 = "http://facebook.com"
invalidtestaddress = "http://notworkingsite.notworkingsite"
invalidformattestaddress = "google.com"


def mock_single_argument_parser(firstsite: str):
    parsedargs = {'site': firstsite}
    return checker.process_site(parsedargs['site'])


def mock_multiple_argument_parser(firstsite: str, secondsite: str):
    parsedargs = {'site': firstsite, 'two': secondsite}
    return checker.process_site(parsedargs['site']) and checker.process_sites_from_file(parsedargs['two'])


def mock_process_sites_from_file(currserver: str, sitesstatuses: dict):
    currserver = currserver.strip('\n')
    if len(currserver) > 3:
        classinstance = checker.ConnectionInstance()
        sitesstatuses[currserver] = classinstance.test_connection(currserver)


def mock_file_argument_parser(mocktests: str):
    with open(mocktests, 'r') as txtfile:
        servers = txtfile.readlines()
        sitesstatuses = {}
        for server in servers:
            mock_process_sites_from_file(server, sitesstatuses)

        return mock_convert_to_JSON(sitesstatuses)

def mock_convert_to_JSON(sitesstatuses: dict):
    return json.dumps(sitesstatuses)


def test_single_valid_connection():
    serversstatus = mock_single_argument_parser(validtestaddress)
    assert serversstatus[validtestaddress] == "up"


def test_single_invalid_connection():
    serversstatus = mock_single_argument_parser(invalidtestaddress)
    assert serversstatus[invalidtestaddress] == "down"


def test_multiple_valid_two_connections():
    serversstatus = mock_multiple_argument_parser(validtestaddress, validtestaddress2)
    assert serversstatus[validtestaddress] == "up" and serversstatus[validtestaddress2] == "up"


def test_multiple_invalid_one_connection():
    serversstatus = mock_multiple_argument_parser(validtestaddress, invalidtestaddress)
    assert serversstatus[validtestaddress] == "up" and serversstatus[invalidtestaddress] == "down"

def test_multiple_invalid_one_input():
    serversstatus = mock_multiple_argument_parser(validtestaddress, invalidformattestaddress)
    assert serversstatus[validtestaddress] == "up" and serversstatus[invalidformattestaddress] == "invalid_input"

def test_connection_to_server_from_textfile():
    testservers = 'tests/mock_servers_file.txt'
    testserverstatus = str(mock_file_argument_parser(testservers))
    expectedteststatus = '{"https://google.com": "up",' \
                         ' "http://invalidsite.invalidsite": "down",' \
                         ' "123.999.92.255": "down"}'
    assert testserverstatus == expectedteststatus
