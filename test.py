from __future__ import print_function
import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']

def main():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())


# Build the Calendar API service
    service = build('calendar', 'v3', credentials=creds)

    # Example: get upcoming events
    events_result = service.events().list(
        calendarId='primary', 
        timeMin='2024-01-01T00:00:00Z',  # or dynamically compute the timeMin
        maxResults=10, 
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    events = events_result.get('items', [])

    if not events:
        print("No upcoming events found.")
    else:
        print("Upcoming events:")
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])

    # Example: create a new event
    event = {
      'summary': 'Automated Task Demo',
      'location': 'Online',
      'description': 'Demo event created by Python script',
      'start': {
        'dateTime': '2024-01-10T09:00:00-07:00',
        'timeZone': 'America/Denver',
      },
      'end': {
        'dateTime': '2024-01-10T10:00:00-07:00',
        'timeZone': 'America/Denver',
      },
      'reminders': {
        'useDefault': False,
        'overrides': [
          {'method': 'email', 'minutes': 24 * 60},
          {'method': 'popup', 'minutes': 10},
        ],
      },
    }

    event_result = service.events().insert(calendarId='primary', body=event).execute()
    print(f'Event created: {event_result.get("htmlLink")}')

if __name__ == '__main__':
    main()