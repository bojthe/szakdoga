import cv2
from tello_asyncio import VIDEO_URL

class videoProcessor:

    def __init__(self, angle, distance, vertical, horizontal, clockwise,
                 counterclockwise, left, right, up, down, forward, backward,
                 decode, failed):
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

        self.capture = cv2.VideoCapture(VIDEO_URL)
        self.decoder = cv2.QRCodeDetector()

    def process(self):
        try:
            self.capture.open(VIDEO_URL)
            while True:
                grabbed, frame = self.capture.read()
                if grabbed:
                    cv2.imshow("video_input", frame)
                if cv2.waitKey(1) != -1:
                    break
        except KeyboardInterrupt:
            pass
        finally:
            if self.capture:
                self.capture.release()
            cv2.destroyAllWindows()
