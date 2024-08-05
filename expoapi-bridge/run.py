from process_data_response import process_data
from get_data_from_expo import fetch_data_from_graphql
import json
import os
import logging
from datetime import datetime, timedelta

# Config logging
logging.basicConfig(level=logging.INFO)

token = os.getenv('TOKEN')
endpoint = os.getenv('ENDPOINT')
days_forward = os.getenv('DAYS_FORWARD', '7') # Default to 7 days
days_backward = os.getenv('DAYS_BACKWARD', '0') # Default to 0 days (Today)

file_path = '/home/app/expoapi-bridge/processed_data.json'

# Ensure the directory exists
os.makedirs(os.path.dirname(file_path), exist_ok=True)

def calculate_start_end_dates():
    """
    Calculate the start and end dates based on the days_forward and days_backward
    """
    # Correct format ex: 2024-06-10
    start_date = (datetime.now().date() - timedelta(days=int(days_backward))).strftime("%Y-%m-%d")
    end_date = (datetime.now().date() + timedelta(days=int(days_forward))).strftime("%Y-%m-%d")
    return start_date, end_date

# make a check that the variables are not empty
if not token or not endpoint:
    missing_variables = []
    if not token:
        missing_variables.append("TOKEN")
    if not endpoint:
        missing_variables.append("ENDPOINT")
    error_message = "Missing environment variables: " + ", ".join(missing_variables)
    logging.log(logging.ERROR, error_message)
    # make a json file that contains the error message
    with open(file_path, 'w') as outfile:
        json.dump({"error": error_message}, outfile, indent=4)
else:
    logging.log(logging.INFO, "Fetching data from Expo's GraphQL API...")
    start_date, end_date = calculate_start_end_dates()
    newdata = process_data(fetch_data_from_graphql(start_date, end_date, token, endpoint))
    # Save the new data to a file
    with open(file_path, 'w') as outfile:
        json.dump(newdata, outfile, indent=4)
    logging.log(logging.INFO, "Data fetched and processed successfully for dates: {} to {}".format(start_date, end_date))