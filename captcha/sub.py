import subprocess
from datetime import datetime
import os

def take_macos_screenshot():
    """
    On macOS, this will invoke the native screenshot UI
    where you can click and drag to select a region.
    """
    # Generate a timestamp for the screenshot filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"myscreenshot_{timestamp}.png"
    
    # Specify the directory where the screenshot will be stored
    directory = "/Users/tss_02/Desktop/INITIAL/snapcal/screenshots"
    os.makedirs(directory, exist_ok=True)  # Create the directory if it doesn't exist
    
    # Full path to the screenshot file
    filepath = os.path.join(directory, filename)
    
    # -i = interactive: prompt the user to select the area
    # -s = only capture the selected area
    cmd = ["screencapture", "-i", "-s", filepath]
    subprocess.run(cmd)
    
if __name__ == "__main__":
    take_macos_screenshot()