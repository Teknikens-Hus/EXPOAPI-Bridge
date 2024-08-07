import requests
import json
import logging

logging.basicConfig(level=logging.INFO)

def fetch_data_from_graphql(start_date, end_date, auth_token, endpoint):
    """
    Fetches data from Expo's GraphQL API using a PAT, Personal access token at the provied endpoint address.
    """
    #print("Fetching data from file...")
    with open('booking-query.graphql', 'r') as file:
        query = file.read()

    variables = {
        "startAtGteq": start_date,
        "endAtLteq": end_date
    }

    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }
    #print(f"Sending request to Expo's GraphQL API at endpoint: {endpoint} with token: {auth_token}")
    # Send the request
    logging.log(logging.INFO, "Fetching data from Expo's GraphQL API...")
    response = requests.post(endpoint, json={"query": query, "variables": variables}, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        try:
            if response.content:
                logging.log(logging.INFO, "Data fetched successfully")
                return response.json()
            else:
                return {"error": "Empty response body"}
        except json.decoder.JSONDecodeError:
            logging.log(logging.ERROR, f"Failed to decode JSON response: {response.text}")
            return {"error": "Failed to decode JSON response"}
    else:
        logging.log(logging.ERROR, "Failed to fetch data, check endpoint or auth token!")
        return {"error": f"HTTP Error: {response.status_code}", "details": response.text}