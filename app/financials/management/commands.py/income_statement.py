"""Here: https://www.alphavantage.co/documentation/"""
import os
import json
import logging
import requests
from django.core.management.base import BaseCommand

from vonFinance.settings import API_KEY
from vonFinance.settings import BASE_DIR

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
        output_directory = os.path.join(BASE_DIR, 'finance_app', 'outputs')
        os.makedirs(output_directory, exist_ok=True)
        output_filename = os.path.join(output_directory, f'{nyse}_income_statement.json')
        with open(output_filename, 'w') as json_file:
            json.dump(response.json(), json_file, indent=4)
        logging.info(f'Successfully created {output_filename}')
        return
    except requests.exceptions.HTTPError as http_err:
        logging.error(f'HTTP error occurred: {http_err}')
    except Exception as e:
        logging.error('An exception occurred: %s', e)

class Command(BaseCommand):
    help = 'Fetch and save income statement for a give Stock Symbol'

    def add_arguments(self, parser):
        parser.add_argument('nyse', type=str, help='The NYSE symbol')

    def handle(self, *args, **kwargs):
        nyse = kwargs['nyse']
        income_statement(nyse)
