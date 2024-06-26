import tkinter as tk

import customtkinter as ctk

import ScrollView
import KeyProcesses
import drone_control


class enterWindow(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.start()

    def start(self):
        self.grid_rowconfigure(index=0, weight=1)
        self.grid_rowconfigure(index=1, weight=0)
        self.grid_rowconfigure(index=2, weight=0)
        self.grid_rowconfigure(index=3, weight=0)
        self.grid_rowconfigure(index=4, weight=1)
        self.grid_columnconfigure(index=0, weight=0)
        self.grid_columnconfigure(index=1, weight=1)
        self.grid_columnconfigure(index=2, weight=0)

        main_label = ctk.CTkLabel(
            master=self,
            text="НАЗВАНИЕ",
            fg_color="transparent",
            font=("MONTSERRAT", 30, "bold")
        )
        main_label.grid(row=0, column=1, columnspan=2, sticky=tk.N, pady=(5, 0), padx=0)

        scroll = ScrollView.ScrollView(
            master=self,
            width=200,
            corner_radius=0,
            fg_color="transparent",
            scrollbar_fg_color="#F2F2F2",
            scrollbar_button_color="#F2F2F2",
            scrollbar_button_hover_color="#F2F2F2",
        )
        scroll.grid(row=0, column=0, rowspan=5, sticky=tk.NSEW)

        label = ctk.CTkLabel(
            master=self,
            text="Подключитесь к дрону",
            fg_color="transparent",
            text_color="#4895EF",
            font=("Montserrat", 25, "bold")
        )
        label.grid(row=1, column=1, columnspan=2, sticky=tk.S, pady=(0, 10))

        self.entry_1 = ctk.CTkEntry(
            master=self,
            height=40,
            font=("Montserrat", 20, "bold"),
            border_width=0,
            fg_color="white",
            placeholder_text="ip адрес"
        )
        self.entry_1.grid(row=2, column=1, sticky=tk.NSEW, padx=(0, 10))

        self.entry_2 = ctk.CTkEntry(
            master=self,
            height=40,
            font=("Montserrat", 20, "bold"),
            border_width=0,
            fg_color="white",
            placeholder_text="порт"
        )
        self.entry_2.grid(row=2, column=2, sticky=tk.NSEW, padx=(0, 10))

        self.entry_3 = ctk.CTkEntry(
            master=self,
            height=40,
            font=("Montserrat", 20, "bold"),
            border_width=0,
            fg_color="white",
            placeholder_text="название"
        )
        self.entry_3.grid(row=3, column=1, columnspan=2, sticky=tk.NSEW, pady=(10, 0), padx=(0, 10))

        button = ctk.CTkButton(
            master=self,
            text="ПОДКЛЮЧИТЬСЯ",
            text_color="white",
            fg_color="#4895EF",
            corner_radius=15,
            font=("Montserrat", 25, "bold"),
            width=300,
            height=70,
            command=self.button_click
        )
        button.grid(row=4, column=1, columnspan=2, sticky=tk.S, pady=(0, 25))

    def button_click(self):
        print("нажатие кнопки!")