import json
from datetime import datetime, timezone

def process_data(jsondata):
    allBookings = []
    #for booking in jsondata['bookings']:
    bookings = len(jsondata['data']['bookings']['nodes'])
    print(f"Found {bookings} bookings")
    # Create a new booking in the new easier format for each booking
    for booking in jsondata['data']['bookings']['nodes']:
        allBookings.append(create_booking(booking))
    
    # Get and format the current date and time in ISO 8601 format, ensuring it's in UTC (like other expo dates in GraphQL)
    current_datetime = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return_data = {"fetched_timestamp": current_datetime, "bookings": allBookings}
    return return_data


### Creates a new booking in the new easier format
def create_booking(booking):
    bookingID = booking['humanNumber']
    bookingState = booking['state']
    if(bookingState != 'confirmed'):
         return {"bookingID": bookingID, "bookingState": bookingState}
    firstName = booking['firstName']
    lastName = booking['lastName']
    email = booking['email']
    messageFromBooker = booking['message']
    externalComment = booking['externalComment']
    internalComment = booking['internalComment']
    bookingType = booking['bookingType']['name']
    organisation = booking['organisation']
    # Format reservation data
    reservations = {}
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
        if(event['eventAllocation']['eventAllocationResources']['totalNodeCount'] != 0):
             for resource in event['eventAllocation']['eventAllocationResources']['nodes']:
                resourceType = resource['resource']['resourceType']['name']
                resourceName = resource['resource']['name']
                newResource = {"type": resourceType, "name": resourceName}
                resources.append(newResource)
        # Set reservation data
        reservations[offer] = {"startTime": startTime, "endTime": endTime, "contract": contract, "attendees": attendees, "resources": resources}
    
    return {"bookingID": bookingID, "bookingState": bookingState, "firstName": firstName, "lastName": lastName, "email": email, "messageFromBooker": messageFromBooker, "externalComment": externalComment, "internalComment": internalComment, "bookingType": bookingType, "organisation": organisation, "reservations": reservations}