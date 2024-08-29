class BookingType:
    def __init__(self, ID, name, position, description):
        self.ID = ID
        self.name = name
        self.position = position
        self.description = description

    def __repr__(self):
        return f"BookingType({self.ID}, {self.name}, {self.position}, {self.description})"    

def BookingFromProcessedJSON(bookingTypeJSON):
    return BookingType(
        ID=bookingTypeJSON.get('id'),
        name=bookingTypeJSON.get('name'),
        position=bookingTypeJSON.get('position'),
        description=bookingTypeJSON.get('description')
    )