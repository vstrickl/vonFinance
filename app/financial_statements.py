"""Here: https://www.alphavantage.co/documentation/"""

import json
import logging
import requests
import argparse

from vonFinance.settings import API_KEY

logging.basicConfig(level=logging.INFO)

def income_statement(nyse):
    url = 'https://www.alphavantage.co/query'
    params = {
        'function': 'INCOME_STATEMENT',
        'symbol': nyse,
        'apikey': API_KEY
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        output_filename = f'{nyse}_income_statement.json'
        with open(output_filename, 'w') as json_file:
            json.dump(response.json(), json_file, indent=4)
        logging.info(f'Successfully created {output_filename}')
        return
    except requests.exceptions.HTTPError as http_err:
        logging.error(f'HTTP error occurred: {http_err}')
    except Exception as e:
        logging.error('An exception occurred: %s', e)

def run():
    parser = argparse.ArgumentParser(description='Fetch and save income statement for a given NYSE ticker.')
    parser.add_argument('function', type=str, help='The function to run')
    parser.add_argument('nyse', type=str, help='The NYSE ticker symbol')

    args = parser.parse_args()

    if args.function == 'income_statement':
        income_statement(args.nyse)
    else:
        logging.error(f'Unknown function: {args.function}')

if __name__ == '__main__':
    run()