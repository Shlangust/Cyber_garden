from pymavlink import mavutil
import time

from drone_control import Drone


if __name__ == "__main__":
    drone1 = Drone('localhost', '5762')

    drone1.enter_guided_mode()
    time.sleep(1)
    drone1.arm_drone()
    time.sleep(1)
    drone1.take_off()
    time.sleep(4)
    drone1.go_to_local_position(20, 10, 10)
