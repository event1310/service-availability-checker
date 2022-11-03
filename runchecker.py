import argparse
from website_status_checker import process_single_url, process_multiple_urls
from db import database

def parse_args():
    argument_parser = argparse.ArgumentParser(description="Enter url to check", prefix_chars='-')
    argument_parser.add_argument('-site',
                                 action='store')
    argument_parser.add_argument('-l',
                                 nargs='*',
                                 action='store',
                                 help='allows to pass more than one website to check')
    argument_parser.add_argument('-f',
                                 type=argparse.FileType('r'))
    argument_parser.add_argument('-db',
                                 action='store_true',
                                 help='store returned values in db')
    parsedargs = argument_parser.parse_args()
    return process_input_arguments(parsedargs)


def process_input_arguments(parsed_args) -> dict:
    database_send_multiple = False
    result = {}

    if parsed_args.l:
        urls = parsed_args.l
        urls_amount = len(urls)
        result = process_multiple_urls(urls, urls_amount)
        database_send_multiple = True

    elif parsed_args.f:
        urls = parsed_args.f.readlines()
        urls_amount = len(urls)
        result = process_multiple_urls(urls, urls_amount)
        database_send_multiple = True

    elif parsed_args.site:
        result = process_single_url(parsed_args.site)

    if parsed_args.db:
        db_instance = database.Database()
        db_instance.connect()
        if database_send_multiple:
            db_instance.save_many(result)
            db_instance.close()
        else:
            db_instance.save(result)
            db_instance.close()

    print(result)
    return result

if __name__ == '__main__':
    parse_args()
