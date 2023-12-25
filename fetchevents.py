import requests
import time
import os
from datetime import datetime

os.chdir("/Users/stevenslater/Desktop/ticcalapp")
print(os.getcwd())

def convert_to_iso(date_string):
    date = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
    return date.isoformat() + "Z"



def fetch_events(api_key, filename="events.txt"):

    url = "https://app.ticketmaster.com/discovery/v2/events.json"
    last_event_date = None
    last_event_id = None
    new_last_event_id = None


    if os.path.exists(filename):
        with open(filename, "r") as file:
            lines = file.readlines()
            last_event_id, last_event_date = lines[-1].strip().split(',')

    page = 0


    while True:
        params = {
            'apikey': api_key,
            'marketId': '207',
            'page': page,  # Fetch the current page
            'sort': 'date,asc',
            'startDateTime': last_event_date
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        events_data = response.json()

        if not events_data.get('_embedded') or page == 49:  # If no new events are found, break the loop
            break

        events = events_data['_embedded']['events']
        new_last_event_id = events[-1]['id']  # Update the last event ID

        with open(filename, "a") as file:
            for event in events:
                print(event['name'])
                if 'dateTime' in event['dates']['start']:
                    file.write(f"{event['id']},{event['dates']['start']['dateTime']}\n")
                else:
                    print(f"Event {event['id']} does not have a start date and time.")

        page += 1  # Go to the next page
        time.sleep(0.2)  # Pause for 0.2 seconds
    
    return new_last_event_id

#function to contiue requesting untill the last request returns the same eventID as the current request (means we have reached the end)
def fetch_all(api_key, filename="events.txt"):
    last_event_id = -1
    new_last_event_id = -2

    while last_event_id != new_last_event_id:
        last_event_id = new_last_event_id
        new_last_event_id = fetch_events(api_key, filename)
    print("All events scanned")
