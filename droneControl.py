import asyncio
from tello_asyncio import Tello


class DroneController:

    def __init__(self, angle, distance, vertical, horizontal, clockwise,
                 counterclockwise, left, right, up, down, forward, backward,
                 decode, failed, stopEvent, stopDroneThread, takeOffEvent, landEvent, correctionEvent):
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
        self.stopEvent = stopEvent
        self.stopDroneThread = stopDroneThread
        self.takeOffEvent = takeOffEvent
        self.landEvent = landEvent
        self.correctionEvent = correctionEvent

    def flyAutomatic(self):
        print("[drone thread] Drone thread Automatic START.")

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

    def flyManual(self):
        print("[drone thread] Drone thread Manual START.")

        async def main():

            drone = Tello()
            try:
                await drone.connect()
                await drone.start_video(connect=False)
                currentCommand = None
                while not self.stopDroneThread.is_set():
                    if self.moveUpEvent.is_set():
                        if currentCommand != "UP":
                            currentCommand = "UP"
                            await drone.remote_control(left_right=0, forward_back=0, up_down=5, yaw=0)
                    elif self.moveDownEvent.is_set():
                        if currentCommand != "DOWN":
                            currentCommand = "DOWN"
                            await drone.remote_control(left_right=0, forward_back=0, up_down=-5, yaw=0)
                    elif self.moveRightEvent.is_set():
                        if currentCommand != "RIGHT":
                            currentCommand = "RIGHT"
                            await drone.remote_control(left_right=5, forward_back=0, up_down=0, yaw=0)
                    elif self.moveLeftEvent.is_set():
                        if currentCommand != "LEFT":
                            currentCommand = "LEFT"
                            await drone.remote_control(left_right=-5, forward_back=0, up_down=0, yaw=0)
                    elif self.moveBackwardEvent.is_set():
                        if currentCommand != "BACK":
                            currentCommand = "BACK"
                            await drone.remote_control(left_right=0, forward_back=-5, up_down=0, yaw=0)
                    elif self.moveForwardEvent.is_set():
                        if currentCommand != "FORW":
                            currentCommand = "FORW"
                            await drone.remote_control(left_right=0, forward_back=5, up_down=0, yaw=0)
                    elif self.turnClockwiseEvent.is_set:
                        if currentCommand != "CLW":
                            currentCommand = "CLW"
                            await drone.remote_control(left_right=0, forward_back=0, up_down=0, yaw=1)
                    elif self.turnCounterClockwiseEvent.is_set():
                        if currentCommand != "CCLW":
                            currentCommand = "CCLW"
                            await drone.remote_control(left_right=0, forward_back=0, up_down=0, yaw=-1)
                    elif self.stopEvent.is_set():
                        if currentCommand != "STOP":
                            currentCommand = "STOP"
                            await drone.remote_control(left_right=0, forward_back=0, up_down=0, yaw=0)
                    elif self.takeOffEvent.is_set():
                        if currentCommand != "TOFF":
                            currentCommand = "TOFF"
                            await drone.takeoff()
                    elif self.landEvent.is_set():
                        if currentCommand != "LAND":
                            currentCommand = "LAND"
                            await drone.land()
                    elif self.correctionEvent.is_set():
                        if currentCommand != "CORR":
                            currentCommand = "CORR"
                            await self.__reposition(drone)
                    else:
                        currentCommand = None
                        await drone.remote_control(left_right=0, forward_back=0, up_down=0, yaw=0)

                    await asyncio.sleep(0.2)
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
                drone.remote_control(left_right=0, forward_back=0, up_down=0, yaw=1)
                controlSet = True
            elif not controlSet and self.turnCounterClockwiseEvent.is_set():
                drone.remote_control(left_right=0, forward_back=0, up_down=0, yaw=-1)
                controlSet = True
            elif controlSet:
                drone.remote_control(left_right=0, forward_back=0, up_down=0, yaw=0)
                controlSet = False
        drone.remote_control(left_right=0, forward_back=0, up_down=0, yaw=0)

    async def __findDistance(self, drone):
        controlSet = False
        while not self.distanceOkEvent.is_set():
            if not controlSet and self.moveForwardEvent.is_set():
                drone.remote_control(left_right=0, forward_back=1, up_down=0, yaw=0)
                controlSet = True
            elif not controlSet and self.moveBackwardEvent.is_set():
                drone.remote_control(left_right=0, forward_back=-1, up_down=0, yaw=0)
                controlSet = True
            elif controlSet:
                drone.remote_control(left_right=0, forward_back=0, up_down=0, yaw=0)
                controlSet = False
        drone.remote_control(left_right=0, forward_back=0, up_down=0, yaw=0)

    async def __findVerticalPosition(self, drone):
        controlSet = False
        while not self.verticalOkEvent.is_set():
            if not controlSet and self.moveUpEvent.is_set():
                drone.remote_control(left_right=0, forward_back=0, up_down=1, yaw=0)
                controlSet = True
            elif not controlSet and self.moveDownEvent.is_set():
                drone.remote_control(left_right=0, forward_back=0, up_down=-1, yaw=0)
                controlSet = True
            elif controlSet:
                drone.remote_control(left_right=0, forward_back=0, up_down=0, yaw=0)
                controlSet = False
        drone.remote_control(left_right=0, forward_back=0, up_down=0, yaw=0)

    async def __findHorizontalPosition(self, drone):
        controlSet = False
        while not self.horizontalOkEvent.is_set():
            if not controlSet and self.moveLeftEvent.is_set():
                drone.remote_control(left_right=1, forward_back=0, up_down=0, yaw=0)
                controlSet = True
            elif not controlSet and self.moveRightEvent.is_set():
                drone.remote_control(left_right=-1, forward_back=0, up_down=0, yaw=0)
                controlSet = True
            elif controlSet:
                drone.remote_control(left_right=0, forward_back=0, up_down=0, yaw=0)
                controlSet = False
        drone.remote_control(left_right=0, forward_back=0, up_down=0, yaw=0)

