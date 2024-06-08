from pymavlink import mavutil
import time

from drone_control import Drone


if __name__ == "__main__":
    drone = Drone('localhost', '5762')
    drone.auto_start(10)
