import _tkinter

import customtkinter as ctk
from console import Console
from command_handler import CommandHandler


class PyShell(ctk.CTk):
    """The main window of the application."""
    def __init__(self, width, height, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.title("PyShell")
        self.iconbitmap("assets/terminal_icon.ico")

        # Center the window
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.resizable(False, False)

        self.create_widgets()
        self.place_widgets()

        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.mainloop()

    def create_widgets(self):
        self.main_frame = MainFrame(self)

    def place_widgets(self):
        self.main_frame.pack(pady=20, padx=10, fill="both", expand=True)

    def on_close(self):
        """Called when the window is closed."""
        self.destroy()


class MainFrame(ctk.CTkFrame):
    """The main frame of the application."""
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
        """Processes the command when the Enter key is pressed."""
        # If the current line is not the last line, prevent the Enter key event
        if self.console.index("insert linestart") != self.console.index("end-1c linestart"):
            return "break"

        # Get the command from the console
        line = self.console.get_last_line().strip().lower()
        self.command_handler.manage_user_input(line)
        return "break"

    def on_key_pressed(self, event):
        """Prevents the user from editing the console."""
        # If the current line is not the last line, prevent the key event
        if self.console.index("insert linestart") != self.console.index("end-1c linestart"):
            return "break"

        # If the current line is the last line and the cursor is at the start of the line, prevent the key event
        if event.keysym == "BackSpace":
            if self.console.index("insert") < self.console.index("end-1c linestart+19c"):
                return "break"

        if event.keysym == "BackSpace":
            try:
                if self.console.index("sel.first") < self.console.index("end-1c linestart+19c") or self.console.index("sel.last") < self.console.index("end-1c linestart+19c"):
                    return "break"
            except _tkinter.TclError:  # If there is no selection, this will be raised
                pass

        # Iterates through the last functions used
        if event.keysym == "Up":
            self.last_function_used_index -= 1
            self.last_function_used_index = max(-len(self.command_handler.last_commands), self.last_function_used_index)
            self.console.write(self.command_handler.last_commands[self.last_function_used_index])
            return "break"

        # Iterates through the last functions used
        if event.keysym == "Down":
            self.last_function_used_index += 1
            self.last_function_used_index = min(0, self.last_function_used_index)
            self.console.write(self.command_handler.last_commands[self.last_function_used_index])
            return "break"

        # Insert colored text for each key press
        if event.char.isprintable():
            self.console.delete("insert")
            self.console.insert("insert", event.char, self.console.typing_color)
            return "break"


if __name__ == "__main__":
    PyShell(1100, 800)
