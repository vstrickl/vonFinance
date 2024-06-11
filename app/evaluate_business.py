"""Here: https://www.alphavantage.co/documentation/"""
import os
import django
import logging
import argparse

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vonFinance.settings')
django.setup()

from financials.financial_statements import income_statement
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Call the function
def run():
    parser = argparse.ArgumentParser(description='Fetch and save income statement for a given NYSE ticker.')
    parser.add_argument('function', type=str, help='The function to run')
    parser.add_argument('nyse', type=str, help='The NYSE ticker symbol')
    parser.add_argument('reportTimeFrame', type=str, choices=['annualReports', 'quarterlyReports'], help='The report time frame (annualReports or quarterlyReports)')
    parser.add_argument('fiscalDateEnding', type=str, help='The fiscal date ending (YYYY-MM-DD)')
 
    args = parser.parse_args()

    if args.function == 'income_statement':
        income_statement(args.nyse, args.reportTimeFrame, args.fiscalDateEnding)
    else:
        logging.error(f'\nUnknown function: {args.function}\n')

if __name__ == '__main__':
    run()