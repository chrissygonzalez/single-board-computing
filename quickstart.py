from __future__ import print_function
import datetime
import pickle
import os.path
import sys
import time
import pytz
from dateutil import parser
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from blinkt import set_pixel, set_all, set_brightness, show, clear


#### CONSTANTS

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
CALENDAR_ID = 'family11329664508214213018@group.calendar.google.com'
FIRST_ALERT = 5
SECOND_ALERT = 2

REBOOT_COUNTER_ENABLED = False
REBOOT_NUM_RETRIES = 10

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 153, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

CHECKING_COLOR = BLUE
SUCCESS_COLOR = GREEN
FAILURE_COLOR = RED


#### GLOBAL VARIABLES
reboot_counter = 0  # counter variable, tracks retry events.
has_error = False


#### CALENDAR FUNCTIONS

def get_credentials():
 # taken from https://developers.google.com/google-apps/calendar/quickstart/python
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
            return creds
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
            return creds
 
 
def get_events(creds, num_minutes):
    service = build('calendar', 'v3', credentials=creds)

    now = datetime.datetime.utcnow()
    then = now + datetime.timedelta(minutes=num_minutes)
    events_result = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=now.isoformat() + 'Z',
        timeMax=then.isoformat() + 'Z',
        maxResults=10,
        singleEvents=True,
        orderBy='startTime').execute()
    events = events_result.get('items', [])
    return events


def get_event_with_reminder(event_list):
    current_time = pytz.utc.localize(datetime.datetime.utcnow())

    for event in event_list:
        start = event['start'].get('dateTime')
        if start:
            event_start = parser.parse(start)
            print(event_start)
            if current_time < event_start:
                if has_reminder_override(event):
                    event_summary = event['summary'] if 'summary' in event else 'No Title'
                    print('Found event:', event_summary)
                    print('Event starts:', start)
                    time_delta = event_start - current_time
                    event['num_minutes'] = time_delta.total_seconds() // 60
                    return event

# def print_events(events):
#     print('Getting the upcoming 10 events')
#     if not events:
#         print('No upcoming events found.')
#     for event in events:
#         start = event['start'].get('dateTime', event['start'].get('date'))
#         print(start, event['summary'])
#         print(has_reminder_override(event))


def has_reminder_override(event):
    has_default_reminder = event['reminders'].get('useDefault')
    if has_default_reminder:
        return False
    else:
        overrides = event['reminders'].get('overrides')
        if overrides:
            return True
    return False





# this is pasted from github
# TODO: adapt to blinkt, etc.
def get_next_event(num_minutes):
    global has_error
    global reboot_counter

    print(datetime.datetime.now().strftime('%a %b %d %I:%M:%S%p'), 'Getting next event')

    try:
        creds = get_credentials()
        event_list = get_events(creds, num_minutes)
        flash_all(SUCCESS_COLOR)

        has_error = False
        reboot_counter = 0;
        if not event_list:
            print(datetime.datetime.now(), 'No entries returned')
            return None
        else:
            get_event_with_reminder(event_list)
    except Exception as e:
        print('\nException type:', type(e))
        print('Error:', sys.exc_info()[0])
        flash_all(FAILURE_COLOR)
        has_error = True
        if REBOOT_COUNTER_ENABLED:
            reboot_counter += 1
            print('Incrementing the reboot counter ({})'.format(reboot_counter))
            if reboot_counter == REBOOT_NUM_RETRIES:
                # Reboot the Pi
                for i in range(1, 10):
                    print('Rebooting in {} seconds'.format(i))
                    time.sleep(1)
                os.system("sudo reboot")

    return None


#### LIGHT FUNCTIONS
        
def flash_light():
    while True:
        for i in range(8):
            clear()
            set_pixel(i, 255, 0, 0)
            show()
            time.sleep(0.05)


def flash_all(color):
    clear()
    set_all(color[0], color[1], color[2], 0.1)
    show()
    time.sleep(1)
    clear()


def main():
    get_next_event(10)
    
if __name__ == '__main__':
    main() 