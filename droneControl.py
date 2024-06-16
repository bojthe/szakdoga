import threading
import asyncio


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
            while True:
                if self.angleOkEvent.is_set():
                    print("[drone thread] Angle event set.")
                if self.distanceOkEvent.is_set():
                    print("[drone thread] Distance event set.")
                if self.verticalOkEvent.is_set():
                    print("[drone thread] Vertical event set.")
                if self.horizontalOkEvent.is_set():
                    print("[drone thread] Horizontal event set.")
                await asyncio.sleep(0.5)

        asyncio.run(main())

        async def __findAngle(drone):
            controlSet = False
            while not self.angleOkEvent.is_set():
                if not controlSet and tself.urnClockwiseEvent.is_set():
                    drone.remote_control(left_right=0, forward_back=0, updown=0, yaw=1)
                    controlSet = True
                elif not controlSet and self.turnCounterClockwiseEvent.is_set():
                    drone.remote_control(left_right=0, forward_back=0, updown=0, yaw=-1)
                    controlSet = True
                elif controlSet:
                    drone.remote_control(left_right=0, forward_back=0, updown=0, yaw=0)
                    controlSet = False
            drone.remote_control(left_right=0, forward_back=0, updown=0, yaw=0)

        async def __findDistance(drone):
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

        async def __findVerticalPosition(drone):
            controlSet = False
            while not self.verticalOkEvent.is_set():
                if not controlSet and self.moveUpEvent.is_set():
                    drone.remote_control(left_right=0, forward_back=0, updown=1, yaw=0)
                    controlSet = True
                elif not controlSet and moveDownEvent.is_set():
                    drone.remote_control(left_right=0, forward_back=0, updown=-1, yaw=0)
                    controlSet = True
                elif controlSet:
                    drone.remote_control(left_right=0, forward_back=0, updown=0, yaw=0)
                    controlSet = False
            drone.remote_control(left_right=0, forward_back=0, updown=0, yaw=0)

        async def __findHorizontalPosition(drone):
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

        print("[drone thread] Drone thread END.")

