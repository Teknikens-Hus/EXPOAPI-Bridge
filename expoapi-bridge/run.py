from process_booking_response import processCombinedData
from process_booking_response import processBookingTypes
from process_booking_response import processBookings
from get_data_from_expo import request_bookings_from_graphql
from get_data_from_expo import request_bookingTypes_from_graphql
from mqtt_publish import MQTTClient
import time

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
mqtt_enabled = os.getenv('MQTT_ENABLED', 'false') # Default to false

file_path = '/home/app/expoapi-bridge/processed_data.json'

# Ensure the directory exists
os.makedirs(os.path.dirname(file_path), exist_ok=True)

def calculate_start_end_dates(forward, backward):
    """
    Calculate the start and end dates based on the days_forward and days_backward
    """
    # Correct format ex: 2024-06-10
    start_date = (datetime.now().date() - timedelta(days=int(backward))).strftime("%Y-%m-%d")
    end_date = (datetime.now().date() + timedelta(days=int(forward))).strftime("%Y-%m-%d")
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
    start_date, end_date = calculate_start_end_dates(days_forward, days_backward)
    newBookingTypes = request_bookingTypes_from_graphql(token, endpoint)
    newBookings = request_bookings_from_graphql(start_date, end_date, token, endpoint)
    finalData = {"error": "Something went wrong. Please check the logs."}
    # Only process the data if there is no error
    if 'error' not in newBookings and 'error' not in newBookingTypes:
        finalData = processCombinedData(newBookings, newBookingTypes)
    else:
        if 'error' in newBookings and 'error' in newBookingTypes:
            finalData = {}
            finalData.update(newBookings)
            finalData.update(newBookingTypes)
        elif 'error' in newBookings:
            finalData = newBookings
        elif 'error' in newBookingTypes:
            finalData = newBookingTypes
    # Save the new data to a file
    with open(file_path, 'w') as outfile:
        json.dump(finalData, outfile)

# Publish data to MQTT if enabled in environment variables
if(mqtt_enabled == 'true'):
    mqtt_client = MQTTClient()
    ## Loop until the MQTT client is connected
    if mqtt_client.mqtt_client is not None:
        while not mqtt_client.mqtt_connected:
            time.sleep(1)
            logging.log(logging.INFO, "Waiting for MQTT client to connect...")
        # Publish the data to the MQTT broker
        mqtt_client.publish("current_bookings", json.dumps(processBookings(newBookings)))
        mqtt_client.publish("current_booking_types", json.dumps(processBookingTypes(newBookingTypes)))
        # Wait for confirmation that the data was published
        while not mqtt_client.mqtt_message_sent:
            time.sleep(1)
            logging.log(logging.INFO, "Waiting for MQTT message to be sent...")
        mqtt_client.disconnect()
    else:
        logging.error("MQTT client did not initialize correctly")