from pymavlink import mavutil
import time

from drone_control import Drone


if __name__ == "__main__":
    drone = Drone('localhost', '5762')
    drone.go_to_global_position_safe(-35.492909, 149.122408)
    print("ok")
