import droneControl
import videoProcessing
import threading
import cv2
import tkinter
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

class ControlGUI:

    def __init__(self):
        self.lastEventSet = None
        self.lastActiveButton = None

        self.window = tkinter.Tk()
        self.window.geometry("800x540")
        self.window.columnconfigure(0, weight=3)
        self.window.columnconfigure(1, weight=1)
        self.window.rowconfigure(0, weight=9)
        self.window.rowconfigure(1, weight=1)
        self.defaultColor = self.window.cget("bg")

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
        self.videoLabel.grid(column=0, row=0)
        self.videoFeed = tkinter.Label(self.videoFrame)
        self.videoFeed.grid(column=0, row=1)

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
            self.lastEventSet = decodeQrEvent
            self.lastEventSet.set()


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