import droneControl
import videoProcessing
import threading
import cv2
import tkinter
import tktooltip
import queue
from PIL import Image, ImageTk

ICON_SIZE = 30

angleOkEvent = threading.Event()
distanceOkEvent = threading.Event()
verticalOkEvent = threading.Event()
horizontalOkEvent = threading.Event()
takeoffEvent = threading.Event()
landEvent = threading.Event()
stopEvent = threading.Event()
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
correctionEvent = threading.Event()

stopVideoEvent = threading.Event()
stopDroneEvent = threading.Event()
videoQueue = queue.Queue(maxsize=10)

def cv2ToTkinter(cv_img):
    # Convert the image from BGR to RGB format
    cv_img_rgb = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    # Convert the image to a PIL Image
    pil_img = Image.fromarray(cv_img_rgb)
    # Convert the PIL Image to a Tkinter Image
    tk_img = ImageTk.PhotoImage(image=pil_img)
    return tk_img

class ControlGUI:

    def __init__(self):
        ### Keeping track of the last entities we have interacted with
        self.lastEventSet = None
        self.lastActiveButton = None

        ### Building the GUI
        self.window = tkinter.Tk()
        self.window.title("Drone Panel")
        self.window.geometry("1465x750")
        self.window.columnconfigure(0, weight=6)
        self.window.columnconfigure(1, weight=1)
        self.window.rowconfigure(0, weight=1)
        self.defaultColor = self.window.cget("bg")

        ### Frame Containing the Video
        self.videoFrame = tkinter.Frame(self.window)
        self.videoFrame.grid(column=0,row=0, sticky='nesw')
        self.videoFrame.rowconfigure(0, weight=0)
        self.videoFrame.rowconfigure(1, weight=1)
        self.videoFrame.columnconfigure(0, weight=1)
        self.videoLabel = tkinter.Label(self.videoFrame, text="Video Feed")
        self.videoLabel.grid(column=0, row=0, sticky='new')
        self.videoFeed = tkinter.Label(self.videoFrame)
        self.videoFeed.configure(background="black")
        self.videoFeed.grid(column=0, row=1, sticky='nesw')


        ### Frame containing the Drone Controls
        self.controlsFrame = tkinter.Frame(self.window)
        self.controlsFrame.grid(column=1, row=0, sticky='nesw')
        self.controlsFrame.rowconfigure(1, weight=5)
        self.controlsFrame.rowconfigure(3, weight=1)
        self.controlsFrame.rowconfigure(4, weight=1)
        self.controlsFrame.rowconfigure(5, weight=1)
        self.controlsFrame.rowconfigure(6, weight=1)
        self.controlsFrame.columnconfigure(0, weight=1)
        self.controlsFrame.columnconfigure(1, weight=1)
        self.controlsFrame.columnconfigure(2, weight=1)
        self.controlsLabel = tkinter.Label(self.controlsFrame, text="Drone Controls")
        self.controlsLabel.grid(column=0, row=2, columnspan=3, sticky='nesw')
        self.tipsHeaderLabel = tkinter.Label(self.controlsFrame, text="Description")
        self.tipsHeaderLabel.grid(column=0, row=0, columnspan=3, sticky='nesw')
        self.tipsLabel = tkinter.Label(self.controlsFrame, state=tkinter.DISABLED)
        self.tipsLabel.grid(column=0, row=1, columnspan=3, sticky='nesw')

        ### Retrieving the icons needed for the control buttons
        takeOffIcon = ImageTk.PhotoImage(Image.open(".\\Icons\\plane-departure.png").resize((ICON_SIZE, ICON_SIZE)))
        correctionIcon = ImageTk.PhotoImage(Image.open(".\\Icons\\qr.png").resize((ICON_SIZE, ICON_SIZE)))
        landIcon = ImageTk.PhotoImage(Image.open(".\\Icons\\plane-arrival.png").resize((ICON_SIZE, ICON_SIZE)))
        turnClockwiseIcon = ImageTk.PhotoImage(Image.open(".\\Icons\\rotate-right.png").resize((ICON_SIZE, ICON_SIZE)))
        turnCounterclockwiseIcon = ImageTk.PhotoImage(Image.open(".\\Icons\\rotate-left.png").resize((ICON_SIZE, ICON_SIZE)))
        moveForwardIcon = ImageTk.PhotoImage(Image.open(".\\Icons\\arrow-circle-up.png").resize((ICON_SIZE, ICON_SIZE)))
        moveBackwardIcon = ImageTk.PhotoImage(Image.open(".\\Icons\\arrow-circle-down.png").resize((ICON_SIZE, ICON_SIZE)))
        moveLeftIcon = ImageTk.PhotoImage(Image.open(".\\Icons\\arrow-circle-left.png").resize((ICON_SIZE, ICON_SIZE)))
        moveRightIcon = ImageTk.PhotoImage(Image.open(".\\Icons\\arrow-circle-right.png").resize((ICON_SIZE, ICON_SIZE)))
        stopIcon = ImageTk.PhotoImage(Image.open(".\\Icons\\stop-circle.png").resize((ICON_SIZE, ICON_SIZE)))
        ascendIcon = ImageTk.PhotoImage(Image.open(".\\Icons\\sort-circle-up.png").resize((ICON_SIZE, ICON_SIZE)))
        descendIcon = ImageTk.PhotoImage(Image.open(".\\Icons\\sort-circle-down.png").resize((ICON_SIZE, ICON_SIZE)))

        ### Creating and binding the control buttons
        self.takeOffButton = tkinter.Button(self.controlsFrame, relief=tkinter.RAISED,
                                            command=self.__takeOffButtonClicked, image=takeOffIcon )
        self.landButton = tkinter.Button(self.controlsFrame, relief=tkinter.RAISED, state=tkinter.DISABLED,
                                         command=self.__landButtonClicked, image=landIcon )
        self.turnClockwiseButton = tkinter.Button(self.controlsFrame, relief=tkinter.RAISED, state=tkinter.DISABLED,
                                                  command=self.__turnClockwiseButtonClicked, image=turnClockwiseIcon)
        self.turnCounterclockwiseButton = tkinter.Button(self.controlsFrame, relief=tkinter.RAISED, state=tkinter.DISABLED,
                                                         command=self.__turnCounterclockwiseButtonClicked, image=turnCounterclockwiseIcon)
        self.moveForwardButton = tkinter.Button(self.controlsFrame, relief=tkinter.RAISED, state=tkinter.DISABLED,
                                                command=self.__moveForwardButtonClicked, image=moveForwardIcon)
        self.moveBackwardButton = tkinter.Button(self.controlsFrame, relief=tkinter.RAISED, state=tkinter.DISABLED,
                                                 command=self.__moveBackwardButtonClicked, image=moveBackwardIcon)
        self.moveLeftButton = tkinter.Button(self.controlsFrame, relief=tkinter.RAISED, state=tkinter.DISABLED,
                                             command=self.__moveLeftButtonClicked, image=moveLeftIcon)
        self.moveRightButton = tkinter.Button(self.controlsFrame, relief=tkinter.RAISED, state=tkinter.DISABLED,
                                              command=self.__moveRightButtonClicked, image=moveRightIcon)
        self.stopButton = tkinter.Button(self.controlsFrame, relief=tkinter.RAISED, state=tkinter.DISABLED,
                                         command=self.__stopButtonClicked, image=stopIcon)
        self.ascendButton = tkinter.Button(self.controlsFrame, relief=tkinter.RAISED, state=tkinter.DISABLED,
                                           command=self.__ascendButtonClicked, image=ascendIcon)
        self.descendButton = tkinter.Button(self.controlsFrame, relief=tkinter.RAISED, state=tkinter.DISABLED,
                                            command=self.__descendButtonClicked, image=descendIcon)
        self.correctionButton = tkinter.Button(self.controlsFrame, relief=tkinter.RAISED, state=tkinter.DISABLED,
                                               command=self.__correctionButtonClicked, image=correctionIcon)

        ### Placing the buttons on a grid
        self.takeOffButton.grid(column=0, row=3, sticky='nesw')
        self.correctionButton.grid(column=1, row=3, sticky='nesw')
        self.landButton.grid(column=2, row=3, sticky='nesw')
        self.turnClockwiseButton.grid(column=0, row=4, sticky='nesw')
        self.turnCounterclockwiseButton.grid(column=2, row=4, sticky='nesw')
        self.moveForwardButton.grid(column=1, row=4, sticky='nesw')
        self.moveBackwardButton.grid(column=1, row=6, sticky='nesw')
        self.moveLeftButton.grid(column=0, row=5, sticky='nesw')
        self.moveRightButton.grid(column=2, row=5, sticky='nesw')
        self.stopButton.grid(column=1, row=5, sticky='nesw')
        self.ascendButton.grid(column=0, row=6, sticky='nesw')
        self.descendButton.grid(column=2, row=6, sticky='nesw')

        ### Tooltips for everything
        tktooltip.ToolTip(self.takeOffButton, msg="Sends a Take Off command to the drone.", delay=2.0)
        tktooltip.ToolTip(self.correctionButton, msg="Initiates the visual input-based position correction process.", delay=2.0)
        tktooltip.ToolTip(self.landButton, msg="Sends a Land command to the drone.", delay=2.0)
        tktooltip.ToolTip(self.turnClockwiseButton, msg="Sends a Clockwise turn command to the drone.", delay=2.0)
        tktooltip.ToolTip(self.turnCounterclockwiseButton, msg="Sends a Counterclockwise turn command to the drone.", delay=2.0)
        tktooltip.ToolTip(self.moveForwardButton, msg="Sends a Forward movement command to the drone.", delay=2.0)
        tktooltip.ToolTip(self.moveBackwardButton, msg="Sends a Backward movement command to the drone.", delay=2.0)
        tktooltip.ToolTip(self.moveLeftButton, msg="Sends a Leftward movement command to the drone.", delay=2.0)
        tktooltip.ToolTip(self.moveRightButton, msg= "Sends a Rightward movement command to the drone.", delay=2.0)
        tktooltip.ToolTip(self.stopButton, msg="Makes the drone stop where it is.", delay=2.0)
        tktooltip.ToolTip(self.ascendButton, msg="Sends an Ascend command to the drone.", delay=2.0)
        tktooltip.ToolTip(self.descendButton, msg="Sends a Descend command to the drone.", delay=2.0)

        # Dialog for choice between Automatic and Manual drone control
        self.isAutomatic = None
        self.dialog = tkinter.Toplevel(self.window)
        self.dialog.title("Chose a startup option!")

        self.dialogLabel = tkinter.Label(self.dialog, text="Please choose a startup option!")
        self.dialogLabel.pack(padx=20, pady=10)

        autoButton = tkinter.Button(self.dialog, text="Automatic", command=lambda: [self.__setIsAutomatic(True), self.__startThreads(), self.dialog.destroy()])
        manualButton = tkinter.Button(self.dialog, text="Manual", command=lambda: [self.__setIsAutomatic(False), self.__startThreads(), self.dialog.destroy()])
        autoButton.pack(side=tkinter.LEFT, padx=10, pady=10)
        manualButton.pack(side=tkinter.RIGHT, padx=10, pady=10)


        # Starting video feed update
        self.__updateImage(videoQueue, stopVideoEvent)

        # Handling close event
        self.window.protocol("WM_DELETE_WINDOW", self.__onClose)

        ### Starting the GUI loop
        self.window.mainloop()

    def __startThreads(self):
        # Creating droneControl and videoProcessing threads
        processor = videoProcessing.videoProcessor(angleOkEvent, distanceOkEvent, verticalOkEvent, horizontalOkEvent,
                                                   turnClockwiseEvent, turnCounterClockwiseEvent, moveLeftEvent,
                                                   moveRightEvent,
                                                   moveUpEvent, moveDownEvent, moveForwardEvent, moveBackwardEvent,
                                                   decodeQrEvent, failedEvent, videoQueue, stopVideoEvent)
        self.videoProcessingThread = threading.Thread(target=processor.process, daemon=True)
        self.videoProcessingThread.start()

        controller = droneControl.DroneController(angleOkEvent, distanceOkEvent, verticalOkEvent, horizontalOkEvent,
                                                  turnClockwiseEvent,
                                                  turnCounterClockwiseEvent, moveLeftEvent, moveRightEvent, moveUpEvent,
                                                  moveDownEvent, moveForwardEvent, moveBackwardEvent, decodeQrEvent,
                                                  failedEvent, stopEvent, stopDroneEvent, takeOffEvent=takeoffEvent,
                                                  landEvent=landEvent, correctionEvent=correctionEvent)

        if self.isAutomatic:
            self.takeOffButton.configure(state=tkinter.DISABLED)
            self.tipsLabel.configure(text="AUTOMATIC MODE\n\nIn this mode you cannot\npilot the drone with\nthe controls provided below.")
            self.droneControlThread = threading.Thread(target=controller.flyAutomatic, daemon=True)
        else:
            self.tipsLabel.configure(text="MANUAL MODE\n\nIn this mode you can\npilot the drone with\nthe controls provided below.\nClick the take off button\nto start!")
            self.droneControlThread = threading.Thread(target=controller.flyManual, daemon=True)
        self.droneControlThread.start()

    def __clearLastCommand(self):
        if self.lastEventSet is not None:
            self.lastEventSet.clear()
            self.lastActiveButton.configure(background=self.defaultColor)

    def __takeOffButtonClicked(self):
        takeoffEvent.set()

        self.takeOffButton.configure(state=tkinter.DISABLED)
        self.correctionButton.configure(state=tkinter.NORMAL)
        self.landButton.configure(state=tkinter.NORMAL)
        self.turnClockwiseButton.configure(state=tkinter.NORMAL)
        self.turnCounterclockwiseButton.configure(state=tkinter.NORMAL)
        self.moveForwardButton.configure(state=tkinter.NORMAL)
        self.moveBackwardButton.configure(state=tkinter.NORMAL)
        self.moveLeftButton.configure(state=tkinter.NORMAL)
        self.moveRightButton.configure(state=tkinter.NORMAL)
        self.stopButton.configure(state=tkinter.NORMAL)
        self.ascendButton.configure(state=tkinter.NORMAL)
        self.descendButton.configure(state=tkinter.NORMAL)

    def __landButtonClicked(self):
        self.__clearLastCommand()
        landEvent.set()

        self.takeOffButton.configure(state=tkinter.NORMAL)
        self.correctionButton.configure(state=tkinter.DISABLED)
        self.landButton.configure(state=tkinter.DISABLED)
        self.turnClockwiseButton.configure(state=tkinter.DISABLED)
        self.turnCounterclockwiseButton.configure(state=tkinter.DISABLED)
        self.moveForwardButton.configure(state=tkinter.DISABLED)
        self.moveBackwardButton.configure(state=tkinter.DISABLED)
        self.moveLeftButton.configure(state=tkinter.DISABLED)
        self.moveRightButton.configure(state=tkinter.DISABLED)
        self.stopButton.configure(state=tkinter.DISABLED)
        self.ascendButton.configure(state=tkinter.DISABLED)
        self.descendButton.configure(state=tkinter.DISABLED)

    def __turnClockwiseButtonClicked(self):
        self.__clearLastCommand()
        if self.lastActiveButton == self.turnClockwiseButton:
            self.lastActiveButton = None
            self.lastEventSet = None
        else:
            self.lastActiveButton = self.turnClockwiseButton
            self.lastActiveButton.configure(background="light blue")
            self.lastEventSet = turnClockwiseEvent
            self.lastEventSet.set()

    def __turnCounterclockwiseButtonClicked(self):
        self.__clearLastCommand()
        if self.lastActiveButton == self.turnCounterclockwiseButton:
            self.lastActiveButton = None
            self.lastEventSet = None
        else:
            self.lastActiveButton = self.turnCounterclockwiseButton
            self.lastActiveButton.configure(background="light blue")
            self.lastEventSet = turnCounterClockwiseEvent
            self.lastEventSet.set()

    def __moveForwardButtonClicked(self):
        self.__clearLastCommand()
        if self.lastActiveButton == self.moveForwardButton:
            self.lastActiveButton = None
            self.lastEventSet = None
        else:
            self.lastActiveButton = self.moveForwardButton
            self.lastActiveButton.configure(background="light blue")
            self.lastEventSet = moveForwardEvent
            self.lastEventSet.set()

    def __moveBackwardButtonClicked(self):
        self.__clearLastCommand()
        if self.lastActiveButton == self.moveBackwardButton:
            self.lastActiveButton = None
            self.lastEventSet = None
        else:
            self.lastActiveButton = self.moveBackwardButton
            self.lastActiveButton.configure(background="light blue")
            self.lastEventSet = moveBackwardEvent
            self.lastEventSet.set()

    def __moveLeftButtonClicked(self):
        self.__clearLastCommand()
        if self.lastActiveButton == self.moveLeftButton:
            self.lastActiveButton = None
            self.lastEventSet = None
        else:
            self.lastActiveButton = self.moveLeftButton
            self.lastActiveButton.configure(background="light blue")
            self.lastEventSet = moveLeftEvent
            self.lastEventSet.set()

    def __moveRightButtonClicked(self):
        self.__clearLastCommand()
        if self.lastActiveButton == self.moveRightButton:
            self.lastActiveButton = None
            self.lastEventSet = None
        else:
            self.lastActiveButton = self.moveRightButton
            self.lastActiveButton.configure(background="light blue")
            self.lastEventSet = moveRightEvent
            self.lastEventSet.set()

    def __stopButtonClicked(self):
        self.__clearLastCommand()
        if self.lastActiveButton == self.stopButton:
            self.lastActiveButton = None
            self.lastEventSet = None
        else:
            self.lastActiveButton = self.stopButton
            self.lastActiveButton.configure(background="light blue")
            self.lastEventSet = stopEvent
            self.lastEventSet.set()

    def __ascendButtonClicked(self):
        self.__clearLastCommand()
        if self.lastActiveButton == self.ascendButton:
            self.lastActiveButton = None
            self.lastEventSet = None
        else:
            self.lastActiveButton = self.ascendButton
            self.lastActiveButton.configure(background="light blue")
            self.lastEventSet = moveUpEvent
            self.lastEventSet.set()

    def __descendButtonClicked(self):
        self.__clearLastCommand()
        if self.lastActiveButton == self.descendButton:
            self.lastActiveButton = None
            self.lastEventSet = None
        else:
            self.lastActiveButton = self.descendButton
            self.lastActiveButton.configure(background="light blue")
            self.lastEventSet = moveDownEvent
            self.lastEventSet.set()

    def __correctionButtonClicked(self):
        self.__clearLastCommand()
        if self.lastActiveButton == self.correctionButton:
            self.lastActiveButton = None
            self.lastEventSet = None
        else:
            self.lastActiveButton = self.correctionButton
            self.lastActiveButton.configure(background="light blue")
            self.lastEventSet = correctionEvent
            self.lastEventSet.set()

    def __updateImage(self, queue, stopEvent):
        if not queue.empty():
            frame = queue.get()
            tk_img = cv2ToTkinter(cv2.resize(frame, (1280, 720)))
            self.videoFeed.config(image=tk_img)
            self.videoFeed.image = tk_img
        if not stopEvent.is_set():
            self.videoFeed.after(1, self.__updateImage, queue, stopEvent)

    def __onClose(self):
        stopVideoEvent.set()
        stopDroneEvent.set()
        self.videoProcessingThread.join()
        self.droneControlThread.join()
        self.window.destroy()

    def __setIsAutomatic(self, flag):
        self.isAutomatic = flag

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    ControlGUI()

