import requests

import checker

validtestaddress = "https://google.com"
validtestaddress2 = "https://facebook.com"
invalidtestaddress = "https://invalidsiteaddress.invalidsiteaddress"


def test_single_valid_connection():
    assert checker.mock_single_argument_parser(validtestaddress) == "up"

def test_single_invalid_connection():
    assert checker.mock_single_argument_parser(invalidtestaddress) == "down"

def test_multiple_valid_two_connections():
    assert checker.mock_multiple_argument_parser(validtestaddress, validtestaddress2) == "up"

def test_multiple_invalid_one_connection():
    assert checker.mock_multiple_argument_parser(validtestaddress, invalidtestaddress) == "down"
