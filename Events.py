import os
from FileHandling import read_from_file
import FileNames
from time import sleep

def delete_event():
    os.system("clear")
    print('---Delete Event---')

    # Read event data from the file
    events_data = read_from_file(FileNames.events, False, True)

    # Display the events to the user with updated event numbers
    # And merge Location Number with Location Name
    event_list = events_data[['Location', 'Event', 'Date']]
    location_df = read_from_file(FileNames.location, False, False)
    location_df['Location'] = location_df.index
    event_list = event_list.merge(location_df, on='Location', how='left')
    event_list.index = range(1, len(event_list) + 1)
    print(event_list[['Date','Name','Event']].to_string(index=True) + '\n')

    # Prompt the user to enter the event number to delete or '0' to go back
    event_to_delete = input('Enter Event Number to Delete (or 0 to go back): ')

    if event_to_delete == '0':
        return

    try:
        event_number_to_delete = int(event_to_delete)
        if event_number_to_delete in event_list.index:
            events_data = events_data.drop(event_number_to_delete)
            events_data.to_csv(FileNames.events, index=False)
            print('Event Successfully Deleted!')
            sleep(2)
        else:
            print('Invalid Event Number.')
            sleep(2)
    except ValueError:
        print('Invalid input. Please enter a valid Event Number.')
        sleep(2)

    # Call delete_event function again to allow deleting more events
    delete_event()
