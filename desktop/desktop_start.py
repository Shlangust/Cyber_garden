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
        window = main_window.MainWindow(self, fg_color="transparent")
        window.grid(row=0, column=0, sticky=tk.NSEW)

        self.bind('<KeyPress>', self.on_key_press)

    def on_key_press(self, event):
        if event.keysym in ('W', 'w'):
            KeyProcesses.press_w()
        elif event.keysym in ('A', 'a'):
            KeyProcesses.press_a()
        elif event.keysym in ('S', 's'):
            KeyProcesses.press_s()
        elif event.keysym in ('D', 'd'):
            KeyProcesses.press_d()
        elif event.keysym in ('Q', 'q'):
            KeyProcesses.press_q()
        elif event.keysym in ('E', 'e'):
            KeyProcesses.press_e()
        elif event.keysym == 'Return':
            KeyProcesses.press_enter()
        elif event.keysym == 'Shift_L' or event.keysym == 'Shift_R':
            KeyProcesses.press_shift()
        elif event.keysym == 'space':
            KeyProcesses.press_space()
        elif event.keysym == 'Up':
            KeyProcesses.press_up_arrow()
        elif event.keysym == 'Down':
            KeyProcesses.press_down_arrow()
        elif event.keysym == 'Left':
            KeyProcesses.press_left_arrow()
        elif event.keysym == 'Right':
            KeyProcesses.press_right_arrow()


if __name__ == "__main__":
    app = Window()
    app.mainloop()
