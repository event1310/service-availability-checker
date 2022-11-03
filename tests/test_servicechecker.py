import pytest
import website_status_checker
from website_status_checker import process_single_url, check_address_validity

validtestaddress = "https://google.com"
validtestaddress2 = "http://facebook.com"
invalidtestaddress = "http://notworkingsite.notworkingsite"
invalidformattestaddress = "awdadad"


def mock_single_argument_parser(firstsite: str) -> dict:
    return process_single_url(firstsite)


def mock_multiple_argument_parser(*args: str) -> dict:
    return {site: process_single_url(site) for site in args}


def mock_process_sites_from_file(currserver: str) -> dict:
    validserver = check_address_validity(currserver.strip('\n'))
    if len(currserver) > 3 and validserver:
        classinstance = website_status_checker.ConnectionInstance()
        return {currserver: classinstance.send_GET_request(validserver)}


def mock_file_argument_parser(mocktests: str) -> list:
    retval = []
    with open(mocktests, 'r') as txtfile:
        servers = txtfile.readlines()
        try:
            for server in servers:
                server = website_status_checker.check_address_validity(server)
                retval.append(mock_process_sites_from_file(server))

        except:
            pass
        return retval


@pytest.mark.websitestatus
def test_single_valid_url():
    output = mock_single_argument_parser(validtestaddress)
    assert output == {validtestaddress: 'up'}

@pytest.mark.websitestatus
def test_single_invalid_url():
    output = mock_single_argument_parser(invalidtestaddress)
    assert output == {invalidtestaddress: 'down'}

@pytest.mark.websitestatus
def test_multiple_valid_two_url():
    output = mock_multiple_argument_parser(validtestaddress, validtestaddress2)
    assert output[validtestaddress] == {validtestaddress: 'up'} \
           and output[validtestaddress2] == {validtestaddress2: 'up'}

@pytest.mark.websitestatus
def test_multiple_one_invalid_url():
    output = mock_multiple_argument_parser(validtestaddress, invalidtestaddress)
    assert output[validtestaddress] == {validtestaddress: 'up'} \
           and output[invalidtestaddress] == {invalidtestaddress: 'down'}

@pytest.mark.websitestatus
def test_multiple_one_invalidformat_url():
    output = mock_multiple_argument_parser(validtestaddress, invalidformattestaddress)
    assert output[validtestaddress] == {validtestaddress: 'up'}

@pytest.mark.websitestatus
def test_multiple_url_extfile():
    testservers = 'tests/mock_servers_file.txt'
    testserverstatus = mock_file_argument_parser(testservers)
    assert testserverstatus[0] == {'https://google.com': 'up'} \
            and testserverstatus[1] == {'http://invalidsite.invalidsite': 'down'}
