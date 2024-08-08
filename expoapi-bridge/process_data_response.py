import json
from datetime import datetime, timezone
import logging

logging.basicConfig(level=logging.INFO)

def process_data(jsondata):
    allBookings = []
    #for booking in jsondata['bookings']:
    bookings = len(jsondata['data']['bookings']['nodes'])
    logging.log(logging.INFO, f"Found {bookings} bookings")
    
    # Create a new booking in the new easier format for each booking
    for booking in jsondata['data']['bookings']['nodes']:
        allBookings.append(create_booking(booking))
    
        # Split the bookings into confirmed and rejected
    confirmedBookings = []
    rejectedBookings = []

    for booking in allBookings:
        if booking['bookingState'] == 'confirmed':
            confirmedBookings.append(booking)
        else:
            rejectedBookings.append(booking)
        
    logging.log(logging.INFO, f"Confirmed bookings: {len(confirmedBookings)}")
    logging.log(logging.INFO, f"Rejected bookings: {len(rejectedBookings)}")

    # Sort the confirmedBookings by the earliest reservation start time
    confirmedBookings.sort(key=lambda x: get_start_time(get_earliest_reservation(x['reservations'])))

    # Combine the confirmed and rejected bookings into one list
    allBookings = confirmedBookings + rejectedBookings
    
    return_data = {"fetched_timestamp": get_current_time(), "bookings": allBookings}
    
    # Check the data
    try:
        json.dumps(return_data)
        return return_data
    except (TypeError, ValueError) as e:
        logging.ERROR(logging.ERROR, f"Error: {e}")
        logging.ERROR(logging.ERROR, f"Data: {return_data}")
        return {"error": "Failed to process data"}
                
def get_start_time(reservation):
    # Convert the startTime string to a datetime object
    return datetime.fromisoformat(reservation['startTime'].replace('Z', '+00:00'))

def get_earliest_reservation(reservations):
    if not reservations:
        return None
    # Use the get_start_time function as the key for the min function
    return min(reservations, key=get_start_time)

def get_current_time():
    # Get and format the current date and time in ISO 8601 format, ensuring it's in UTC (like other expo dates in GraphQL)
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

### Creates a new booking in the new easier format
def create_booking(booking):
    bookingID = booking['humanNumber']
    bookingState = booking['state']
    #if(bookingState != 'confirmed'):
    #     return {"bookingID": bookingID, "bookingState": bookingState}
    firstName = booking['firstName']
    lastName = booking['lastName']
    email = booking['email']
    messageFromBooker = booking['message']
    externalComment = booking['externalComment']
    internalComment = booking['internalComment']
    bookingType = booking['bookingType']['name']
    organisation = booking['organisation']
    # Format reservation data
    reservations = []
    for reservation in booking['reservations']['nodes']:
        startTime = reservation['startAt']
        endTime = reservation['endAt']
        contract = None
        # Reservations
        event = reservation['event']
        offer = event['offer']['name']
        if(reservation['contract'] != None):
             contract = reservation['contract']['name']

        # Format attendees data
        attendees = {"Attendees": 0}
        if(reservation['attendees']['totalNodeCount'] != 0):
            tempAttendees = {}
            for attendee in reservation['attendees']['nodes']:
                attendeeType = attendee['attendeeType']['name']
                if attendeeType in tempAttendees:
                    tempAttendees[attendeeType] += 1
                else:
                    tempAttendees[attendeeType] = 1
            # Set formated attendee data
            attendees = tempAttendees
        
        resources = []
        if(event['eventAllocation'] != None):
             if event['eventAllocation']['eventAllocationResources']['totalNodeCount'] != 0:
                for resource in event['eventAllocation']['eventAllocationResources']['nodes']:
                    resourceType = resource['resource']['resourceType']['name']
                    resourceName = resource['resource']['name']
                    newResource = {"type": resourceType, "name": resourceName}
                    resources.append(newResource)
        else:
            resources = None
        # Set reservation data
        reservations.append({"startTime": startTime, "endTime": endTime, "contract": contract, "attendees": attendees, "resources": resources})
    
    return {"bookingID": bookingID, "bookingState": bookingState, "firstName": firstName, "lastName": lastName, "email": email, "messageFromBooker": messageFromBooker, "externalComment": externalComment, "internalComment": internalComment, "bookingType": bookingType, "organisation": organisation, "reservations": reservations}