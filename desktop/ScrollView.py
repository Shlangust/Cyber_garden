import tkinter as tk

import customtkinter as ctk


class ScrollView(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.label = ctk.CTkLabel(self)
        self.label.grid(row=0, column=0, padx=20)

        frame = ctk.CTkFrame(
            master=self,
            width=180,
            height=50,
            fg_color="white"
        )
        frame.grid(row=0, column=0, padx=10, pady=(5, 0))