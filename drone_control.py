from pymavlink import mavutil


class Drone:
    connection_status = True

    def __init__(self, host: str, port: str | int, protocol='tcp'):
        """создаёт подключение к дрону по указанному порту и хосту
        :param host: ip дрона
        :param port: порт для подключения
        :param protocol: протокол, по умолчанию tcp
        """
        try:
            self.connection = mavutil.mavlink_connection(f'{protocol}:{host}:{port}')
            self.connection.wait_heartbeat()
        except ConnectionRefusedError:
            self.connection_status = False

    def enter_guided_mode(self):
        """перевод дрона в управляемый режим"""
        self.connection.mav.set_mode_send(self.connection.target_system,
                                          mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED, 4)

    def leave_guided_mode(self):
        """вывод дрона из управляемого режима"""
        self.connection.mav.set_mode_send(self.connection.target_system,
                                          mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED, 0)

    def arm_drone(self):
        """включает двигатели"""
        self.connection.mav.command_long_send(self.connection.target_system, self.connection.target_component,
                                              mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)

    def disarm_drone(self):
        """выключает двигатели"""
        self.connection.mav.command_long_send(self.connection.target_system, self.connection.target_component,
                                              mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 0, 0, 0, 0, 0, 0, 0)

    def take_off(self, height=2.0):
        """дрон взлетает с поверхности на указанную высоту
        :param height: высота в метрах, по умолчанию 2
        """
        self.connection.mav.command_long_send(self.connection.target_system, self.connection.target_component,
                                              mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, height)

    def go_to_local_position(self, lat=0.0, lon=0.0, height=0.0):
        """дрон направляется в указанные координаты относительно места старта
        :param lat: широта в м (положительное - вперёд, север; отрицательное - назад, юг)
        :param lon: долгота в м (положительное - направо, восток; отрицательное - налево, запад)
        :param height: высота в м (положительное - вверх, отрицательное - вниз)
        """
        height *= -1
        self.connection.mav.send(mavutil.mavlink.MAVLink_set_position_target_local_ned_message(
            10, self.connection.target_system, self.connection.target_component, mavutil.mavlink.MAV_FRAME_LOCAL_NED,
            int(0b110111111000), lat, lon, height, 0, 0, 0, 0, 0, 0, 0, 0))

    def set_speed(self, lat=0.0, lon=0.0, height=0.0):
        """дрон направляется в указанные координаты относительно места старта
        :param lat: вперёд/назад в м/с положительное - вперёд, север; отрицательное - назад, юг)
        :param lon: влево/вправо в м/с (положительное - направо, восток; отрицательное - налево, запад)
        :param height: высота в м/с (положительное - вверх, отрицательное - вниз)
        """
        height *= -1
        self.connection.mav.send(mavutil.mavlink.MAVLink_set_position_target_local_ned_message(
            10, self.connection.target_system, self.connection.target_component, mavutil.mavlink.MAV_FRAME_LOCAL_NED,
            int(0b110111000111), 0, 0, 0, lat, lon, height, 0, 0, 0, 0, 0))
