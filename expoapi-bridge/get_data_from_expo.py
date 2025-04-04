import requests
import json
import logging
from query_helperfunction import morePagesExist, getNumpages, getNodesFromData, appendSplitData

logging.basicConfig(level=logging.INFO)

def request_data_from_graphql(auth_token, endpoint, dataType, start_date=None, end_date=None):
    """
    Fetches data from Expo's GraphQL API using a PAT, Personal access token at the provied endpoint address.
    """
    jsonData = fetchData(auth_token, endpoint, dataType, start_date=start_date, end_date=end_date)
    if jsonData == None:
        return {"error": f"Failed to fetch {dataType} from Expo's GraphQL API"}
    if 'error' in jsonData:
        # Dont do anything if there is an error, return the error json
        return jsonData
    if morePagesExist(jsonData, dataType):
        logging.log(logging.INFO, f"{dataType} fetched successfully for dates: {start_date} to {end_date}, but had more pages, fetching rest...")
        # 15 is an arbitrary number, but it might not be wise to fetch more data at one time
        totalNodes = jsonData['data'][dataType]['totalNodeCount']
        if getNumpages(jsonData, dataType) < 15:
            currentPage = 2
            numPages = getNumpages(jsonData, dataType)
            for page in range(2, numPages+1):
                nextCursor = jsonData['data'][dataType]['pageInfo']['endCursor']
                jsonDataPage = fetchData(auth_token, endpoint, dataType, cursor=nextCursor, start_date=start_date, end_date=end_date)
                logging.log(logging.INFO,"Fetching pages. Current page: {}. Total Pages: {}. NextCursor: {}. Has morePages: {}".format(currentPage, numPages, nextCursor, morePagesExist(jsonDataPage, dataType)))
                if 'errors' in jsonDataPage:
                    logging.log(logging.ERROR, jsonDataPage)
                    return jsonDataPage
                jsonData = appendSplitData(jsonData, jsonDataPage, dataType)
                currentPage += 1
            logging.log(logging.INFO, "All pages fetched. TotalNodes: {}, nodes fetched: {}".format(totalNodes, len(getNodesFromData(jsonData, dataType))))
            return jsonData
        else:
            logging.log(logging.ERROR, "Too many pages to fetch, aborting. Number of pages: {}".format(getNumpages(jsonData, dataType)))
            return {"error": "Too many pages to fetch, aborting. Number of pages: {}".format(getNumpages(jsonData, dataType))}
    else:
        # No more data exists. Return data.
        return jsonData 

def fetchData(auth_token, endpoint, dataType, cursor="", start_date=None, end_date=None):
    # Read the query template from the file
    fileName = "query/" + dataType + '-query.graphql'
    if start_date != None and end_date != None:
        variables = {
            "startAtGteq": start_date,
            "endAtLteq": end_date,
            "cursor": cursor
        }
    else:
        variables = {
            "cursor": cursor
        }
    with open(fileName, 'r') as file:
        query = file.read()
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }
    logging.log(logging.INFO, f"Fetching {dataType} from Expo's GraphQL API...")
    # Send the request
    response = requests.post(endpoint, json={"query": query, "variables": variables}, headers=headers)
    # Check if the request was successful
    if response.status_code == 200:
        try:
            if response.content:
                if morePagesExist(response.json(), dataType):
                    return response.json()
                else:
                    logging.log(logging.INFO, f"{dataType} fetched successfully")
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