# Google Calendar Event Manager Base Class
# Authored: 01/08/25

import datetime
import os.path
from typing import Optional
import json
import base64


from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from openai import OpenAI
import logging
from pydantic import BaseModel

SCOPES = ["https://www.googleapis.com/auth/calendar"]

class GoogleEventsManager:

    def __init__(self):
        self.service = self.authenticate()

    def authenticate(self):
        """
        Default Startup to Link Google Account, and access API 
        """
        creds = None
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(creds.to_json())

        try: 
            service = build("calendar", "v3", credentials=creds)
        except HttpError as e:
            print(f"An error occurred: {e}")

        return service

    def create_event(self, summary: str, start_time: str, end_time: str, description: Optional[str] = None, location: Optional[str] = None):
        """
        Create a new event in the user's calendar.
        Refactor into Dataloader so Json structure can be inputted
        """
        event = {
            'summary': summary,
            'start': {
                'dateTime': start_time,
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': end_time,
                'timeZone': 'UTC',
            },
            'description': description,
            'location': location,
        }

        try:
            event = self.service.events().insert(calendarId='primary', body=event).execute()
            print(f"Event created: {event.get('htmlLink')}")
        except HttpError as error:
            print(f"An error occurred: {error}")

