import droneControl
import time
import threading

angleOkEvent = threading.Event()
distanceOkEvent = threading.Event()
verticalOkEvent = threading.Event()
horizontalOkEvent = threading.Event()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("[main thread] Creating controller thread")
    controller = droneControl.DroneController(angleOkEvent, distanceOkEvent, verticalOkEvent, horizontalOkEvent)
    flyingThread = threading.Thread(target=controller.flyAutomatic, daemon=True)
    flyingThread.start()

    print("[main thread] Setting distance event")
    distanceOkEvent.set()
    time.sleep(0.2)
    print("[main thread] Setting angle event")
    angleOkEvent.set()
    time.sleep(1)
    print("[main thread] clearing distance event")
    distanceOkEvent.clear()
    time.sleep(3)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
