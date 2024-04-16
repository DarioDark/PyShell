import customtkinter as ctk

from typing import Literal


class Console(ctk.CTkTextbox):
    """A custom console widget."""
    def __init__(self, master):
        super().__init__(master, wrap=ctk.WORD, width=1050, height=650, font=("Cascadia Code", 17), fg_color="transparent",
                         bg_color="transparent", activate_scrollbars=False, state="normal", corner_radius=10)
        self.master = master
        self.user: Literal["classical", "super"] = "classical"
        self.users_colors: dict[str, str] = {"classical": "yellow", "super": "red"}
        self.user_color: str = self.users_colors[self.user]
        self.typing_color: str = "white"

        self.config_tags()

        self.string = "classical@user ~$ "
        self.new_line(line_break=False)

    @property
    def user_length(self):
        return len(self.string)

    def config_tags(self):
        self.tag_config("white", foreground="white")
        self.tag_config("red", foreground="red")
        self.tag_config("green", foreground="green")
        self.tag_config("blue", foreground="blue")
        self.tag_config("yellow", foreground="yellow")
        self.tag_config("cyan", foreground="cyan")
        self.tag_config("magenta", foreground="magenta")

    def get_last_line_index(self):
        return self.index("end-1c")

    def get_last_line(self):
        return self.get('end-1c linestart', 'end-1c')

    def print_line(self, line: str):
        self.insert(ctk.END, "\n" + line)

    def break_line(self):
        self.insert(ctk.END, "\n")

    def clear(self):
        """Clear the console."""
        self.delete("1.0", ctk.END)
        self.new_line(line_break=False)

    def new_line(self, line_break=True):
        """Add a new blank line to the console, you can choose to add a line break or not"""
        if line_break:
            text_to_insert = "\n" + self.string
        else:
            text_to_insert = self.string

        self.insert(ctk.END, text_to_insert, self.user_color)
        # Moves the cursor to the end of the console
        self.see(ctk.END)
        self.mark_set(ctk.INSERT, ctk.END)

    def write(self, text: str):
        """Write text to the console (on the same line)."""
        self.delete(f"end-1c linestart +{self.user_length}c", "end-1c lineend")
        self.insert(f"end-1c linestart +{self.user_length}c", text, self.typing_color)
