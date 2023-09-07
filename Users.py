from FileHandling import read_from_file
import FileNames

class User:


    def __init__(self, first_name, last_name, username, password, is_admin):
        self._name = first_name
        self._surname = last_name
        self.unique_username(username)
        self._password = password
        self._is_admin = is_admin
        self._reservations = []
        
    
    def save_to_csv(self):
        to_save = self._username + ',' + self._password.decode('utf-8') + ',' + self._name + ',' + self._surname + ',' + str(self._is_admin) + '\n'
        to_save = ''.join(to_save)
        with open(FileNames.user, 'a') as f:
            f.write(to_save)

    
    def unique_username(self, username):
        df = read_from_file(FileNames.user, False, False)
        not_unique = username in df['Username'].values
        if not_unique:
            while not_unique:
                print('Username already taken. Choose an another one:')
                username = input('>>>')
                not_unique = username in df['Username'].values
        self._username = username
        

