import threading
import asyncio


class DroneController:

    def __init__(self, angle, distance, vertical, horizontal, clockwise,
                 counterclockwise, left, right, up, down, forward, backward):
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

        print("[drone thread] Drone thread END.")

