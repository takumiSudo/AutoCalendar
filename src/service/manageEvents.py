import os
import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# The scopes your app needs (read/write access to Calendar)
SCOPES = ['https://www.googleapis.com/auth/calendar']

class GoogleCalendarService:
    def __init__(self, credentials_file='credentials.json', token_file='token.json'):
        """
        Initialize the Google Calendar service client.
        :param credentials_file: Path to your OAuth2 credentials JSON file.
        :param token_file: Path to the token JSON file where
                           the user's access/refresh tokens are stored.
        """
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.service = self.authenticate()

    def authenticate(self):
        """
        Handle user authentication and build the Calendar API service.
        """
        creds = None
        # Load credentials from token file if it exists
        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_file(self.token_file, SCOPES)
        
        # If there's no (valid) token available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                # Refresh token if expired
                creds.refresh(Request())
            else:
                # Prompt for login if no valid credentials
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_file, SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save the credentials for the next run
            with open(self.token_file, 'w') as token:
                token.write(creds.to_json())
        
        # Build the service object
        service = build('calendar', 'v3', credentials=creds)
        return service

    def list_events(self, calendar_id='primary', max_results=10):
        """
        List the next N upcoming events on the user's calendar.
        """
        try:
            now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
            events_result = self.service.events().list(
                calendarId=calendar_id, timeMin=now,
                maxResults=max_results, singleEvents=True,
                orderBy='startTime').execute()
            events = events_result.get('items', [])
            return events
        except HttpError as error:
            print(f"An error occurred while listing events: {error}")
            return []

    def create_event(self, calendar_id='primary', summary='New Event', description='', 
                     start_time=None, end_time=None):
        """
        Create a new event on the user's calendar.
        """
        if not start_time or not end_time:
            # Default to an event starting now, ending in 1 hour
            start_time = datetime.datetime.utcnow()
            end_time = start_time + datetime.timedelta(hours=1)
        
        event_body = {
            'summary': summary,
            'description': description,
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': 'UTC',
            },
        }

        try:
            event = self.service.events().insert(
                calendarId=calendar_id, body=event_body
            ).execute()
            print("Event created:", event.get('htmlLink'))
            return event
        except HttpError as error:
            print(f"An error occurred while creating event: {error}")
            return None

    def delete_event(self, calendar_id='primary', event_id=None):
        """
        Delete an event from the calendar.
        """
        if not event_id:
            print("No event_id provided.")
            return None
        try:
            response = self.service.events().delete(
                calendarId=calendar_id, eventId=event_id
            ).execute()
            print(f"Event {event_id} deleted.")
            return response
        except HttpError as error:
            print(f"An error occurred while deleting event: {error}")
            return None

    def run_continuously(self):
        """
        Example method that keeps the service 'alive'. 
        You could use this to listen for CLI input or an API framework.
        """
        print("Running continuously. Type commands (list, create, delete, exit)...")
        while True:
            user_input = input("> ").strip()
            if user_input == "list":
                events = self.list_events()
                for idx, evt in enumerate(events):
                    start = evt['start'].get('dateTime', evt['start'].get('date'))
                    print(f"{idx+1}. {evt.get('summary')} at {start}")
            elif user_input == "create":
                self.create_event(summary="Docker Listening Event")
            elif user_input.startswith("delete"):
                _, event_id = user_input.split()
                self.delete_event(event_id=event_id)
            elif user_input == "exit":
                print("Exiting continuous loop.")
                break
            else:
                print("Unknown command. Try 'list', 'create', 'delete <event_id>', or 'exit'.")

