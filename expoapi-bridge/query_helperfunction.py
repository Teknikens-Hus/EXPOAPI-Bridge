import logging
import json

logging.basicConfig(level=logging.INFO)

def morePagesExist(json, dataType):
    """
    Check if the request was too big and was split into multiple pages
    """
    try:
        return json['data'][dataType]['pageInfo']['hasNextPage']
    except KeyError:
        logging.error("No pageInfo found in the json response!")
        return False

def getNumpages(json, dataType):
    """
    Get the number of pages that exist
    """
    try:
        return json['data'][dataType]['totalPageCount']
    except KeyError:
        logging.error("No totalPageCount found in the json response!")
        return False

def getNodesFromData(json, dataType):
    """
    Get the nodes from the data
    """
    try:
        return json['data'][dataType]['nodes']
    except KeyError:
        logging.error("No nodes found in the json response!")
        return False
    
def appendSplitData(data1, data2, dataType):
    # Append the data from the second request to the first request
    nodes = getNodesFromData(data1, dataType) + getNodesFromData(data2, dataType)
    combinedData = {"data": 
                    {dataType: 
                     {"totalNodeCount": data2['data'][dataType]['totalNodeCount'],
                      "totalPageCount": data2['data'][dataType]['totalPageCount'],
                      "pageInfo":
                        {"endCursor": data2['data'][dataType]['pageInfo']['endCursor'],
                         "hasNextPage": data2['data'][dataType]['pageInfo']['hasNextPage'],
                         "hasPreviousPage": data2['data'][dataType]['pageInfo']['hasPreviousPage'],
                         "startCursor": data1['data'][dataType]['pageInfo']['startCursor']},
                      "nodes": nodes
                      }
                    }
                   }
    return combinedData