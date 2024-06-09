import threading
import time
import tkinter as tk

import customtkinter as ctk
from tkintermapview import TkinterMapView
from PIL import Image
import win32api

import ScrollView
import KeyProcesses
import drone_control


class MainWindow(ctk.CTkFrame):

    def create_connect_drone(self):
        self.obj = drone_control.Drone(host="localhost", port="5762")

        if not self.obj.connection_status:
            result = win32api.MessageBox(0, 'Подключение к дрону не удалось.\n', 'SkyGrid - Error', 5)
            if result == 4:
                self.create_connect_drone()
        else:
            self.drone_list.append(self.obj)

    def __init__(self, base, master, **kwargs):
        super().__init__(master, **kwargs)

        self.base = base
        self.drone_list = list()
        self.current_drone = 0

        thread = threading.Thread(target=self.create_connect_drone)
        thread.start()

        self.start()

    def start(self):
        self.grid_columnconfigure(index=0, weight=0)
        self.grid_columnconfigure(index=1, weight=1)
        self.grid_columnconfigure(index=2, weight=1)
        self.grid_rowconfigure(index=0, weight=0)
        self.grid_rowconfigure(index=1, weight=1)
        self.grid_rowconfigure(index=2, weight=0)

        scroll = ScrollView.ScrollView(
            master=self,
            corner_radius=0,
            fg_color="transparent",
            scrollbar_fg_color="#F2F2F2",
            scrollbar_button_color="#F2F2F2",
            scrollbar_button_hover_color="#F2F2F2",
        )
        scroll.grid(row=1, column=0, rowspan=2, sticky=tk.NSEW)

        label = ctk.CTkLabel(
            master=self,
            text="SkyGrid",
            text_color="black",
            font=("Montserrat", 20, "bold"),
        )
        label.grid(row=0, column=1, columnspan=2, pady=10)

        frame = ctk.CTkFrame(
            master=self,
            corner_radius=10,
            fg_color="white"
        )
        frame.grid(row=1, column=1, columnspan=2, rowspan=2, sticky=tk.NSEW, padx=0, pady=0)

        self.create_card()

        self.main_frame = ctk.CTkFrame(
            master=self,
            height=30,
            fg_color="#dcdcdc",
            corner_radius=15
        )
        self.main_frame.grid(row=2, column=1, columnspan=5, rowspan=2, sticky=tk.NSEW, padx=10, pady=(0, 5))

        self.main_frame.grid_columnconfigure(index=0, weight=0)
        self.main_frame.grid_columnconfigure(index=1, weight=0)
        self.main_frame.grid_columnconfigure(index=2, weight=1)
        self.main_frame.grid_columnconfigure(index=3, weight=1)
        self.main_frame.grid_columnconfigure(index=4, weight=1)
        self.main_frame.grid_columnconfigure(index=5, weight=0)

        my_image = ctk.CTkImage(light_image=Image.open("../Image/battery-image.png"),
                                dark_image=Image.open("../Image/battery-image.png"),
                                size=(20, 20))
        image_label = ctk.CTkLabel(
            master=self.main_frame,
            image=my_image,
            text=""
        )
        image_label.grid(column=0, row=0, padx=(10, 5))
        image_label.bind("<Enter>", lambda event: self.create_battery_menu())
        image_label.bind("<Leave>", lambda event: self.delete_battery_menu())

        self.battery_label = ctk.CTkLabel(
            master=self.main_frame,
            text="100%" if len(self.drone_list) != 0 else "--%"
        )
        self.battery_label.grid(column=1, row=0)
        self.battery_label.after(5000, self.current_battery)

        my_image = ctk.CTkImage(light_image=Image.open("../Image/world-image.png"),
                                dark_image=Image.open("../Image/world-image.png"),
                                size=(20, 20))
        self.image_button = ctk.CTkButton(
            master=self.main_frame,
            width=25, height=25,
            image=my_image,
            fg_color="transparent",
            hover=False,
            text="",
            command=self.new_view
        )
        self.image_button.grid(column=3, row=0, padx=(10, 5), sticky=tk.S)


        frame_slider = ctk.CTkFrame(
            master=self.main_frame,
            fg_color="transparent",
        )
        frame_slider.grid(column=4, row=0, sticky=tk.NSEW)

        text_1 = ctk.CTkLabel(
            master=frame_slider,
            text="скорость: 0.1 "
        )
        text_1.grid(column=0, row=0)

        slider = ctk.CTkSlider(
            master=frame_slider,
            from_=10,
            to=100,
            command=self.slider_event
        )
        slider.grid(column=1, row=0)

        text_2 = ctk.CTkLabel(
            master=frame_slider,
            text=" 10 м/сек "
        )
        text_2.grid(column=2, row=0)

        top_frame = ctk.CTkFrame(
            master=self.main_frame,
            fg_color="transparent"
        )
        top_frame.grid(column=5, row=0, sticky=tk.W)

        top_frame.grid_columnconfigure(index=0, weight=0)
        top_frame.grid_columnconfigure(index=0, weight=0)

        my_image = ctk.CTkImage(light_image=Image.open("../Image/stats-image.png"),
                                dark_image=Image.open("../Image/stats-image.png"),
                                size=(18, 18))
        self.image_button = ctk.CTkButton(
            master=top_frame,
            width=25, height=25,
            image=my_image,
            fg_color="transparent",
            hover=False,
            text=""
        )
        self.image_button.grid(column=0, row=0, padx=(0, 5), sticky=tk.S)

        my_image = ctk.CTkImage(light_image=Image.open("../Image/info-image.png"),
                                dark_image=Image.open("../Image/info-image.png"),
                                size=(20, 20))
        image_label1 = ctk.CTkLabel(master=top_frame, image=my_image, text="")
        image_label1.grid(column=1, row=0, padx=(0, 10), sticky=tk.W)

        image_label1.bind("<Enter>", lambda event: self.create_inform_menu())
        image_label1.bind("<Leave>", lambda event: self.delete_inform_menu())

        self.base.bind('<KeyPress>', self.on_key_press)
        self.base.bind('<Control-space>', self.on_ctrl_space)
        self.bind('<Control-Shift-Key>', self.on_ctrl_shift)

    def on_ctrl_space(self, event):
        if len(self.drone_list) != 0:
            drone = self.drone_list[self.current_drone]
            drone.auto_start()

    def on_ctrl_shift(self):
        if len(self.drone_list) != 0:
            drone = self.drone_list[self.current_drone]
            drone.auto_land()


    current_speed = 1
    current_mode = False
    go_to_position = None
    list_drone_positions = list()

    def create_path_marker(self, coords):
        try:
            self.go_to_position = self.map_widget.set_marker(coords[0], coords[1], text="точка назначения")
            self.go_to_position.text_color = "white"
            self.map_widget.delete_all_path()
            self.map_widget.set_path([self.list_drone_positions[self.current_drone].position, self.go_to_position.position])

            drone = self.drone_list[self.current_drone]
            drone.go_to_global_position_safe(coords[0], coords[1])

            if not drone.autopilot:
                self.map_widget.delete_all_path()

        except:
            pass

    def update_path_marker(self):
        try:
            self.map_widget.delete_all_path()
            self.map_widget.set_path([self.list_drone_positions[self.current_drone].position, self.go_to_position.position])
        except:
            pass


    def create_drone_marker(self, name: str, coords: list):
        position = self.map_widget.set_marker(coords[0], coords[1], text=name)
        position.text_color = "white"
        self.map_widget.set_zoom(12)
        self.list_drone_positions.append(position)

    def add_marker_event(self, coords):
        if self.go_to_position is None:
            self.create_path_marker(coords)
        else:
            self.go_to_position.delete()
            self.create_path_marker(coords)

    drone_current_position = None

    def create_card(self):
        self.map_widget = TkinterMapView(self, corner_radius=10)
        self.map_widget.grid(row=1, column=1, columnspan=2, rowspan=2, sticky=tk.NSEW, padx=0, pady=0)
        self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

        if len(self.drone_list) != 0:
            drone = self.drone_list[self.current_drone]
            position = drone.get_geo()

            self.create_drone_marker(name="дрон 1", coords=[position.get("latitude"), position.get("longitude")])
            self.map_widget.set_position(*self.list_drone_positions[self.current_drone].position)
            thread = threading.Thread(target=self.update_dron_position)
            thread.start()

        self.map_widget.add_right_click_menu_command(label="отправить дрон сюда",
                                                command=self.add_marker_event,
                                                pass_coords=True)

    def update_dron_position(self):
        drone = self.drone_list[self.current_drone]
        position = drone.get_geo()

        marker = self.list_drone_positions[self.current_drone]
        marker.set_position(position.get("latitude"), position.get("longitude"))
        self.update_path_marker()

        time.sleep(0.2)
        self.update_dron_position()

    def new_view(self):
        image = ctk.CTkImage(
            light_image=Image.open("../Image/drone-image.png"),
            dark_image=Image.open("../Image/drone-image.png"),
            size=(20, 20)
        )

        image_1 = ctk.CTkImage(
            light_image=Image.open("../Image/world-image.png"),
            dark_image=Image.open("../Image/world-image.png"),
            size=(20, 20)
        )

        self.image_button.configure(image=image_1 if self.current_mode else image)
        if not self.current_mode:
            self.map_widget.destroy()

            self.camera = ctk.CTkFrame(
                master=self,
                corner_radius=10,
                fg_color="black"
            )
            self.camera.grid(row=1, column=1, columnspan=2, rowspan=2, sticky=tk.NSEW, padx=0, pady=0)
            self.main_frame.lift()
        else:
            self.camera.destroy()
            self.create_card()

            self.main_frame.lift()

        self.current_mode = not self.current_mode

    def slider_event(self, value):
        self.current_speed = round(value / 10, 3)

    def create_battery_menu(self):
        if len(self.drone_list) == 0:
            return

        obj = self.drone_list[self.current_drone]
        data = obj.get_battery_status()

        self.frame_menu_battery = ctk.CTkFrame(
            master=self,
            corner_radius=0,
            width=205, height=80,
            fg_color="white",
        )
        self.frame_menu_battery.grid(column=1, row=1, columnspan=2, sticky=tk.SW, padx=(10, 0), pady=(0, 5))

        self.inform = ctk.CTkLabel(
            master=self.frame_menu_battery,
            compound="left",
            justify="left",
            text=f"Напряжение: {data.get('voltage')} V\n"
                 f"Температура: {data.get('temperature')} ℃\n"
                 f"Потребленный заряд: {data.get('consumed_charge')} мA/ч\n"
                 f"Потребленная энергия: {data.get('consumed_energy')} Дж\n"
        )
        self.inform.place(x=5, y=5)

    def delete_battery_menu(self):
        if hasattr(self, 'frame_menu_battery'):
            self.frame_menu_battery.destroy()

    def create_inform_menu(self):
        self.frame_menu_battery = ctk.CTkFrame(
            master=self,
            corner_radius=0,
            width=170, height=165,
            fg_color="white",
        )
        self.frame_menu_battery.grid(column=1, row=1, columnspan=2, sticky=tk.SE, padx=(0, 10), pady=(0, 5))

        self.inform = ctk.CTkLabel(
            master=self.frame_menu_battery,
            compound="left",
            justify="left",
            text="Управление дроном:\n"
                 "W - вперед \n"
                 "S - назад \n"
                 "A - налево \n"
                 "D - вправо \n"
                 "Q - поворот налево \n"
                 "E - поворот направо \n"
                 "Shift - спуск дрона \n"
                 "Space - подьем дрона \n"
                 "Ctrl + Space - запуск дрона \n"
                 "Ctrl + Shift - посадка дрона"
        )
        self.inform.place(x=5, y=5)

    def delete_inform_menu(self):
        if hasattr(self, 'frame_menu_battery'):
            self.frame_menu_battery.destroy()

    def current_battery(self):
        if len(self.drone_list) != 0:
            obj = self.drone_list[self.current_drone]
            self.battery_label.configure(text=f"{obj.get_battery_status().get('charge')}%")
            self.after(5000, self.current_battery)

    def on_key_press(self, event):
        if event.keysym in ('W', 'w'):
            KeyProcesses.press_w(self.drone_list[self.current_drone], self.current_speed)
        elif event.keysym in ('A', 'a'):
            KeyProcesses.press_a(self.drone_list[self.current_drone], self.current_speed)
        elif event.keysym in ('S', 's'):
            KeyProcesses.press_s(self.drone_list[self.current_drone], self.current_speed)
        elif event.keysym in ('D', 'd'):
            KeyProcesses.press_d(self.drone_list[self.current_drone], self.current_speed)
        elif event.keysym in ('Q', 'q'):
            KeyProcesses.press_q(self.drone_list[self.current_drone], self.current_speed)
        elif event.keysym in ('E', 'e'):
            KeyProcesses.press_e(self.drone_list[self.current_drone], self.current_speed)
        elif event.keysym == 'Return':
            KeyProcesses.press_enter(self.drone_list[self.current_drone], self.current_speed)
        elif event.keysym == 'Shift_L' or event.keysym == 'Shift_R':
            KeyProcesses.press_shift(self.drone_list[self.current_drone], self.current_speed)
        elif event.keysym == 'space':
            KeyProcesses.press_space(self.drone_list[self.current_drone], self.current_speed)
