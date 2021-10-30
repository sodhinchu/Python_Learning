from collections import namedtuple, Counter
from datetime import datetime

class ParkingTickets:
    '''
    This is a class to lazily read contents of \'nyc_parking_tickets_extract-1.csv\' file
    '''
    def __init__(self, file_name):
        self.file_name = file_name

    def __iter__(self):
        return ParkingTickets.read_file(self.file_name)

    @staticmethod
    def read_file(file_name):
        with open(file_name) as f:
            #Yield helps reading the file contents only when retrieved but not the whole content at once
            yield from f


def cast(data_type, value):
    '''
    Function used to cast the type of each field as required for later usage
    '''
    if data_type == 'INT':
        return int(value)
    elif data_type == 'DATE&TIME':
        return datetime.strptime(value, '%m/%d/%Y')
    elif data_type == 'BOOL':
        return bool(value)
    else:
        return str(value)

def cast_row(data_types, data_row):
    return [cast(data_type, value) for data_type, value in zip(data_types, data_row)]

class Tickets:
    '''
    This is a class to lazily read and extract violation information in a structured manner
    '''
    def __init__(self, ParkingTickets):
        self.tickets = ParkingTickets

    def __iter__(self):
        return Tickets.fetch_ticket(self.tickets)

    @staticmethod
    def fetch_ticket(park_tkts):
        data_types = ['INT', 'STRING', 'STRING', 'STRING', 'DATE&TIME', 'INT', 'STRING', 'STRING', 'STRING', 'BOOL']    
        for index, tkt in enumerate(park_tkts):
            if index == 0:
                #First line of the file contains headers
                headers = tkt.strip('\n').split(',')
                for index, header in enumerate(headers):
                    headers[index] = '_'.join(header.split(' '))
                #Added new column to easily count the violations for each car
                headers.append('Is_Violated')
                Car = namedtuple('Car', headers)
            else:
                #Violations data starts from second line onwards in the file
                data = tkt.strip('\n').split(',')
                #Adding data for the new column: True Indicates a violation happened, False otherwise
                if(data[-1] == ''):
                    data.append('False')
                else:
                    data.append('True')
                #Casting to maintain the type of each field of namedtuple
                data = cast_row(data_types, data)
                car = Car(*data)
                yield car