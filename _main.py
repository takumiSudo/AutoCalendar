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

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

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



class DataLoader:
    def __init__(self, summary: str, start_time: str, end_time: str, description: Optional[str] = None, location: Optional[str] = None):
        self.summary = summary
        self.start_time = start_time
        self.end_time = end_time
        self.description = description
        self.location = location

class CalendarEvent(BaseModel):
    summary: str 
    start_time: str
    end_time: str
    description: str
    location: str


class GCalEventMangerAgent(GoogleEventsManager):

    def __init__(self):
        super().__init__()
        self.agent = self.setup_agent()

    def setup_agent(self)-> OpenAI:
        try:
            client = OpenAI(
                api_key=os.getenv("OPENAI_API_KEY")
            )
            logger.info("oAI Agent Setup Complete")
        except Exception as e:
            logger.error(f"Error while setting up: {e}")
            raise
        return client

    def input2event(self, input = str):
        """
        Function to create gooogle calendar event jsons, via llm agent
        """
        try:
            chat_completion = self.agent.beta.chat.completions.parse(
                model="gpt-4o-2024-08-06",
                messages=[
                    {
                        "role": "user",
                        "content": input,
                    }
                ],
                response_format=CalendarEvent,
            )

            return chat_completion.choices[0].message.parsed
        except Exception as e:
            logger.error("Error: {e}")
            raise

    def photo2event(self, photo_path: str):

        try:
            base64_image = encode_image(photo_path)
            chat_completion = self.agent.beta.chat.completions.parse(
                model="gpt-4o-2024-08-06",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type" : "text",
                                "text" : "Create a Calendar Event according to the photo",
                            },
                            {
                                "type" : "image_url",
                                "image_url" : {"url": f"data:image/jpeg;base64,{base64_image}"}
                            }
                        ]
                    }
                ],
                response_format=CalendarEvent,
            )

            return chat_completion.choices[0].message.parsed
        except Exception as e:
            logger.error("Error: {e}")
            raise

    def create_event(self, event: json):

        try: 
            event = self.service.events().insert(calendarId='primary', body=event).execute()
            print(f"Event created: {event.get('htmlLink')}")
        except HttpError as error:
            print(f"An error occurred: {error}")


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


if __name__ == "__main__":


    # # 1. first test 
    events_manager= GCalEventMangerAgent()
    # summary = "みのんとご飯"
    # start_time = "2025-01-08T12:00:00"
    # end_time = "2025-01-08T13:00:00"
    # description = "Discuss project updates"
    # location = "None"
    # events_manager.create_event(summary, start_time, end_time, description, location)

    # logger.info("Successfully passed first test")

    # # 2. Try out the agent
    # result = events_manager.input2event("I am going to the movie this friday")
    # print(json.dumps(result.model_dump()))

    # logger.info("Successfully passed 2nd test")

    # 3. Try out the agent
    result = events_manager.photo2event("test-img.png")
    print(json.dumps(result.model_dump()))
    events_manager.create_event(result.model_dump())