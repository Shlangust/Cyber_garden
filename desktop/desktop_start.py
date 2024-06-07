import tkinter as tk

import customtkinter as ctk

ctk.set_default_color_theme("dark-blue")
ctk.set_appearance_mode("light")


class Window(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.windows_size = (1500, 750)
        self.monitor_height = self.winfo_screenheight()
        self.monitor_width = self.winfo_screenwidth()

        x = int((self.monitor_width - self.windows_size[0]) / 2)
        y = int((self.monitor_height - self.windows_size[1]) / 2)

        self.geometry(f'{self.windows_size[0]}x{self.windows_size[1]}+{x}+{y}')
        self.resizable(False, False)
        self.title('Название')

        self.start()

    def start(self):
        pass


if __name__ == "__main__":
    app = Window()
    app.mainloop()
