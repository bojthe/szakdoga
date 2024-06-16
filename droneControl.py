import threading
import asyncio
from tello_asyncio import Tello

class DroneController:

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

    def flyAutomatic(self):
        print("[drone thread] Drone thread START.")

        async def main():
            drone = Tello()
            try:
                await drone.connect()
                await drone.start_video(connect=False)
                await asyncio.sleep(5)  # non-blocking sleep
                await drone.takeoff()

                # Here goes the automatic drone pathing

                await self.__reposition(drone)

                await drone.land()
            finally:
                await drone.stop_video()
                await drone.disconnect()



        asyncio.run(main())
        print("[drone thread] Drone thread END.")

    async def __reposition(self, drone):
        # clearing all events to have an initial state
        self.angleOkEvent.clear()
        self.distanceOkEvent.clear()
        self.verticalOkEvent.clear()
        self.horizontalOkEvent.clear()

        # setting the event for QR decoding
        print("QR decoding enabled.")
        self.decodeQrEvent.set()

        # reacting to QR interpretation
        await self.__findAngle(drone)
        await self.__findDistance(drone)
        await self.__findVerticalPosition(drone)
        await self.__findHorizontalPosition(drone)

        if self.failedEvent.is_set():
            print("Repositioning FAILED.")
            self.failedEvent.clear()
        else:
            print("Repositioning DONE.")

        # clearing all impacted events
        self.decodeQrEvent.clear()
        print("QR decoding disabled.")
        self.angleOkEvent.clear()
        self.distanceOkEvent.clear()
        self.verticalOkEvent.clear()
        self.horizontalOkEvent.clear()

    async def __findAngle(self, drone):
        controlSet = False
        while not self.angleOkEvent.is_set():
            if not controlSet and self.turnClockwiseEvent.is_set():
                drone.remote_control(left_right=0, forward_back=0, updown=0, yaw=1)
                controlSet = True
            elif not controlSet and self.turnCounterClockwiseEvent.is_set():
                drone.remote_control(left_right=0, forward_back=0, updown=0, yaw=-1)
                controlSet = True
            elif controlSet:
                drone.remote_control(left_right=0, forward_back=0, updown=0, yaw=0)
                controlSet = False
        drone.remote_control(left_right=0, forward_back=0, updown=0, yaw=0)

    async def __findDistance(self, drone):
        controlSet = False
        while not self.distanceOkEvent.is_set():
            if not controlSet and self.moveForwardEvent.is_set():
                drone.remote_control(left_right=0, forward_back=1, updown=0, yaw=0)
                controlSet = True
            elif not controlSet and self.moveBackwardEvent.is_set():
                drone.remote_control(left_right=0, forward_back=-1, updown=0, yaw=0)
                controlSet = True
            elif controlSet:
                drone.remote_control(left_right=0, forward_back=0, updown=0, yaw=0)
                controlSet = False
        drone.remote_control(left_right=0, forward_back=0, updown=0, yaw=0)

    async def __findVerticalPosition(self, drone):
        controlSet = False
        while not self.verticalOkEvent.is_set():
            if not controlSet and self.moveUpEvent.is_set():
                drone.remote_control(left_right=0, forward_back=0, updown=1, yaw=0)
                controlSet = True
            elif not controlSet and self.moveDownEvent.is_set():
                drone.remote_control(left_right=0, forward_back=0, updown=-1, yaw=0)
                controlSet = True
            elif controlSet:
                drone.remote_control(left_right=0, forward_back=0, updown=0, yaw=0)
                controlSet = False
        drone.remote_control(left_right=0, forward_back=0, updown=0, yaw=0)

    async def __findHorizontalPosition(self, drone):
        controlSet = False
        while not self.horizontalOkEvent.is_set():
            if not controlSet and self.moveLeftEvent.is_set():
                drone.remote_control(left_right=1, forward_back=0, updown=0, yaw=0)
                controlSet = True
            elif not controlSet and self.moveRightEvent.is_set():
                drone.remote_control(left_right=-1, forward_back=0, updown=0, yaw=0)
                controlSet = True
            elif controlSet:
                drone.remote_control(left_right=0, forward_back=0, updown=0, yaw=0)
                controlSet = False
        drone.remote_control(left_right=0, forward_back=0, updown=0, yaw=0)

