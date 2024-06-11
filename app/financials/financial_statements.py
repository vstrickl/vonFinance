import os
import json
import requests
import logging

from vonFinance.settings import API_KEY
from vonFinance.settings import BASE_DIR
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Create your views here.
def income_statement(nyse, report_time_frame, fiscal_date_ending):
    url = 'https://www.alphavantage.co/query'
    params = {
        'function': 'INCOME_STATEMENT',
        'symbol': nyse,
        'apikey': API_KEY
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        reports = data.get(report_time_frame, [])
        
        # Filter reports by fiscal_date_ending
        filtered_reports = [report for report in reports if report['fiscalDateEnding'] == fiscal_date_ending]

        output_directory = os.path.join(BASE_DIR, 'financials', 'outputs')
        os.makedirs(output_directory, exist_ok=True)
        filename = f'{nyse}_{report_time_frame}_{fiscal_date_ending}_income_statement.json'
        output_filename = os.path.join(output_directory, f'{filename}')
        with open(output_filename, 'w', encoding='utf-8') as json_file:
            json.dump(filtered_reports, json_file, indent=4)

        logging.info(f'\nSuccessfully created the following file in the outputs directory:\n\n      - {filename}\n')
        return
    except requests.exceptions.HTTPError as http_err:
        logging.error(f'\nHTTP error occurred: {http_err}\n')
    except Exception as e:
        logging.error('\nAn exception occurred: %s\n', e)