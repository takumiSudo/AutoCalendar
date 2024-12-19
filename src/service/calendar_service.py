import os
import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from typing import Optional, Dict, Any
import json
import logging 

# Configure the logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("example.log"),  # Log to a file
                        logging.StreamHandler()  # Log to console
                    ])

logger = logging.getLogger(__name__)

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
        self.run_continuously()

    def authenticate(self):
        """
        Handle user authentication and build the Calendar API service.
        """
        creds = None
        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_file(self.token_file, SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_file, SCOPES)
                creds = flow.run_local_server(port=0)
            
            with open(self.token_file, 'w') as token:
                token.write(creds.to_json())
        
        service = build('calendar', 'v3', credentials=creds)
        logger.info("Session successfully created.")
        return service

    def create_event(self, calendar_id = 'primary', event_body= Optional([str, Any])):

        if not event_body['start'] or not event_body['end']:
            event_body['start']['dateTime']: datetime.datetime.utcnow().isoformat()
            start = datetime.datetime.utcnow().isoformat()
            event_body['end']['dateTime']: start + datetime.timedelta(hours=1)

        # TODO: Make a Human Checker to see if the Schedule is correct, and also an UI 
        # So that they can change/add details if they want to
        event_body = self._user_check(event_body)

        try: 
            event = self.service.events().insert(
                calendarId = calendar_id, body = event_body
            ).execute()
            logger.info("Event Created", event.get('htmlLink'))
            return event
        except HttpError as error:
            logger.info(f"An error occurred while creating event: {error}")
            return None

        
    
    def _user_check(self, event_body = Optional([str, Any])):

        pass
        