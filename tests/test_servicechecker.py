import json
import checker

validtestaddress = "https://google.com"
validtestaddress2 = "http://facebook.com"
invalidtestaddress = "http://notworkingsite.notworkingsite"
invalidformattestaddress = "google.com"


def mock_single_argument_parser(firstsite: str) -> dict:
    return {firstsite: checker.process_site(firstsite)}


def mock_multiple_argument_parser(*args: str) -> dict:
    return {site: checker.process_site(site) for site in args}


def mock_process_sites_from_file(currserver: str, sitesstatuses: dict) -> None:
    currserver = currserver.strip('\n')
    if len(currserver) > 3:
        classinstance = checker.ConnectionInstance()
        sitesstatuses[currserver] = classinstance.test_connection(currserver)


def mock_file_argument_parser(mocktests: str) -> str:
    with open(mocktests, 'r') as txtfile:
        servers = txtfile.readlines()
        sitesstatuses = {}
        for server in servers:
            mock_process_sites_from_file(server, sitesstatuses)

        return mock_convert_to_JSON(sitesstatuses)


def mock_convert_to_JSON(sitesstatuses: dict) -> str:
    return json.dumps(sitesstatuses)


def test_single_valid_connection():
    output = mock_single_argument_parser(validtestaddress)
    assert output[validtestaddress] == "up"


def test_single_invalid_connection():
    output = mock_single_argument_parser(invalidtestaddress)
    assert output[invalidtestaddress] == "down"


def test_multiple_valid_two_connections():
    output = mock_multiple_argument_parser(validtestaddress, validtestaddress2)
    assert output[validtestaddress] == "up" and output[validtestaddress2] == "up"


def test_multiple_invalid_one_connection():
    output = mock_multiple_argument_parser(validtestaddress, invalidtestaddress)
    assert output[validtestaddress] == "up" and output[invalidtestaddress] == "down"


def test_multiple_invalid_one_input():
    output = mock_multiple_argument_parser(validtestaddress, invalidformattestaddress)
    assert output[validtestaddress] == "up" and output[invalidformattestaddress] == "invalid_input"


def test_connection_to_server_from_textfile():
    testservers = 'tests/mock_servers_file.txt'
    testserverstatus = str(mock_file_argument_parser(testservers))
    expectedteststatus = '{"https://google.com": "up",' \
                         ' "http://invalidsite.invalidsite": "down",' \
                         ' "123.999.92.255": "down"}'
    assert testserverstatus == expectedteststatus
