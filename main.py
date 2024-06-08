from pymavlink import mavutil
import time

from drone_control import Drone


if __name__ == "__main__":
    connection = mavutil.mavlink_connection(f'tcp:localhost:5762')
    connection.wait_heartbeat()

    connection.mav.command_long_send(connection.target_system, connection.target_component,
                                     mavutil.mavlink.MAV_CMD_DO_DIGICAM_CONFIGURE, 0, 1, 24, 4, 80, 0, 0, 0.1)

    connection.mav.command_long_send(connection.target_system, connection.target_component,
                                     mavutil.mavlink.MAV_CMD_DO_DIGICAM_CONTROL, 0, 1, 0, 0, 1, 1, 0, 0)

    connection.mav.request_data_stream_send(connection.target_system, connection.target_component,
                                            mavutil.mavlink.MAV_DATA_STREAM_ALL, 1, 1)

    msg = connection.recv_match(blocking=True)
    print(msg)
