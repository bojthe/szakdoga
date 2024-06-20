import cv2
from tello_asyncio import VIDEO_URL


class videoProcessor:
    # [red, orange, yellow, light-green, green]
    COLOR_STAGES = [(0, 0, 255), (0, 128, 255), (0, 255, 255), (0, 255, 128), (0, 255, 0)]
    # the size of the QR code edge in pixels from that distance
    SIDE_SIZES = {"30": 202, "40": 116, "50": 90}
    # the margin of error in pixels from that distance
    MARGINS = {"30": 20, "40": 12, "50": 9}

    def __init__(self, angle, distance, vertical, horizontal, clockwise,
                 counterclockwise, left, right, up, down, forward, backward,
                 decode, failed, videoQueue, threadStopEvent):
        self.angleOkEvent = angle
        self.distanceOkEvent = distance
        self.verticalOkEvent = vertical
        self.horizontalOkEvent = horizontal
        self.turnClockwiseEvent = clockwise
        self.turnCounterClockwiseEvent = counterclockwise
        self.moveLeftEvent = left
        self.moveRightEvent = right
        self.moveUpEvent = up
        self.moveDownEvent = down
        self.moveForwardEvent = forward
        self.moveBackwardEvent = backward
        self.decodeQrEvent = decode
        self.failedEvent = failed
        self.threadStopEvent = threadStopEvent
        self.videoQueue = videoQueue

        #self.capture = cv2.VideoCapture(VIDEO_URL)
        self.capture = cv2.VideoCapture("testVideo.mp4")
        self.decoder = cv2.QRCodeDetector()

    def process(self):
        try:
            # self.capture.open(VIDEO_URL)
            self.capture.open("testVideo.mp4")
            frameCount = 0
            points, data = None, None
            nothingFound = True
            while not self.threadStopEvent.is_set():
                grabbed, frame = self.capture.read()
                if grabbed:
                    if self.decodeQrEvent.is_set():
                        # every 5 frames try and decode the QR code
                        if frameCount % 5 == 0:
                            data, points, _ = self.decoder.detectAndDecode(frame)
                        frameCount = frameCount + 1
                        if points is not None and len(points) > 0 and data is not None:
                            nothingFound = False
                            code = data.split("-")
                            if len(code) == 3:
                                print(code[0] + " " + code[1] + " " + code[2])
                                self.__interpretQR(frame, points[0], code[0], code[1], code[2])

                        if not self.videoQueue.full():
                            self.videoQueue.put(frame)

                        if frameCount > 100 and nothingFound == True:
                            frameCount = 0
                            print("[video processor] FAILURE. QR code not found.")
                            self.angleOkEvent.set()
                            self.distanceOkEvent.set()
                            self.verticalOkEvent.set()
                            self.horizontalOkEvent.set()
                            self.failedEvent.set()
                            break
                    else:
                        if not self.videoQueue.full():
                            self.videoQueue.put(frame)
                        frameCount = 0
                if cv2.waitKey(1) != -1:
                    break
        except KeyboardInterrupt:
            pass
        finally:
            if self.capture:
                self.capture.release()

    def __interpretQR(self, frame, points, horizontalPosition, verticalPosition, distance):
        if not self.angleOkEvent.is_set():
            self.__controlAngle(points, distance)
            self.__box(frame, points, 0)
        elif not self.distanceOkEvent.is_set():
            self.__controlDistance(points, distance)
            self.__box(frame, points, 1)
        elif not self.verticalOkEvent.is_set():
            self.__controlVerticalPosition(frame, points, distance, verticalPosition)
            self.__box(frame, points, 2)
        elif not self.horizontalOkEvent.is_set():
            self.__controlHorizontalPosition(frame, points, distance, horizontalPosition)
            self.__box(frame, points, 3)
        else:
            self.__box(frame, points, 4)
            self.__clearMovementEvents()


    def __clearMovementEvents(self):
        self.turnClockwiseEvent.clear()
        self.turnCounterClockwiseEvent.clear()
        self.moveLeftEvent.clear()
        self.moveRightEvent.clear()
        self.moveUpEvent.clear()
        self.moveDownEvent.clear()
        self.moveForwardEvent.clear()
        self.moveBackwardEvent.clear()


    def __box(self, frame, points, colorIndex):
        for i in range(len(points)):
            pt1 = [int(val) for val in points[i]]
            pt2 = [int(val) for val in points[(i + 1) % 4]]
            # print('i:' + str(i) + ' pt1: ' + str(pt1) + ' pt2: ' + str(pt2))
            cv2.line(frame, pt1, pt2, color=self.COLOR_STAGES[colorIndex], thickness=2)


    def __controlAngle(self, points, distance):
        # if left side is smaller than right side ---> turn clockwise
        if points[3][1]-points[0][1]-points[2][1]-points[1][1] < 0-self.MARGINS[distance]:
            self.turnCounterClockwiseEvent.clear()
            self.turnClockwiseEvent.set()
        # if right side smaller than left side ---> turn counter clockwise
        elif points[3][1]-points[0][1]-points[2][1]-points[1][1] > self.MARGINS[distance]:
            self.turnClockwiseEvent.clear()
            self.turnCounterClockwiseEvent.set()
        # if both sides within margin of error ---> angle is correct
        else:
            self.turnCounterClockwiseEvent.clear()
            self.turnClockwiseEvent.clear()
            self.angleOkEvent.set()


    def __controlDistance(self, points, distance):
        # if side length is smaller than expected ---> move forward
        if points[1][0] - points[0][0] < self.SIDE_SIZES[distance] - self.MARGINS[distance]:
            self.moveBackwardEvent.clear()
            self.moveForwardEvent.set()
        # if side length greater than expected ---> move backwards
        elif points[1][0] - points[0][0] > self.SIDE_SIZES[distance] + self.MARGINS[distance]:
            self.moveForwardEvent.clear()
            self.moveBackwardEvent.set()
        # if side length within margin of error ---> distance is correct
        else:
            self.moveForwardEvent.clear()
            self.moveBackwardEvent.clear()
            self.distanceOkEvent.set()


    def __controlVerticalPosition(self, frame, points, distance, position):
        if position == "Under":
            # if the top side of the QR code is above threshold --> move down
            if points[0][1] < frame.shape[0] / 2 + self.SIDE_SIZES[distance]:
                self.moveUpEvent.clear()
                self.moveDownEvent.set()
            # if the top side of the QR code is below threshold --> vertical position is correct
            else:
                self.moveUpEvent.clear()
                self.moveDownEvent.clear()
                self.verticalOkEvent.set()
        elif position == "Center":
            # if the top side of the QR code is above threshold --> move down
            if points[0][1] < frame.shape[0] / 2 - self.SIDE_SIZES[distance] / 2 - self.MARGINS[distance]:
                self.moveUpEvent.clear()
                self.moveDownEvent.set()
            # if the top side of the QR code is below threshold --> move up
            elif points[0][1] > frame.shape[0] / 2 - self.SIDE_SIZES[distance] / 2 + self.MARGINS[distance]:
                self.moveDownEvent.clear()
                self.moveUpEvent.set()
            # if the top side of the QR code is in between the thresholds --> vertical position is correct
            else:
                self.moveDownEvent.clear()
                self.moveUpEvent.clear()
                self.verticalOkEvent.set()
        else:
            # if the bottom side of the QR code is below threshold --> move up
            if points[3][1] > frame.shape[0] / 2 - self.SIDE_SIZES[distance]:
                self.moveDownEvent.clear()
                self.moveUpEvent.set()
            # if the bottom side of the QR code is above threshold --> vertical position is correct
            else:
                self.moveUpEvent.clear()
                self.moveDownEvent.clear()
                self.verticalOkEvent.set()


    def __controlHorizontalPosition(self, frame, points, distance, position):
        if position == "Left":
            # if the right side of the QR code is right from the threshold --> move left
            if points[1][0] > frame.shape[1] / 2 - 2 * self.SIDE_SIZES[distance] + self.MARGINS[distance]:
                self.moveRightEvent.clear()
                self.moveLeftEvent.set()
            # if the right side of the Qr code is left from threshold --> horizontal position is correct
            else:
                self.moveRightEvent.clear()
                self.moveLeftEvent.clear()
                self.horizontalOkEvent.set()
        elif position == "Center":
            # if the right side of the QR code is right from the threshold --> move left
            if points[1][0] > frame.shape[1] / 2 + self.SIDE_SIZES[distance] / 2 + self.MARGINS[distance]:
                self.moveRightEvent.clear()
                self.moveLeftEvent.set()
            # if the right side of the QR code is left from the threshold --> move right
            elif points[1][0] < frame.shape[1] / 2 + self.SIDE_SIZES[distance] / 2 - self.MARGINS[distance]:
                self.moveLeftEvent.clear()
                self.moveRightEvent.set()
            # if the right side of the Qr code is in between the thresholds --> horizontal position is correct
            else:
                self.moveRightEvent.clear()
                self.moveLeftEvent.clear()
                self.horizontalOkEvent.set()
        else:
            # if the left side of the Qr code is left from threshold --> move right
            if points[0][0] < frame.shape[1] / 2 - 2 * self.SIDE_SIZES[distance] - self.MARGINS[distance]:
                self.moveLeftEvent.clear()
                self.moveRightEvent.set()
            # if the left side of the Qr code is right from threshold --> horizontal position is correct
            else:
                self.moveRightEvent.clear()
                self.moveLeftEvent.clear()
                self.horizontalOkEvent.set()