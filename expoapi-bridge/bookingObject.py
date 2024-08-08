class Booking:
    def __init__(self, bookingID, bookingState, firstName, lastName, email, messageFromBooker, externalComment, internalComment, bookingType, organisation, reservations):
        self.bookingID = bookingID
        self.bookingState = bookingState
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.messageFromBooker = messageFromBooker
        self.externalComment = externalComment
        self.internalComment = internalComment
        self.bookingType = bookingType
        self.organisation = organisation
        self.reservations = reservations

    def __repr__(self):
        return f"Booking({self.bookingID}, {self.bookingState}, {self.firstName}, {self.lastName}, {self.email})"
    
    def getStartDates(self):
        if self.bookingState == 'rejected':
            return []
        startDates = []
        for reservation in self.reservations:
            startDates.append(reservation['startTime'])
        return startDates
    
    

def BookingFromProcessedJSON(bookingJSON):
    return Booking(
        bookingID=bookingJSON.get('bookingID'),
        bookingState=bookingJSON.get('bookingState'),
        firstName=bookingJSON.get('firstName'),
        lastName=bookingJSON.get('lastName'),
        email=bookingJSON.get('email'),
        messageFromBooker=bookingJSON.get('messageFromBooker'),
        externalComment=convertEmptyStringToNone(bookingJSON.get('externalComment')),
        internalComment=convertEmptyStringToNone(bookingJSON.get('internalComment')),
        bookingType=bookingJSON.get('bookingType'),
        organisation=convertEmptyStringToNone(bookingJSON.get('organisation')),
        reservations=bookingJSON.get('reservations')
    )


def convertEmptyStringToNone(value):
    if value == "":
        return None
    return value