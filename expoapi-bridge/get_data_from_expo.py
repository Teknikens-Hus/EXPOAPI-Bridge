import requests
import json
import logging
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)

def request_bookings_from_graphql(start_date, end_date, auth_token, endpoint):
    """
    Fetches data from Expo's GraphQL API using a PAT, Personal access token at the provied endpoint address.
    """
    jsonData = fetchBookings(start_date, end_date, auth_token, endpoint)
    if jsonData == None:
        return {"error": "Failed to fetch Bookings from Expo's GraphQL API"}
    if 'error' in jsonData:
        # Dont do anything if there is an error, return the error json
        return jsonData
    if morePagesExist(jsonData):
        logging.log(logging.INFO, "Bookings fetched successfully for dates: {} to {}, but had more pages, fetching rest...".format(start_date, end_date))
        # 15 is an arbitrary number, but it might not be wise to fetch more data at one time
        totalNodes = jsonData['data']['bookings']['totalNodeCount']
        if getNumpages(jsonData) < 15:
            currentPage = 2
            numPages = getNumpages(jsonData)
            for page in range(2, numPages+1):
                nextCursor = jsonData['data']['bookings']['pageInfo']['endCursor']
                jsonDataPage = fetchBookings(start_date, end_date, auth_token, endpoint, nextCursor)
                logging.log(logging.INFO,"Fetching pages. Current page: {}. Total Pages: {}. NextCursor: {}. Has morePages: {}".format(currentPage, numPages, nextCursor, morePagesExist(jsonDataPage)))
                if 'errors' in jsonDataPage:
                    logging.log(logging.ERROR, jsonDataPage)
                    return jsonDataPage
                jsonData = appendSplitBookings(jsonData, jsonDataPage)
                currentPage += 1
            logging.log(logging.INFO, "All pages fetched. TotalNodes: {}, nodes fetched: {}".format(totalNodes, len(getNodesFromData(jsonData))))
            return jsonData
        else:
            logging.log(logging.ERROR, "Too many pages to fetch, aborting. Number of pages: {}".format(getNumpages(jsonData)))
            return {"error": "Too many pages to fetch, aborting. Number of pages: {}".format(getNumpages(jsonData))}
    else:
        # No more data exists. Return data.
        return jsonData

def request_bookingTypes_from_graphql(auth_token, endpoint):
    """
    Fetches the bookingTypes from Expo's GraphQL API
    """
    jsonData = fetchBookingTypes(auth_token, endpoint)
    if jsonData == None:
        return {"error": "Failed to fetch BookingTypes from Expo's GraphQL API"}
    if 'error' in jsonData:
        # Dont do anything if there is an error, return the error json
        return jsonData
    if morePagesExist(jsonData):
        logging.log(logging.INFO, "BookingTypes fetched successfully, but had more pages, fetching rest...")
        # 15 is an arbitrary number, but it might not be wise to fetch more data at one time
        totalNodes = jsonData['data']['bookingTypes']['totalNodeCount']
        if getNumpages(jsonData) < 15:
            currentPage = 2
            numPages = getNumpages(jsonData)
            for page in range(2, numPages+1):
                nextCursor = jsonData['data']['bookingTypes']['pageInfo']['endCursor']
                jsonDataPage = fetchBookingTypes(auth_token, endpoint, nextCursor)
                logging.log(logging.INFO,"Fetching pages. Current page: {}. Total Pages: {}. NextCursor: {}. Has morePages: {}".format(currentPage, numPages, nextCursor, morePagesExist(jsonDataPage)))
                if 'errors' in jsonDataPage:
                    logging.log(logging.ERROR, jsonDataPage)
                    return jsonDataPage
                jsonData = appendSplitBookingTypes(jsonData, jsonDataPage)
                currentPage += 1
            logging.log(logging.INFO, "All pages fetched. TotalNodes: {}, nodes fetched: {}".format(totalNodes, len(getNodesFromData(jsonData))))
            return jsonData
        else:
            logging.log(logging.ERROR, "Too many pages to fetch, aborting. Number of pages: {}".format(getNumpages(jsonData)))
            return {"error": "Too many pages to fetch, aborting. Number of pages: {}".format(getNumpages(jsonData))}
    else:
        # No more data exists. Return data.
        return jsonData    

def fetchBookings(start_date, end_date, auth_token, endpoint, cursor=None):
    # Read the query template from the file
    
    if cursor:
        variables = {
            "startAtGteq": start_date,
            "endAtLteq": end_date,
            "cursor": cursor
        }
        with open('booking-query-page.graphql', 'r') as file:
            query = file.read()
    else:
        variables = {
            "startAtGteq": start_date,
            "endAtLteq": end_date
        }
        with open('booking-query.graphql', 'r') as file:
            query = file.read()

    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }
    logging.log(logging.INFO, "Fetching Bookings from Expo's GraphQL API... at dates: {} to {}".format(start_date, end_date))
    # Send the request
    response = requests.post(endpoint, json={"query": query, "variables": variables}, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        try:
            if response.content:
                if morePagesExist(response.json()):
                    return response.json()
                else:
                    logging.log(logging.INFO, "Bookings fetched successfully for dates: {} to {}".format(start_date, end_date))
                    return response.json()
            else:
                logging.log(logging.ERROR, "Empty response body")
                return {"error": "Empty response body"}
        except json.decoder.JSONDecodeError:
            logging.log(logging.ERROR, f"Failed to decode JSON response: {response.text}")
            return {"error": "Failed to decode JSON response"}
    else:
        logging.log(logging.ERROR, "Failed to fetch data, check endpoint or auth token!")
        return {"error": f"HTTP Error: {response.status_code}", "details": response.text, "hint": "Check the endpoint and auth token"}

def fetchBookingTypes(auth_token, endpoint, cursor=None):
    # Read the query template from the file
    if cursor:
        variables = {
            "cursor": cursor
        }
        with open('bookingTypes-query-page.graphql', 'r') as file:
            query = file.read()
    else:
        variables = {}
        with open('bookingTypes-query.graphql', 'r') as file:
            query = file.read()

    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }
    logging.log(logging.INFO, "Fetching bookingTypes from Expo's GraphQL API...")
    # Send the request
    response = requests.post(endpoint, json={"query": query, "variables": variables}, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        try:
            if response.content:
                if morePagesExist(response.json()):
                    return response.json()
                else:
                    logging.log(logging.INFO, "BookingTypes fetched successfully")
                    return response.json()
            else:
                logging.log(logging.ERROR, "Empty response body")
                return {"error": "Empty response body"}
        except json.decoder.JSONDecodeError:
            logging.log(logging.ERROR, f"Failed to decode JSON response: {response.text}")
            return {"error": "Failed to decode JSON response"}
    else:
        logging.log(logging.ERROR, "Failed to fetch data, check endpoint or auth token!")
        return {"error": f"HTTP Error: {response.status_code}", "details": response.text}

def appendSplitBookings(data1, data2):
    # Append the data from the second request to the first request
    nodes = getNodesFromData(data1) + getNodesFromData(data2)
    combinedData = {"data": 
                    {"bookings": 
                     {"totalNodeCount": data2['data']['bookings']['totalNodeCount'],
                      "totalPageCount": data2['data']['bookings']['totalPageCount'],
                      "pageInfo":
                        {"endCursor": data2['data']['bookings']['pageInfo']['endCursor'],
                         "hasNextPage": data2['data']['bookings']['pageInfo']['hasNextPage'],
                         "hasPreviousPage": data2['data']['bookings']['pageInfo']['hasPreviousPage'],
                         "startCursor": data1['data']['bookings']['pageInfo']['startCursor']},
                      "nodes": nodes
                      }
                    }
                   }
    return combinedData

def appendSplitBookingTypes(data1, data2):
    # Append the data from the second request to the first request
    nodes = getNodesFromData(data1) + getNodesFromData(data2)
    combinedData = {"data": 
                    {"bookingTypes": 
                     {"totalNodeCount": data2['data']['bookingTypes']['totalNodeCount'],
                      "totalPageCount": data2['data']['bookingTypes']['totalPageCount'],
                      "pageInfo":
                        {"endCursor": data2['data']['bookingTypes']['pageInfo']['endCursor'],
                         "hasNextPage": data2['data']['bookingTypes']['pageInfo']['hasNextPage'],
                         "hasPreviousPage": data2['data']['bookingTypes']['pageInfo']['hasPreviousPage'],
                         "startCursor": data1['data']['bookingTypes']['pageInfo']['startCursor']},
                      "nodes": nodes
                      }
                    }
                   }
    return combinedData

def morePagesExist(json):
    """
    Check if the request was too big and was split into multiple pages
    """
    try:
        return json['data']['bookings']['pageInfo']['hasNextPage']
    except KeyError:
        try:
            return json['data']['bookingTypes']['pageInfo']['hasNextPage']
        except KeyError:
            logging.error("No pageInfo found in the json response!")
            return False

def getNumpages(json):
    """
    Get the number of pages that exist
    """
    try:
        return json['data']['bookings']['totalPageCount']
    except KeyError:
        try:
            return json['data']['bookingTypes']['totalPageCount']
        except KeyError:
            logging.error("No totalPageCount found in the json response!")
            return False

def getNodesFromData(data):
    """
    Get the nodes from the data
    """
    try:
        return data['data']['bookings']['nodes']
    except KeyError:
        try:
            return data['data']['bookingTypes']['nodes']
        except KeyError:
            logging.error("No nodes found in the json response!")
            return False