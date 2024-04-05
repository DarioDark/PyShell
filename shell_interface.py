import customtkinter as ctk

from console import Console
from command_handler import CommandHandler

class PyShell(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.title("PyShell")

        # Center the window
        width = 1100
        height = 700

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.geometry(f"{width}x{height}+{x}+{y}")
        self.resizable(False, False)

        # Main frame
        self.main_frame = MainFrame(self)
        self.main_frame.pack(pady=20, padx=10, fill="both", expand=True)

        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.mainloop()

    def on_close(self):
        self.destroy()


class MainFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=20, fg_color="#1B1B1B")
        self.master = master

        self.last_function_used_index: int = 0

        self.create_widgets()
        self.bind_widgets()
        self.place_widgets()

    def create_widgets(self):
        self.console = Console(self)
        self.command_handler = CommandHandler(self, self.console)

    def bind_widgets(self):
        self.console.bind("<Return>", self.on_enter_pressed)  # Bind the Enter key to the on_enter_pressed method
        self.console.bind("<Key>", self.on_key_pressed)  # Bind the Key event to the on_key_pressed method

    def place_widgets(self):
        self.console.pack(expand=True, fill=ctk.BOTH, side=ctk.LEFT, pady=10, padx=5)

    def on_enter_pressed(self, event):
        if self.console.index("insert linestart") != self.console.index("end-1c linestart"):
            return "break"  # If the current line is not the penultimate line, prevent the key event
        line = self.console.get_last_line()[18:]
        print(f"line: {line}")
        self.command_handler.process_command(line)
        return "break"

    def on_key_pressed(self, event):
        if self.console.index("insert linestart") != self.console.index("end-1c linestart"):
            return "break"
        if event.keysym == "BackSpace":
            if self.console.index("insert") < self.console.index("end-1c linestart+19c"):
                return "break"
        # arrow up
        if event.keysym == "Up":
            self.last_function_used_index -= 1
            self.last_function_used_index = max(-len(self.command_handler.last_functions), self.last_function_used_index)
            print(self.last_function_used_index, self.command_handler.last_functions)
            self.console.delete("end-1c linestart", "end-1c")
            self.console.insert("end-1c", "classical@user ~$ " + self.command_handler.last_functions[self.last_function_used_index])
            return "break"
        # arrow down
        if event.keysym == "Down":
            self.last_function_used_index += 1
            self.last_function_used_index = min(0, self.last_function_used_index)
            print(self.last_function_used_index, self.command_handler.last_functions)
            self.console.delete("end-1c linestart", "end-1c")
            self.console.insert("end-1c", "classical@user ~$ " + self.command_handler.last_functions[self.last_function_used_index])
            return "break"

    def get_line_length(self):
        return len(self.console.get('end-1c linestart', 'end-1c'))

    def get_last_line_index(self):
        return self.console.get_last_line_index()


if __name__ == "__main__":
    PyShell()
