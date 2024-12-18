import os
import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

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
        return service

