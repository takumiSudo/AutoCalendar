# Main Routine
import json
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import datetime
from dotenv import load_dotenv

load_dotenv()

from src.services.class_event_manager import GCalEventManagerAgent
from src.utils.event_class import EventDateTime, CalendarEvent

IMAGE_DIRECTORY = "screenshots"

class ImageHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            file_path = event.src_path

            print(f"New Image Detected: {file_path}")

            agent = GCalEventManagerAgent()
            result = agent.photo2event(file_path)
            print(json.dumps(result.model_dump()))
            agent.create_event(result.model_dump())

def start_watching():

    event_handler = ImageHandler()
    observer = Observer()
    observer.schedule(event_handler, IMAGE_DIRECTORY, recursive=False)
    observer.start()

    print(f"Watching directory: {IMAGE_DIRECTORY}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    start_watching()
    

        




    

