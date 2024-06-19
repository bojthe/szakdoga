import droneControl
import videoProcessing
import threading
import cv2
import tkinter
from PIL import Image, ImageTk

angleOkEvent = threading.Event()
distanceOkEvent = threading.Event()
verticalOkEvent = threading.Event()
horizontalOkEvent = threading.Event()
turnClockwiseEvent = threading.Event()
turnCounterClockwiseEvent = threading.Event()
moveLeftEvent = threading.Event()
moveRightEvent = threading.Event()
moveUpEvent = threading.Event()
moveDownEvent = threading.Event()
moveForwardEvent = threading.Event()
moveBackwardEvent = threading.Event()
decodeQrEvent = threading.Event()
failedEvent = threading.Event()

class ControlGUI:

    def __init__(self):
        self.window = tkinter.Tk()
        self.window.geometry("800x540")
        self.window.columnconfigure(0, weight=3)
        self.window.columnconfigure(1, weight=1)
        self.window.rowconfigure(0, weight=9)
        self.window.rowconfigure(1, weight=1)

        self.videoFrame = tkinter.Frame(self.window)
        self.videoFrame.configure(background="yellow")
        self.videoFrame.grid(column=0,row=0, sticky='nesw')
        self.videoFrame.rowconfigure(1, weight=1)
        self.controlsFrame = tkinter.Frame(self.window)
        self.controlsFrame.configure(background="red")
        self.controlsFrame.grid(column=1, row=0, rowspan=2, sticky='nesw')
        self.controlsFrame.rowconfigure(0, weight=1)
        self.controlsFrame.rowconfigure(2, weight=1)
        self.controlsFrame.rowconfigure(3, weight=1)
        self.controlsFrame.rowconfigure(4, weight=1)
        self.controlsFrame.rowconfigure(5, weight=1)
        self.controlsFrame.columnconfigure(0, weight=1)
        self.controlsFrame.columnconfigure(1, weight=1)
        self.controlsFrame.columnconfigure(2, weight=1)

        self.videoLabel = tkinter.Label(self.videoFrame, text="Video Feed")
        self.videoLabel.grid(column=0,row=0)
        self.videoFeed = tkinter.Label(self.videoFrame)
        self.videoFeed.grid(column=0, row=1)

        self.takeOffButton = tkinter.Button(self.controlsFrame, relief=tkinter.RAISED,
                                            command=self.__takeOffButtonClicked, text="Take Off" )
        #command = self.__takeOffButtonClicked, text = "Take Off" )
        self.landButton = tkinter.Button(self.controlsFrame, relief=tkinter.RAISED, state=tkinter.DISABLED,
                                         command=self.__landButtonClicked, text="Land" )
        #command = self.__landButtonClicked, text = "Land" )
        self.turnClockwiseButton = tkinter.Button(self.controlsFrame, relief=tkinter.RAISED, state=tkinter.DISABLED,
                                                  command=self.__turnClockwiseButtonClicked, text="Clockwise")
        #command=self.__turnClockwiseButtonClicked, text="Clockwise")
        self.turnCounterclockwiseButton = tkinter.Button(self.controlsFrame, relief=tkinter.RAISED, state=tkinter.DISABLED,
                                                         command=self.__turnCounterclockwiseButtonClicked, text="Counterclockwise")
        #command=self.__turnCounterclockwiseButtonClicked, text="Counterclockwise")
        self.moveForwardButton = tkinter.Button(self.controlsFrame, relief=tkinter.RAISED, state=tkinter.DISABLED,
                                                command=self.__moveForwardButtonClicked, text="Forward")
        #command=self.__moveForwardButtonClicked, text="Forward")
        self.moveBackwardButton = tkinter.Button(self.controlsFrame, relief=tkinter.RAISED, state=tkinter.DISABLED,
                                                 command=self.__moveBackwardButtonClicked, text="Backward")
        #command=self.__moveBackwardButtonClicked, text="Backward")
        self.moveLeftButton = tkinter.Button(self.controlsFrame, relief=tkinter.RAISED, state=tkinter.DISABLED,
                                             command=self.__moveLeftButtonClicked, text="Left")
        #command=self.__moveLeftButtonClicked, text="Left")
        self.moveRightButton = tkinter.Button(self.controlsFrame, relief=tkinter.RAISED, state=tkinter.DISABLED,
                                              command=self.__moveRightButtonClicked, text="Right")
        #command=self.__moveRightButtonClicked, text="Right")
        self.stopButton = tkinter.Button(self.controlsFrame, relief=tkinter.RAISED, state=tkinter.DISABLED,
                                         command=self.__stopButtonClicked, text="Stop")
        #command=self.__stopButtonClicked, text="Stop")
        self.ascendButton = tkinter.Button(self.controlsFrame, relief=tkinter.RAISED, state=tkinter.DISABLED,
                                           command=self.__ascendButtonClicked, text="Ascend")
        #command=self.__ascendButtonClicked, text="Ascend")
        self.descendButton = tkinter.Button(self.controlsFrame, relief=tkinter.RAISED, state=tkinter.DISABLED,
                                            command=self.__descendButtonClicked, text="Descend")
        #command=self.__descendButtonClicked, text="Descend")
        self.correctionButton = tkinter.Button(self.controlsFrame, relief=tkinter.RAISED, state=tkinter.DISABLED,
                                               command=self.__correctionButtonClicked, text="Correction")
        #command=self.__correctionButtonClicked, text="Correction")

        self.takeOffButton.grid(column=0, row=2, sticky='nesw')
        self.correctionButton.grid(column=1, row=2, sticky='nesw')
        self.landButton.grid(column=2, row=2, sticky='nesw')
        self.turnClockwiseButton.grid(column=0, row=3, sticky='nesw')
        self.turnCounterclockwiseButton.grid(column=2, row=3, sticky='nesw')
        self.moveForwardButton.grid(column=1, row=3, sticky='nesw')
        self.moveBackwardButton.grid(column=1, row=5, sticky='nesw')
        self.moveLeftButton.grid(column=0, row=4, sticky='nesw')
        self.moveRightButton.grid(column=2, row=4, sticky='nesw')
        self.stopButton.grid(column=1, row=4, sticky='nesw')
        self.ascendButton.grid(column=0, row=5, sticky='nesw')
        self.descendButton.grid(column=2, row=5, sticky='nesw')

        self.window.mainloop()

    def __takeOffButtonClicked(self):
        pass

    def __landButtonClicked(self):
        pass

    def __turnClockwiseButtonClicked(self):
        pass

    def __turnCounterclockwiseButtonClicked(self):
        pass

    def __moveForwardButtonClicked(self):
        pass

    def __moveBackwardButtonClicked(self):
        pass

    def __moveLeftButtonClicked(self):
        pass

    def __moveRightButtonClicked(self):
        pass

    def __stopButtonClicked(self):
        pass

    def __ascendButtonClicked(self):
        pass

    def __descendButtonClicked(self):
        pass

    def __correctionButtonClicked(self):
        pass


def cv2ToTkinter(cv_img):
    # Convert the image from BGR to RGB format
    cv_img_rgb = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    # Convert the image to a PIL Image
    pil_img = Image.fromarray(cv_img_rgb)
    # Convert the PIL Image to a Tkinter Image
    tk_img = ImageTk.PhotoImage(image=pil_img)
    return tk_img

def updateImage(img, label):
    label.config(image=img)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #print("[main thread] Creating controller thread")
    #controller = droneControl.DroneController(angleOkEvent, distanceOkEvent, verticalOkEvent, horizontalOkEvent,
    #                                         turnClockwiseEvent, turnCounterClockwiseEvent, moveLeftEvent, moveRightEvent,
    #                                          moveUpEvent, moveDownEvent, moveForwardEvent, moveBackwardEvent,
    #                                          decodeQrEvent, failedEvent)
    #flyingThread = threading.Thread(target=controller.flyAutomatic, daemon=True)
    #flyingThread.start()
#
    #processor = videoProcessing.videoProcessor(angleOkEvent, distanceOkEvent, verticalOkEvent, horizontalOkEvent,
    #                                          turnClockwiseEvent, turnCounterClockwiseEvent, moveLeftEvent, moveRightEvent,
    #                                          moveUpEvent, moveDownEvent, moveForwardEvent, moveBackwardEvent,
    #                                          decodeQrEvent, failedEvent)
    #videoProcessingThread = threading.Thread(target=processor.process, daemon=True)
    #videoProcessingThread.start()
#
    #flyingThread.join()
    #videoProcessingThread.join()
    #cv_img = cv2.imread("pic8.jpg")
    #window = Tk()
    #window.title("Placeholder Title")

    #tk_img = cv2_to_tkinter(cv_img)

    #label = Label(window, image=tk_img)
    #label.pack()

    #window.mainloop()
    ControlGUI()