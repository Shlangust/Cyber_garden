import tkinter as tk

import customtkinter as ctk

import ScrollView
import KeyProcesses
import drone_control


class MainWindow(ctk.CTkFrame):
    def __init__(self, base, master, **kwargs):
        super().__init__(master, **kwargs)

        self.base = base
        self.drone_list = list()
        self.current_drone = 0

        self.obj = drone_control.Drone(host="localhost", port="5762")
        self.obj.enter_guided_mode()
        self.drone_list.append(self.obj)

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

        camera = ctk.CTkFrame(
            master=self,
            fg_color="gray",
        )
        camera.grid(row=1, column=1, columnspan=2, sticky=tk.NSEW, padx=0, pady=0)

        label_left = ctk.CTkLabel(
            master=self,
            text="x: 0, y: 0 z: 0",
            text_color="black",
            bg_color="white"
        )
        label_left.grid(row=2, column=1, sticky=tk.NW, padx=(10, 0))

        label_right = ctk.CTkLabel(
            master=self,
            text="заряд батареи: 90%",
            text_color="black",
            bg_color="white"
        )
        label_right.grid(row=2, column=2, sticky=tk.NE, padx=(0, 10))

        text_information = ctk.CTkLabel(
            master=self,
            bg_color="white",
            text="W - вперед \tA - влево \nS - назад  \tD - вправо \nQ - поворот налево \tE - поворот направо \n↑ - тангаж  \t↓ - тангаж \n← - крен   \t→ - крен \nEnter - вверх \tShift - вниз"
        )
        text_information.grid(row=2, column=1, columnspan=3, pady=40)

        self.base.bind('<KeyPress>', self.on_key_press)

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
