import os
import Locations
from Users import *
from FileHandling import *
import FileNames
from time import sleep
from datetime import datetime
import bcrypt
from Events import delete_event

#----- Current Date:      
now = datetime.today().date()
today = pd.to_datetime(datetime.today().date())
date_text = now.strftime('%A, %d. %B')
date_str = now.strftime('%Y-%m-%d')

#----------------------------------------------- FUNCTIONS
#----- Screens:
def main_screen():
    os.system('clear')
    
    # Display upcoming events if they exist
    if events_screen():
        print('---Upcoming Events---')
        events_list = first_3_rows_dict
        for events_dict in events_list:
            #print(f'{events_dict["Name"]: {events_dict["Event"]}}')
            date = events_dict['Date'].strftime('%Y-%m-%d')
            print(date + ' at ' + events_dict['Name'] + ': ' + events_dict['Event'])
        print('\n')

    # Display user options
    print('---Workplace PRO---')
    print('1. Register')
    print('2. Log in')
    print('3. Exit application')

    # Prompt the user to enter number to change screen
    userinput = input('>>>')
    if userinput == '1':
        register()
    if userinput == '2':
        login()
    if userinput == '3':
        exit()
    else:
        main_screen()


def events_screen():
    """
    Generates the global variable first_3_rows_dict which contains the next three events.
    Returns True if there are any events otherwise, it returns False
    """
    events_df = pd.read_csv(FileNames.events)
    location_df = pd.read_csv(FileNames.location)
    location_df['Location'] = location_df.index
    sorted_df = sort_by_date(events_df)
    if sorted_df.empty:
        return False
    merged_df = sorted_df.merge(location_df, on='Location', how='left')
    global first_3_rows_dict
    first_3_rows_dict = merged_df.iloc[:3].to_dict(orient='records')
    return True


def register():
    """
    Prompts the user through the registration process and saves it to csv
    """
    os.system('clear')
    print('Enter your first name:')
    first_name = input('>>>')
    print('Enter your last name:')
    last_name = input('>>>')
    print('Enter an username:')
    username = input('>>>')
    print('Create a password:')
    password = input('>>>')
    hashed_password = hash_password(password)
    print('Create an admin Account? (y/n)')
    print("Please note that admin accounts can't book reservaions.")
    is_admin = input('>>>')
    if is_admin.lower() == 'y':
        admin = 1
    else:
        admin = 0
    new_user = User(first_name, last_name, username, hashed_password, admin)
    new_user.save_to_csv()
    main_screen()


def login():
    """Hanles user login functionality"""
    os.system('clear')
    df = read_from_file(FileNames.user, False, False)
    print('---Log in---')
    print('Enter your username')
    input_username = input('>>>')
    print('Enter your password')
    input_password = input('>>>')
    if input_username in df['Username'] .values:
        global userindex
        userindex = df[df['Username'] == input_username].iloc[0]
        global userdata
        userdata = userindex.to_dict()
        stored_password = userdata['Password']
        if check_password(input_password, stored_password):
            is_admin = userindex['Is Admin']
            if is_admin:
                admin_screen() 
            else:
                user_screen()        
        else:
            print("Invalid password.")
            sleep(2)
            main_screen()
    else:
        print("Username not found.")
        sleep(2)
        main_screen()

    
def admin_screen():
    os.system('clear')
    print('---Admin Account---')
    print('Hi ' + userdata['First Name'])
    print(date_text + '\n')

    # Display admin options
    print("1. Edit locations.")
    print("2. Show current utilization.")
    print("3. Cancel reservations.")
    print("4. Manage Events")
    print('5. Log out')

    # Prompt the user to enter number
    userinput = int(input('>>>'))

    if userinput == 1:
         edit_locations()
            
    elif userinput == 2:
        os.system('clear')
        print(free_spots(date_str))
        print('\n\n\n')
        print('1. Go back...')
        if input('>>>') == '1':
            admin_screen()
    elif userinput == 3:
        os.system('clear')
        admin_cancel_reservation()
        sleep(2)
        admin_screen()
    elif userinput == 4:
        os.system('clear')
        manage_events()
    elif userinput == 5:
        main_screen()


def user_screen():
    os.system('clear')
    print('---User Account---')
    print('Hi ' + userdata['First Name'])
    print(date_text + '\n')

    # Display user options
    print("1. Book new reservation.")
    print("2. Show current utilization.")
    print("3. Cancel reservations.")
    print('4. Show upcoming reservations')
    print('5. Log out')

    # Prompt the user to enter a number
    userinput = int(input('>>>'))
    
    if userinput == 1:
         new_reservation()
         sleep(2)
         user_screen()
            
    elif userinput == 2:
        os.system('clear')
        print(free_spots(date_str))
        print('\n\n\n')
        print('1. Go back...')
        if input('>>>') == '1':
            user_screen()
        
    elif userinput == 3:
         os.system('clear')
         user_cancel_reservation()
         user_screen()

    elif userinput == 4:
        os.system('clear')
        get_reservations(True)
        print('\n')
        print('1. Go back...')
        if input('>>>') == '1':
            user_screen()


    elif userinput == 5:
        main_screen()


#------ Admin Functions:
def manage_events():
        """
        A function to display saved events and give the user the option
        to add new or delete existing ones
        """
        os.system('clear')
        print('---Manage Events---')
        print(date_text + '\n')
        print_out_events()
        print('\n')
        print("1. Add Event")
        print("2. Delete Event")
        print("3. Go back...")
        userinput = int(input('>>>'))

        if userinput == 1:
            add_event()
            sleep(2)
            manage_events()
        elif userinput == 2:
            delete_event()
            manage_events()
        elif userinput == 3:
            admin_screen()


def print_out_events():
    """Prints saved events from csv file in a formatted way"""
    events = pd.read_csv(FileNames.events)
    locations = pd.read_csv(FileNames.location)
    locations['Location'] = locations.index
    merged_df = events.merge(locations, on='Location', how='left')
    merged_df = sort_by_date(merged_df)
    print(merged_df[['Date','Name','Event']].to_string(index=False))


def add_event():
    """A function that lets the user create new events and save them to the csv file"""
    os.system('clear')
    print('---Add Event---')
    print(date_text + '\n')

    # Show locations that will be linked to the events
    print('Available Locations:')
    df_locations = read_from_file(FileNames.location, False, True)
    print(df_locations[['Name','Capacity','Adress']].to_string(index=True) + '\n')

    # Userinput
    location = int(input('Enter Location Number: ')) - 1
    event = input('Enter Event: ')
    date = input('Enter Date (yyyy-mm-dd): ')

    # Create pandas dataframe 
    event_data = {
        'Location': [location],
        'Event': [event],
        'Date': [date]
    }
    event_df = pd.DataFrame(event_data)

    # Append dataframe to csv
    with open(FileNames.events, 'a', newline='') as f:
        event_df.to_csv(f, header=False, index=False)

    print('Event Successfully Added!')
    sleep(2)


def admin_cancel_reservation():
    """Allows the admin to see all future reservations and cancel them"""
    
    # Get reservations from csv and sort it by date
    all_reservations = pd.read_csv(FileNames.reservation)
    sorted_df = sort_by_date(all_reservations)
    sorted_df.index = np.arange(1, len(sorted_df) + 1)
    print(sorted_df.to_string())
    print("Enter the reservations number to cancel or '0' to go back.")
    
    # Prompt the user continuously for input until an action is performed
    while True:
            userinput = input('>>>')
            if userinput == '0':
                admin_screen()
            elif userinput.isnumeric():
                # try to cancel reservation
                try:
                    df = sorted_df.drop([int(userinput)], axis=0)
                    df.to_csv(FileNames.reservation, index=False)
                    print('The reservation was successfully cancelled:')
                    sleep(2)
                    return True
                # handle the case where the specified index does not exist 
                except KeyError:
                    print('Choose one of the above reservations')
            # go back...
            else:
                print('Failed because no integer was entered.')


def edit_locations():
    """Display all options the admin has regarding locations"""
    os.system('clear')
    print('Stored Locations:')
    df = read_from_file(FileNames.location, False, True)
    print(df.to_string(index=False))
    print('\n\n\n')

    # Display admin options
    print("1. Add location.")
    print("2. Delete Location.")
    print("3. Go back...")

    # Prompt for userinput
    userinput = int(input('>>>'))
    if userinput == 1:
        Locations.add_location(FileNames.location)
        admin_screen()
    elif userinput == 2:
        location_id = Locations.delete_location()
        delete_events_by_location(location_id)
        delete_reservations_by_location(location_id)
        admin_screen()
    elif userinput == 3:
        admin_screen()


#------ User Functions:
def is_duplicate_reservation(username, location, date):
    """
    Check if a user already has a reservation on a specific location at the specific date.
    Return True if it has. Otherwise, return False.
    """
    reservations_df = pd.read_csv(FileNames.reservation)
    reservations_df = reservations_df[reservations_df['User'] == username]
    reservations_df = reservations_df[reservations_df['Location'] == location]
    reservations_df = reservations_df[reservations_df['Date'] == date]
    if reservations_df.empty:
        return False
    return True


def add_reservation(username, location, date):
    """
    Creates a new reservation. 
    Does error handling for location, date, free spots and duplicate reservations
    """

    # Check if location exists
    df_locations = read_from_file(FileNames.location, False, False)
    df_locations['Location'] = df_locations.index
    if location not in df_locations['Location'].values:
        print('Invalid Location. Please choose from the available locations.')
        return False


    # Check if the date follows the correct format (yyyy-mm-dd) and if it is in the future or today
    try:
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        if date_obj < datetime.now().replace(hour=0, minute=0, second=0, microsecond=0):
            print('Invalid Date. Please choose a future date or today.')
            return False
    except ValueError:
        print('Invalid Date Format. Please use yyyy-mm-dd format.')
        return False
    
    # Check if there are free spots left
    free_spots_df = free_spots(date)
    row_index = free_spots_df.index[free_spots_df['Location'] == location].tolist()
    selected_row = free_spots_df.iloc[row_index]

    # Convert the selected row to a dictionary
    row_dict = selected_row.to_dict()
    free_seats = row_dict['Free Seats']
    free_seats = int(free_seats[location])
    if free_seats < 1:
        print('No seats avaible on this day. Please try a different date or a different location.')
        return False
   
    # Check if the user already has a reservation at the specieefied location on this date
    if is_duplicate_reservation(username, location, date):
        print('You cannot have two reservations in the same location at the same day.')
        return False

    # Create a dataframe with the relevant details
    reservation_data = {
        'User': [username],
        'Location': [location],
        'Date': [f'{date}'] 
    }
    reservation_df = pd.DataFrame(reservation_data)

    # Append dataframe to csv file
    with open(FileNames.reservation, 'a', newline='') as f:
        reservation_df.to_csv(f, header=False, index=False)

    print('Reservation Successfully Added!')
    return True


def new_reservation():
    """
    Is used to display all the options the user has to create a new reservation
    Passes the data to add_reservation()
    """
    os.system('clear')
    print('---Book New Reservation---')
    print(date_text + '\n')

    # Show avaible locations
    print('Available Locations:')
    df_locations = read_from_file(FileNames.location, False, True)
    print(df_locations[['Name','Capacity','Adress']].to_string(index=True) + '\n')

    # Userinput for location and date
    location = int(input('Enter Location Number: ')) - 1
    date = input('Enter Date (yyyy-mm-dd): ')

    # Pass data to add_reservation()
    add_reservation(userdata['Username'], location, date)


def user_cancel_reservation():
    """
    Displays all reservation of a specific user and let's the user choose. Based on the input 
    the reservation gets cancelled.
    """
    username = userdata['Username']
    all_reservations = pd.read_csv(FileNames.reservation)
    locations = pd.read_csv(FileNames.location)
    filtered_df = all_reservations[all_reservations['User'] != username]
    upcoming_reservations = get_reservations(False)
    locations['Location'] = locations.index
    loc_merged_df = upcoming_reservations.merge(locations, on='Location', how='left')
    loc_merged_df.index = np.arange(1, len(upcoming_reservations) + 1)
    print(loc_merged_df[['User', 'Date', 'Name']].to_string())
    print("Enter the reservations number to cancel or '0' to go back.")
    while True:
            userinput = input('>>>')
            if userinput == '0':
                user_screen()
            elif userinput.isnumeric():
                try:
                    df = upcoming_reservations.drop([int(userinput)], axis=0)
                    merged_df = pd.concat([df, filtered_df])
                    merged_df.to_csv(FileNames.reservation, index=False)
                    print('The reservation was successfully deleted. You are still signed up to the following reservstions:')
                    print(df)
                    sleep(2)
                    return True
                except KeyError:
                    print('Choose one of the above reservations')
            else:
                print('Failed because no integer was entered.')


#------ Programm Functions:
def sort_by_date(df):
    """
    Takes a dataframe as input and sorts it by the 'Date' column in ascending order.
    Additionally it filters to only show entries from today or in the future.
    """
    df['Date'] = pd.to_datetime(df['Date'])
    filtered_df = df[df['Date'] >= today]
    sorted_df = filtered_df.sort_values(by='Date')
    return sorted_df


def free_spots(date_str):
    """
    Calculates the free seats for all locations.
    date_str needs to be YYYY-mm-dd format
    """

    # Read reservations csv file and filter it to a specific date
    reservations_df = pd.read_csv(FileNames.reservation)
    reservations_df = reservations_df[reservations_df['Date'] == date_str]

    # Count how many reservations are made per location
    bookings_count = reservations_df.groupby('Location').size().reset_index(name='Number of Bookings')

    # Get location data and create an index 'Location'
    locations_df = pd.read_csv(FileNames.location)
    locations_df['Location'] = locations_df.index

    # Merge events dataframe with location on 'Location'
    merged_df = locations_df.merge(bookings_count, on='Location', how='left')

    # Fill empty values for calculations and convert all numbers into integers
    merged_df['Number of Bookings'].fillna(0, inplace=True)
    merged_df['Number of Bookings'] = merged_df['Number of Bookings'].astype(int)

    # calculate 'Free Seats' and return final df
    merged_df['Free Seats'] = merged_df['Capacity'] - merged_df['Number of Bookings']
    return merged_df


def get_reservations(print_out):
    df_reservations = read_from_file(FileNames.reservation, False, True)
    username = userdata['Username']
    df = df_reservations[df_reservations['User'] == username]
    if print_out == True:
        print(df.to_string(index=False))
    return df


def delete_events_by_location(location_id):
    """Deletes all events assigned to a specific location based on the location_id"""
    try:
        # Read the events CSV file into a DataFrame
        events_df = pd.read_csv(FileNames.events)

        # Filter events to exclude the specified location_id
        filtered_events_df = events_df[events_df['Location'] != location_id]

        # Save the filtered DataFrame back to the same CSV file
        filtered_events_df.to_csv(FileNames.events, index=False)

    except FileNotFoundError:
        print(f"File {FileNames.events} not found.")


def delete_reservations_by_location(location_id):
    """Deletes all reservations assigned to a specific location based on the location_id"""
    try:
        # Read the reservations CSV file into a DataFrame
        reservations_df = pd.read_csv(FileNames.reservation)

        # Filter reservations to exclude the specified location_id
        filtered_reservation_df = reservations_df[reservations_df['Location'] != location_id]

        # Save the filtered DataFrame back to the same CSV file
        filtered_reservation_df.to_csv(FileNames.reservation, index=False)

    except FileNotFoundError:
        print(f"File {FileNames.reservation} not found.")


#------ Password Functions:
def hash_password(password):
    """Takes password as input and returns a hashed password"""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def check_password(input_password, hashed_password):
    """Checks input password with hashed password"""
    return bcrypt.checkpw(input_password.encode('utf-8'), hashed_password.encode('utf-8'))


#----------------------------------------------- RUN THE PROGRAM
# Check if csv files exist. Create if necessary
create_files(FileNames.location, FileNames.reservation, FileNames.user, FileNames.events)

# Display the main screen
main_screen()
