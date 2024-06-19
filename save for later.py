import cv2
from tkinter import Tk, Label
from PIL import Image, ImageTk

# Function to convert OpenCV image to Tkinter-compatible format
def cv2_to_tkinter(cv_img):
    # Convert the image from BGR to RGB format
    cv_img_rgb = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    # Convert the image to a PIL Image
    pil_img = Image.fromarray(cv_img_rgb)
    # Convert the PIL Image to a Tkinter Image
    tk_img = ImageTk.PhotoImage(image=pil_img)
    return tk_img

# Load an image using OpenCV
cv_img = cv2.imread('path_to_your_image.jpg')  # Provide the path to your image file

# Create a Tkinter window
window = Tk()
window.title("OpenCV Image in Tkinter")

# Convert the OpenCV image to a Tkinter-compatible image
tk_img = cv2_to_tkinter(cv_img)

# Create a Label widget to display the image
label = Label(window, image=tk_img)
label.pack()

# Function to update the image in the Tkinter window (if needed)
def update_image(new_cv_img):
    new_tk_img = cv2_to_tkinter(new_cv_img)
    label.config(image=new_tk_img)
    label.image = new_tk_img

# Start the Tkinter event loop
window.mainloop()

###################################################################################################

import threading
import cv2
import time

# Dummy functions for drone control and video processing
def control_drone(event):
    while not event.is_set():
        # Drone control logic
        print("Drone control thread is running")
        time.sleep(1)

def process_video(event):
    while not event.is_set():
        # Video processing logic
        print("Video processing thread is running")
        time.sleep(1)

# Create a class for the GUI
class DroneGUI:
    def __init__(self):
        # Initialize the GUI here
        pass

    def start(self):
        # Start the GUI main loop
        self.running = True
        self.run()

    def stop(self):
        # Stop the GUI main loop
        self.running = False

    def run(self):
        while self.running:
            # Update GUI elements
            # Handle user input
            # Communicate with drone control and video processing threads
            print("GUI thread is running")
            time.sleep(1)

# Create events for synchronization
control_event = threading.Event()
video_event = threading.Event()

# Start drone control and video processing threads
control_thread = threading.Thread(target=control_drone, args=(control_event,))
video_thread = threading.Thread(target=process_video, args=(video_event,))
control_thread.start()
video_thread.start()

# Create and start the GUI
gui = DroneGUI()
gui.start()

# When the GUI is closed, set events to stop other threads
gui.stop()
control_event.set()
video_event.set()

# Wait for the threads to finish
control_thread.join()
video_thread.join()

print("Application terminated")