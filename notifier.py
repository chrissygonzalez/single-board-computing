from __future__ import print_function
import datetime
import pickle
import os
import sys
import time
import pytz
from dateutil import parser
from subprocess import call
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from blinkt import set_pixel, set_all, set_brightness, show, clear


#### CONSTANTS
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
CALENDAR_ID = 'family11329664508214213018@group.calendar.google.com'
FIRST_ALERT = 9
SECOND_ALERT = 4
THIRD_ALERT = 1

REBOOT_COUNTER_ENABLED = False
REBOOT_NUM_RETRIES = 10


#### GLOBAL VARIABLES
reboot_counter = 0  # counter variable, tracks retry events.
has_error = False


#### CALENDAR FUNCTIONS (https://developers.google.com/google-apps/calendar/quickstart/python)

def get_credentials():
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
        event_summary = event['summary'] if 'summary' in event else 'No Title'
        if start:
            event_start = parser.parse(start)
            print(event_start)
            if current_time < event_start:
                if has_reminder(event):
                    print('Found event:', event_summary)
                    print('Event starts:', start)
                    time_delta = event_start - current_time
                    event['num_minutes'] = time_delta.total_seconds() // 60
                    return event
                else:
                    print(event_summary, 'has no reminder set')
            else:
                print(event_summary, 'is in progress')


def has_reminder(event):
    has_default_reminder = event['reminders'].get('useDefault')
    
    if has_default_reminder:
        return True
    else:
        overrides = event['reminders'].get('overrides')
        if overrides:
            return True
    return False



def get_next_event(num_minutes):
    global has_error
    global reboot_counter

    print(datetime.datetime.now().strftime('%a %b %d %I:%M:%S%p'), 'Getting next event')

    try:
        creds = get_credentials()
        event_list = get_events(creds, num_minutes)
#         flash_all(SUCCESS_COLOR)
        has_error = False
        reboot_counter = 0;
        if not event_list:
            print(datetime.datetime.now(), 'No entries returned')
            return None
        else:
            return get_event_with_reminder(event_list)
    except Exception as e:
        print('\nException type:', type(e))
        print('Error:', sys.exc_info()[0])
#         flash_all(FAILURE_COLOR)
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


#### LIGHT & SOUND FUNCTIONS

def beep():
    beepcmd = "play -n synth 0.3 sine A 2>/dev/null"
    os.system(beepcmd)
    
def unconvinced():
    notifycmd = "play unconvinced-569.mp3 2>/dev/null"
    os.system(notifycmd)
    
def quiteimpressed():
    notifycmd = "play quite-impressed-565.mp3 2>/dev/null"
    os.system(notifycmd)
    
def holdon():
    notifycmd = "play hold-on-560.mp3 2>/dev/null"
    os.system(notifycmd)
    
def speak_reminder(num_minutes, summary):
    cmd_beg = 'espeak -ven-us -s120 '
    cmd_end = ' 2>/dev/null'
    num = int(num_minutes)
    num_str = str(num)
    words = summary + " starts in " + num_str + " minutes"
    words = words.replace(' ','_')
    call([cmd_beg + words + cmd_end], shell=True)
        
    
def main():
    last_minute = datetime.datetime.now().minute
    # on startup, just use the previous minute as lastMinute
    if last_minute == 0:
        last_minute = 59
    else:
        last_minute -= 1
        
    # infinite loop to continuously check Google Calendar for future entries
    while 1:
        current_minute = datetime.datetime.now().minute
        if current_minute != last_minute:
            last_minute = current_minute
            next_event = get_next_event(11)
            if next_event is not None:
                num_minutes = next_event['num_minutes']
                summary = next_event['summary'] if 'summary' in next_event else 'No Title'
                print(num_minutes)
                if num_minutes == FIRST_ALERT:
                    unconvinced()
                    time_until = num_minutes + 1
                    speak_reminder(time_until, summary)

                elif num_minutes == SECOND_ALERT:
                    quiteimpressed()
                    time_until = num_minutes + 1
                    speak_reminder(time_until, summary)

                elif num_minutes == THIRD_ALERT:
                    holdon()
                    time_until = num_minutes + 1
                    speak_reminder(time_until, summary)

        time.sleep(2)
           
print('STARTING UP THE PI REMINDER')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nSee you later!\n')
        sys.exit(0) 