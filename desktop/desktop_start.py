import tkinter as tk

import customtkinter as ctk

import ScrollView
import enter_window
import main_window
import KeyProcesses

ctk.set_default_color_theme("dark-blue")
ctk.set_appearance_mode("light")


class Window(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.windows_size = (850, 500)
        self.monitor_height = self.winfo_screenheight()
        self.monitor_width = self.winfo_screenwidth()

        x = int((self.monitor_width - self.windows_size[0]) / 2)
        y = int((self.monitor_height - self.windows_size[1]) / 2)

        self.geometry(f'{self.windows_size[0]}x{self.windows_size[1]}+{x}+{y}')
        self.title('Название')
        self.configure(fg_color="#F2F2F2")

        self.start()

    def start(self):
        self.grid_rowconfigure(index=0, weight=1)
        self.grid_columnconfigure(index=0, weight=1)

        # window = enter_window.enterWindow(self, fg_color="transparent")
        window = main_window.MainWindow(self, self, fg_color="transparent")
        window.grid(row=0, column=0, sticky=tk.NSEW)


if __name__ == "__main__":
    app = Window()
    app.mainloop()
