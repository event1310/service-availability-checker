from tests.test_servicechecker import *

if __name__ == '__main__':
    test_single_valid_connection()
    test_single_invalid_connection()
    test_multiple_valid_two_connections()
    test_multiple_invalid_one_connection()
    test_connection_to_server_from_textfile()
