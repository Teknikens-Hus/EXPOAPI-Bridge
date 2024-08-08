from get_data_from_expo import request_data_from_graphql
from run import calculate_start_end_dates
from process_data_response import process_data
from bookingObject import Booking
from bookingObject import BookingFromProcessedJSON
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
    print(f"New data at: Start date: {start_date}, End date: {end_date}")
    data = request_data_from_graphql(start_date, end_date, token, endpoint)

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



raw_data = read_json('raw_data.json')
processed_data = read_json('processed_data.json')

# Make booking objects
Bookings = []

for jsonBooking in processed_data['bookings']:
    #print(booking)
    Bookings.append(BookingFromProcessedJSON(jsonBooking))
print("Number of bookings {}".format(len(Bookings)))

for booking in Bookings:
    if booking.organisation is not None:
        print(booking.bookingID + " " + booking.organisation)