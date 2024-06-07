from pymavlink import mavutil
conection = mavutil.mavlink_connection('tcp:localhost:5762')
conection.wait_heartbeat()

print('Heartbeat from system (system %u component %u)' %
      (conection.target_system, conection.target_component))

conection.mav.command_long_send(conection.target_system, conection.target_component,
                                mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)
conection.mav.command_long_send(conection.target_system, conection.target_component,
                                mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, 10)

while True:
    msg = conection.recv_match(type='COMMAND_ACK', blocking=True)
    print(msg)
