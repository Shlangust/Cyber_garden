from pymavlink import mavutil
import time

from drone_control import Drone
connections = {}
connections['drone0'] = Drone('localhost', '5782')
connections['drone1'] = Drone('localhost', '5762')
connections['drone2'] = Drone('localhost', '5772')

connections['drone0'].auto_start()
connections['drone1'].auto_start()
connections['drone2'].auto_start()
def klin():
    alpha_position = connections['drone0'].get_geo()

    for drone_name, drone_connection in connections.items():
        plase = int(drone_name[5:])
        if plase%2 == 0 and plase != 0:
            drone_connection.go_to_global_position(alpha_position['latitude']-plase * 000.0000001,
                                                   alpha_position['longitude']-plase * 000.0000001)
        if plase%2 ==1 and plase !=0:
            drone_connection.go_to_global_position(alpha_position['latitude'] - plase * 000.0000001,
                                                   alpha_position['longitude'] + plase * 000.0000001)
klin()
print(connections['drone0'].get_geo())
print(connections['drone1'].get_geo())
print(connections['drone2'].get_geo())