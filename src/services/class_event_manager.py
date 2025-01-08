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

from src.services.base_event_manager import GoogleEventsManager
from src.utils.event_class import CalendarEvent

SCOPES = ["https://www.googleapis.com/auth/calendar"]
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

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
