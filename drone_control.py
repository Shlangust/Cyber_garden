from pymavlink import mavutil
import math


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

    def go_to_local_position(self, lat=0.0, lon=0.0, height=0.0, angle=0.0):
        """дрон направляется в указанные координаты относительно места старта
        :param lat: широта в м (положительное - вперёд, север; отрицательное - назад, юг)
        :param lon: долгота в м (положительное - направо, восток; отрицательное - налево, запад)
        :param height: высота в м (положительное - вверх, отрицательное - вниз)
        :param angle: градус поворота
        """
        height *= -1
        angle = math.radians(angle)
        self.connection.mav.send(mavutil.mavlink.MAVLink_set_position_target_local_ned_message(
            10, self.connection.target_system, self.connection.target_component, mavutil.mavlink.MAV_FRAME_LOCAL_NED,
            int(0b100111111000), lat, lon, height, 0, 0, 0, 0, 0, 0, angle, 0))

    def go_to_global_position(self, lat=0.0, lon=0.0, height=0.0, angle=0.0):
        """дрон направляется в указанные глобальные
        :param lat: широта в градусах (положительное - север; отрицательное - юг)
        :param lon: долгота в м (положительное - восток; отрицательное - запад)
        :param height: высота в м (положительное - вверх, отрицательное - вниз)
        :param angle: градус поворота
        """
        height *= -1
        angle = math.radians(angle)
        lat = int(lat * 10 ** 7)
        lon = int(lon * 10 ** 7)
        self.connection.mav.send(mavutil.mavlink.MAVLink_set_position_target_global_int_message(
            10, self.connection.target_system, self.connection.target_component, mavutil.mavlink.MAV_FRAME_GLOBAL_INT,
            int(0b100111111000), lat, lon, height, 0, 0, 0, 0, 0, 0, angle, 0))

    def set_speed(self, lat=0.0, lon=0.0, height=0.0, angle=0.0):
        """дрон направляется в указанные координаты относительно места старта
        :param lat: вперёд/назад в м/с положительное - вперёд, север; отрицательное - назад, юг)
        :param lon: влево/вправо в м/с (положительное - направо, восток; отрицательное - налево, запад)
        :param height: высота в м/с (положительное - вверх, отрицательное - вниз)
        :param angle: угловая скорость в градусах/секунду
        """
        height *= -1
        angle = math.radians(angle)
        self.connection.mav.send(mavutil.mavlink.MAVLink_set_position_target_local_ned_message(
            10, self.connection.target_system, self.connection.target_component, mavutil.mavlink.MAV_FRAME_LOCAL_NED,
            int(0b000111000111), 0, 0, 0, lat, lon, height, 0, 0, 0, 0, angle))

    def get_battery_status(self):
        """
        charge: оставшийся заряд в процентах,\n
        voltage: напряжение на батарее в Вольтах,\n
        temperature: температура в градусах Цельсия,\n
        consumed_charge: потреблённый заряд в миллиАмпер/час,\n
        consumed_energy: потреблённая энергия в Джоулях\n
        :return: словарь со значениями выше. если дрон прислал неверное значение - элемент в словаре равен 'invalid'
        """
        self.connection.mav.request_data_stream_send(self.connection.target_system, self.connection.target_component,
                                                     mavutil.mavlink.MAV_DATA_STREAM_ALL, 1, 1)
        msg = self.connection.recv_match(type='BATTERY_STATUS', blocking=True)
        battery_status = {
            "charge": msg.battery_remaining if msg.battery_remaining != -1 else "invalid",
            "voltage": (msg.voltages[0] / 1000) if msg.voltages[0] != 32767 else "invalid",
            "temperature": (msg.temperature / 100) if msg.temperature != 32767 else "invalid",
            "consumed_charge": msg.current_consumed if msg.current_consumed != -1 else "invalid",
            "consumed_energy": (msg.energy_consumed / 100) if msg.energy_consumed != -1 else "invalid"
        }
        return battery_status

    def get_geo(self):
        """
        latitude: широта (+ север; - юг) в градусах\n
        longitude: долгота (+ восток; - запад) в градусах\n
        altitude: высота от уровня моря в метрах\n
        altitude_ground: высота от уровня земли в метрах\n
        lat_speed: горизонтальная скорость в метрах/секунду (+ север, вперёд; - юг, назад)\n
        lon_speed: горизонтальная скорость в метрах/секунду (+ восток, право; - запад, лево)\n
        alt_speed: вертикальная скорость в метрах/секунду (+ верх; - низ)\n
        angle: угол от севера в градусах
        :return: словарь со значениями выше
        """
        self.connection.mav.request_data_stream_send(self.connection.target_system, self.connection.target_component,
                                                     mavutil.mavlink.MAV_DATA_STREAM_ALL, 1, 1)
        msg = self.connection.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
        position = {
            'latitude': msg.lat / 10000000,
            'longitude': msg.lon / 10000000,
            'altitude': msg.alt / 1000,
            'altitude_ground': msg.relative_alt / 1000,
            'lat_speed': msg.vx / 100,
            'lon_speed': msg.vy / 100,
            'alt_speed': msg.vz / -100,
            'angle': msg.hdg / 100
        }
        return position
