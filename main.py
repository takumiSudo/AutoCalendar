import os
import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from src.service import manageEvents



def main():
    json = "client_secret.json"
    if os.path.exists(json):
        service = manageEvents.GoogleCalendarService(json)
    else:
        raise Exception("An error occurred.")
    
    service.run_continuously()

    





if __name__ == "__main__":
    main()