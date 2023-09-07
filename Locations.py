import os
from time import sleep
import FileNames
from FileHandling import read_from_file


class Location:


    def __init__(self, locname, pmax, address):
        self._locname = locname
        self.set_pmax(pmax)
        self._address = address


    def set_pmax(self, pmax):
        if pmax.isnumeric() and int(pmax) > 0:
            self._pmax = pmax
        else:
            message = 'At least one seat must be assigned and only whole numbers may be entered'
            userinput = 0
            while userinput < 1:
                print(message)
                try:
                    userinput = int(input('>>>'))
                except ValueError:
                    pass
            self._pmax = str(userinput)
                  

    def print_location_info(self):
            info = f"""
            Name: {self._locname}
            Number of seats: {self._pmax}
            Adress: {self._address}
            """
            return info
    

    def save_to_csv(self, filename):
        to_save = str(self._locname + ',' + self._pmax + ',' + self._address + '\n')
        with open(filename, 'a') as f:
            f.write(to_save)


def create_location_object():
     locname = input('Location name: ')
     pmax = input('Maximum number of seats: ')
     address = input('Adress: ')
     return Location(locname, pmax, address)


def add_location(filename):
    os.system('clear')   
    new_location = create_location_object() 
    print(new_location.print_location_info())  
    new_location.save_to_csv(filename)
    sleep(2)


def delete_location():
        os.system('clear')
        df = read_from_file(FileNames.location, True, True)
        while True:
            userinput = input('>>>')
            if userinput == '0':
                return          
            elif userinput.isnumeric():
                try:
                    df = df.drop([int(userinput)], axis=0)
                    df.to_csv(FileNames.location, index=False)
                    print('The location was successfully removed. The database contains the following seats:')
                    print(df)
                    sleep(2)
                    return int(userinput) - 1
                except KeyError:
                    print('Choose one of the above locations')
            else:
                print('Failed because no integer was entered.')