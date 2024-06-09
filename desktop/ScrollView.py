import json
import tkinter as tk

import customtkinter as ctk

import desktop_start

import main_window

class frame(ctk.CTkFrame):
    def __init__(self, base: desktop_start, obj, master, **kwargs ):
        super().__init__(master, **kwargs)

        self.base = base
        self.grid_columnconfigure(0, weight=0)
        self.grid_rowconfigure(0, weight=0)

        button = ctk.CTkButton(
            master=self,
            text=obj["name"],
            width=170,
            text_color="black",
            fg_color="transparent",
            hover=False,
            height=30,
            command=lambda: self.show(obj["host"], obj["port"])
        )
        button.grid(row=0, column=0, padx=5, pady=5)

    def show(self, host, port):
        if main_window.cdrone < 2:
            main_window.cdrone += 1
        else:
            main_window.cdrone = 0


class ScrollView(ctk.CTkScrollableFrame):
    def __init__(self, master, base, **kwargs):
        super().__init__(master, **kwargs)
        with open("../Data/drone.json", "r", encoding="utf-8") as file:
            data = json.load(file)

            for num, obj in enumerate(data["drones"], start=0):
                obj = frame(base, obj, self, width=170, height=40, corner_radius=10, fg_color="white")
                obj.grid(row=num, column=0, padx=10, pady=(5, 0))
