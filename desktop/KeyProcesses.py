import drone_control


def press_w(obj: drone_control.Drone, speed: int = 1):
    print("дрон летит вперед")
    obj.set_speed(lat=speed)


def press_a(obj: drone_control.Drone, speed: int = 1):
    print("рон летит нелево")
    obj.set_speed(lon=-speed)


def press_s(obj: drone_control.Drone, speed: int = 1):
    print("дрон летит назад")
    obj.set_speed(lat=-speed)


def press_d(obj: drone_control.Drone, speed: int = 1):
    print("дрон летит вправо")
    obj.set_speed(lon=speed)


def press_q(obj: drone_control.Drone, speed: int = 1):
    pass


def press_e(obj: drone_control.Drone, speed: int = 1):
    pass


def press_shift(obj: drone_control.Drone, speed: int = 1):
    obj.set_speed(height=-speed)


def press_enter(obj: drone_control.Drone, speed: int = 1):
    pass


def press_space(obj: drone_control.Drone, speed: int = 1):
    obj.set_speed(height=speed)


def press_up_arrow(obj: drone_control.Drone, speed: int = 1):
    pass


def press_down_arrow(obj: drone_control.Drone, speed: int = 1):
    pass


def press_left_arrow(obj: drone_control.Drone, speed: int = 1):
    pass


def press_right_arrow(obj: drone_control.Drone, speed: int = 1):
    pass
