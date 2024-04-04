import customtkinter as ctk


class Console(ctk.CTkTextbox):
    def __init__(self, master):
        super().__init__(master, wrap=ctk.WORD, width=1050, height=650, font=("Cascadia Code", 17), fg_color="transparent",
                         bg_color="transparent", activate_scrollbars=False, state="normal", corner_radius=10)
        self.master = master
        self.string = "classical@user ~$ "
        self.new_line(line_break=False)

    def get_last_line_index(self):
        return self.index("end-1c")

    def get_last_line(self):
        return self.get('end-1c linestart', 'end-1c')

    def print_line(self, line: str):
        self.insert(ctk.END, "\n" + line)

    def clear(self):
        self.delete("1.0", ctk.END)
        self.new_line(line_break=False)

    def new_line(self, line_break=True):
        if line_break:
            text_to_insert = "\n" + self.string
        else:
            text_to_insert = self.string

        self.insert(ctk.END, text_to_insert)

    def break_line(self):
        self.insert(ctk.END, "\n")

    # TODO def wait_for_input(self):
