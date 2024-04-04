import time
import tkinter as tk
import sys
import subprocess
import customtkinter as ctk


class PyShell(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.title("PyShell")

        # Center the window
        width = 800
        height = 600

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.geometry(f"{width}x{height}+{x}+{y}")
        self.resizable(False, False)

        # Main frame
        self.main_frame = MainFrame(self)
        self.main_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.mainloop()

    def on_close(self):
        self.destroy()


class MainFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=10, fg_color="#1B1B1B")
        self.master = master

        self.create_widgets()
        self.bind_widgets()
        self.place_widgets()

    def create_widgets(self):
        self.right_console = RightConsole(self)
        self.left_console = LeftConsole(self)

    def bind_widgets(self):
        self.right_console.bind("<Return>", self.on_enter_pressed)  # Bind the Enter key to the on_enter_pressed method
        self.right_console.bind("<Key>", self.on_key_pressed)  # Bind the Key event to the on_key_pressed method

    def place_widgets(self):
        self.left_console.pack(expand=True, fill=ctk.BOTH, side=ctk.LEFT)
        self.right_console.pack(expand=True, fill=ctk.BOTH, side=ctk.RIGHT)

    def on_enter_pressed(self, event):
        if self.right_console.index("insert linestart") != self.right_console.index("end-1c linestart"):
            return "break"  # If the current line is not the penultimate line, prevent the key event
        last_line_index = str(float(self.get_last_line_index()) + 1.0)
        self.left_console.new_line(last_line_index, line_break=True)

    def on_key_pressed(self, event):
        if self.right_console.index("insert linestart") != self.right_console.index("end-1c linestart"):
            return "break"  # If the current line is not the penultimate line, prevent the key event
        if len(self.right_console.get('end-2c linestart', 'end-1c')) >= 55 and event.keysym != "BackSpace":
            return "break"  # If the last line is "57", prevent the key event

    def get_last_line_index(self):
        return self.right_console.get_last_line_index()


class LeftConsole(ctk.CTkTextbox):
    def __init__(self, master):
        super().__init__(master, wrap=tk.WORD, width=196, height=500, font=("Cascadia Code", 17), fg_color="#1B1B1B", bg_color="#1B1B1B", activate_scrollbars=False, state="disabled",
                         corner_radius=10)

        self.string = "classical@user ~$"

        self.line_break_counter: float = 2.0
        self.new_line("1.0", line_break=False)

        self.master = master

    def new_line(self, last_line_index, line_break=True):
        self.configure(state="normal")
        if line_break:
            text_to_insert = "\n" + self.string
        else:
            text_to_insert = self.string

        self.insert(last_line_index, text_to_insert)

        self.configure(state="disabled")


class RightConsole(ctk.CTkTextbox):
    def __init__(self, master):
        super().__init__(master, wrap=tk.WORD, width=605, height=500, font=("Cascadia Code", 17), fg_color="#1B1B1B", bg_color="#1B1B1B",
                         activate_scrollbars=False, state="normal", corner_radius=10, border_spacing=0)
        self.master = master
        
    def get_last_line_index(self):
        return self.index("end-1c linestart")


if __name__ == "__main__":
    PyShell()
