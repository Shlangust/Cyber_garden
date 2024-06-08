import tkinter as tk

import customtkinter as ctk
from tkintermapview import TkinterMapView
from PIL import Image

import ScrollView
import KeyProcesses
import drone_control


class MainWindow(ctk.CTkFrame):
    def __init__(self, base, master, **kwargs):
        super().__init__(master, **kwargs)

        self.base = base
        self.drone_list = list()
        self.current_drone = 0

        # self.obj = drone_control.Drone(host="localhost", port="5762")
        # self.obj.enter_guided_mode()
        # self.drone_list.append(self.obj)

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
            text="НАЗВАНИЕ",
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

        self.map_widget = TkinterMapView(self, corner_radius=10)
        self.map_widget.grid(row=1, column=1, columnspan=2, rowspan=2, sticky=tk.NSEW, padx=0, pady=0)
        # self.map_widget.set_address("Москва")

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

        my_image = ctk.CTkImage(light_image=Image.open("../Image/free-icon-font-battery-three-quarters-9234404.png"),
                                          dark_image=Image.open("../Image/free-icon-font-battery-three-quarters-9234404.png"),
                                          size=(20, 20))
        image_label = ctk.CTkLabel(
            master=self.main_frame,
            image=my_image,
            text=""
        )
        image_label.grid(column=0, row=0, padx=(10, 5))
        image_label.bind("<Enter>", lambda event: self.create_menu())
        image_label.bind("<Leave>", lambda event: self.delete_menu())

        self.battery_label = ctk.CTkLabel(
            master=self.main_frame,
            text="95%"
        )
        self.battery_label.grid(column=1, row=0)
        # self.battery_label.after(5000, self.current_battery)

        my_image = ctk.CTkImage(light_image=Image.open("../Image/free-icon-font-drone-alt-11739931.png"),
                                dark_image=Image.open("../Image/free-icon-font-drone-alt-11739931.png"),
                                size=(20, 20))
        image_label = ctk.CTkLabel(master=self.main_frame, image=my_image, text="")
        image_label.grid(column=2, row=0, padx=(10, 5), sticky=tk.E)

        my_image = ctk.CTkImage(light_image=Image.open("../Image/free-icon-font-world-3916990.png"),
                                dark_image=Image.open("../Image/free-icon-font-world-3916990.png"),
                                size=(20, 20))
        image_label = ctk.CTkLabel(master=self.main_frame, image=my_image, text="")
        image_label.grid(column=3, row=0, padx=(10, 5), sticky=tk.W)


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
        )
        slider.grid(column=1, row=0)

        text_2 = ctk.CTkLabel(
            master=frame_slider,
            text=" 10 м/сек "
        )
        text_2.grid(column=2, row=0)

        my_image = ctk.CTkImage(light_image=Image.open("../Image/free-icon-font-info-3916699.png"),
                                dark_image=Image.open("../Image/free-icon-font-info-3916699.png"),
                                size=(20, 20))
        image_label = ctk.CTkLabel(master=self.main_frame, image=my_image, text="")
        image_label.grid(column=5, row=0, padx=(0, 10), sticky=tk.W)

        self.base.bind('<KeyPress>', self.on_key_press)

    def create_menu(self):
        obj = self.drone_list[self.current_drone]
        data = obj.get_battery_status()

        self.frame_menu_battery = ctk.CTkFrame(
            master=self,
            corner_radius=0,
            width=150, height=80,
            fg_color="white",
        )
        self.frame_menu_battery.grid(column=1, row=1, columnspan=2, sticky=tk.SW, padx=(10, 0), pady=(0, 5))

        self.inform = ctk.CTkLabel(
            master=self.frame_menu_battery,
            text=f"Напряжение: {data.get('voltage')}\n"
                 f"Температура: {data.get('temperature')}\n"
                 f"Потребленный заряд: {data.get('consumed_charge')}\n"
                 f"Потребленная энергия: {data.get('consumed_energy')}\n"
        )
        self.inform.place(x=0, y=0)

    def delete_menu(self):
        self.frame_menu_battery.destroy()

    def current_battery(self):
        obj = self.drone_list[self.current_drone]
        self.battery_label.configure(text=f"{obj.get_battery_status().get('charge')}%")
        self.after(5000, self.current_battery)

    def on_key_press(self, event):
        if event.keysym in ('W', 'w'):
            KeyProcesses.press_w(self.drone_list[self.current_drone])
        elif event.keysym in ('A', 'a'):
            KeyProcesses.press_a(self.drone_list[self.current_drone])
        elif event.keysym in ('S', 's'):
            KeyProcesses.press_s(self.drone_list[self.current_drone])
        elif event.keysym in ('D', 'd'):
            KeyProcesses.press_d(self.drone_list[self.current_drone])
        elif event.keysym in ('Q', 'q'):
            KeyProcesses.press_q(self.drone_list[self.current_drone])
        elif event.keysym in ('E', 'e'):
            KeyProcesses.press_e(self.drone_list[self.current_drone])
        elif event.keysym == 'Return':
            KeyProcesses.press_enter(self.drone_list[self.current_drone])
        elif event.keysym == 'Shift_L' or event.keysym == 'Shift_R':
            KeyProcesses.press_shift(self.drone_list[self.current_drone])
        elif event.keysym == 'space':
            KeyProcesses.press_space(self.drone_list[self.current_drone])
        elif event.keysym == 'Up':
            KeyProcesses.press_up_arrow(self.drone_list[self.current_drone])
        elif event.keysym == 'Down':
            KeyProcesses.press_down_arrow(self.drone_list[self.current_drone])
        elif event.keysym == 'Left':
            KeyProcesses.press_left_arrow(self.drone_list[self.current_drone])
        elif event.keysym == 'Right':
            KeyProcesses.press_right_arrow(self.drone_list[self.current_drone])
