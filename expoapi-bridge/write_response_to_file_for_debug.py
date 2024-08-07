from get_data_from_expo import fetch_data_from_graphql
from run import calculate_start_end_dates
from process_data_response import process_data
import json
import yaml
import os

def read_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def read_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Filepath to the secrets file
secrets_file_path = './secrets.yaml'
# Read the secrets from the file
secrets = read_yaml(secrets_file_path)
# Get values we need to test
token = secrets['token']
endpoint = secrets['endpoint']
days_forward = secrets['days_forward']
days_backward = secrets['days_backward']


def write_response_to_file_for_debug(jsondata, filename):
    with open(filename, 'w') as file:
        file.write(json.dumps(jsondata, indent=4))
    print("Response written to file {}".format(filename))
    return


def get_new_debug_data():
    # Get dates from the calculate_start_end_dates function
    start_date, end_date = calculate_start_end_dates(days_forward, days_backward)
    data = fetch_data_from_graphql(start_date, end_date, token, endpoint)

    write_response_to_file_for_debug(data, 'raw_data.json')
    write_response_to_file_for_debug(process_data(data), 'processed_data.json')

# Get new data if one of the files dont exist.
# Simply delete the files and rerun the script to get new data
if not os.path.exists('raw_data.json') or not os.path.exists('processed_data.json'):
    print("Files not found, getting new data")
    get_new_debug_data()


def find_key(obj, result_array, target_key):
    # Find the humanNumber in the raw data
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == target_key:
                result_array.append(value)
            else:
                find_key(value, result_array, target_key)
    elif isinstance(obj, list):
        for item in obj:
            find_key(item, result_array, target_key)


human_numbers_raw = []
bookingIDs_processed = []
startTime_processed = []

raw_data = read_json('raw_data.json')
processed_data = read_json('processed_data.json')

find_key(raw_data, human_numbers_raw, 'humanNumber')
find_key(processed_data, bookingIDs_processed, 'bookingID')
find_key(processed_data, startTime_processed, 'startTime')

print(len(human_numbers_raw))
print(len(bookingIDs_processed))
print(len(startTime_processed))

