import inspect
from typing import Literal
from threading import Thread


class CommandHandler:
    """Handles the commands and the entry of the user."""
    available_colors: list[str] = ["white", "red", "green", "blue", "yellow", "cyan", "magenta"]

    def __init__(self, master, console):
        self.master = master
        self.console = console
        self.command_dict: dict[str, callable] = {"calc": self.calc,
                                                  "exit": self.exit,
                                                  "help": self.show_help,
                                                  "clear": self.clear,
                                                  "pyshell": self.pyshell}
        self.last_commands: list[str] = [""]
        self.status: Literal["waiting for response", "waiting for command"] = "waiting for command"
        self.minimum_line_length: int = self.console.user_length + 1

    def save_last_command(self, function: str, arg: str, *options: str) -> None:
        """Save the last command."""
        if arg == "No argument provided":
            arg = ""
        self.last_commands.append(function + " " + arg + " " + " ".join(options).replace("  ", ""))
        return

    def get_command_function(self, command: str) -> str:
        """Get the function of the command."""
        command: str = command.split(" ")[0]
        self.last_function = command
        return command

    def get_command_arg(self, command: str) -> str:
        """Get the argument of the command."""
        arg: list[str] = command.split(" ")
        if len(arg) > 1:
            return arg[1]
        return "No argument provided"

    def get_command_options(self, command: str) -> list[str | None]:
        """Get the options of the command."""
        options: list[str] = command.split(" ")
        if len(options) > 2:
            return options[2:]
        return []

    def check_provided_command(self, function: str, arg: str) -> bool:
        """Check if the command has a valid function, argument and options."""
        # If the function is empty, break the line
        if function == '':
            self.console.new_line()
            return False

        # If the function is not found, print an error message
        function_found: bool = function in self.command_dict.keys()
        if not function_found:
            self.console.print_line(f"Command '{function}' not found")
            self.console.new_line()
            return False

        # Functions that don't need an argument
        if function == "clear":
            self.clear()
            self.last_commands.append("clear")
            return False
        elif function == "exit":
            self.exit()
            self.last_commands.append("exit")
            return False

        # For the functions that need an argument, if no argument is provided, print an error message
        arg_provided: bool = arg != "No argument provided"
        if not arg_provided and function != "help":
            self.console.print_line("No argument provided")
            self.console.new_line()
            return False
        return True

    def process_command(self, line: str) -> None:
        """Process the command and print the result to the console."""
        # Get the function, argument and options of the command
        command: str = line[18:].strip().lower()
        function: str = self.get_command_function(command)
        arg: str = self.get_command_arg(command)
        options: list[str] = self.get_command_options(command)

        # Check if the command is valid
        if self.check_provided_command(function, arg):
            # Execute the command and print the result to the console
            result: list[str] = self.command_dict[function](arg, *options)
            print(function, arg, options, result)
            self.print_to_console(result)

        self.save_last_command(function, arg, *options)

    def process_response(self, line: str) -> None:
        """Process the response of the user."""
        response: str = line.split(" ")[-1]
        if response.lower() == "y":
            response = "-y"

        command = self.last_commands[-1].strip().lower()
        self.status = "waiting for command"
        function: 'function' = self.command_dict[self.get_command_function(command)]
        arg = self.get_command_arg(command)
        options = self.get_command_options(command) + [response]
        result = function(arg, *options)
        self.print_to_console(result)

    def manage_user_input(self, line: str) -> None:
        """Manage the user input."""
        if self.status == "waiting for command":
            self.process_command(line)
        elif self.status == "waiting for response":
            self.process_response(line)

    def print_to_console(self, text: list[str]) -> None:
        """Print the text to the console, line by line."""
        for i in range(len(text)):
            self.console.print_line(text[i])

        if self.status == "waiting for command":
            self.console.break_line()
            self.console.new_line()

    def clear(self) -> str:
        """Clear the console."""
        self.console.clear()
        return ""

    def exit(self) -> str:
        """Exit the shell."""
        self.console.print_line("Exiting...")
        self.master.master.after(500, self.master.master.on_close)
        return "Exiting..."

    def calc(self, arg: Literal["calculus"], *options: str) -> list[str]:
        """Calculate the result of a mathematical expression."""
        try:
            return [str(eval(arg))]
        except ZeroDivisionError:
            return ["You can't divide by zero"]

    def pyshell(self, arg: Literal["tc : Change the typing color.", "-uc : Changes the font color of the super user."], *options: str) -> list[str]: # TODO attribute a color invidually to each user
        """Interact with the Python shell."""
        if arg == "":
            return ["This is a Python shell, use one of the following options to change the properties of the shell: -tc, -uc"]
        if arg == "tc":
            color_given: list[str] = [color for color in options if color in CommandHandler.available_colors]
            if len(color_given) == 0:
                formatted_colors = ', '.join(CommandHandler.available_colors)
                return [f"Error : Invalid color, use one of the following colors : {formatted_colors}."]
            color_picked: str = color_given[0]
            if color_picked not in CommandHandler.available_colors:
                return ["Error : Invalid color"]
            if "-y" in options:
                self.console.typing_color = color_given
                return ["Typing color changed to " + color_picked]
            else:
                self.status = "waiting for response"
                return ["Are you sure you want to change the typing color? (y/n) "]

        if arg == "uc":
            if len(options) == 0:
                self.status = "waiting for response"
                return ["Attribute a color to each user: ", "Classical User -> "]
            if len(options) == 1:
                self.status = "waiting for response"
                return ["Super User -> "]
            if len(options) == 2:
                self.status = "waiting for response"
                return ["Are you sure you want to change the user colors? (y/n) "]
            if len(options) == 3 and options[2] == "-y":
                self.status = "waiting for command"
                self.console.users_colors["classical"] = options[0]
                self.console.users_colors["super"] = options[1]
                return ["User colors changed"]

    def show_help(self, arg: Literal["A function."], *options: str) -> list[str]:
        """Display help information about commands."""

        if arg == "No argument provided":
            return [f"{func.__name__.upper()} : {func.__doc__}" for func in self.command_dict.values()] + [""] + ["For more info about a command, type HELP and then the command."]

        if arg in self.command_dict.keys():
            result = [f"{arg.upper()} : {self.command_dict[arg].__doc__}"]

            sig = inspect.signature(self.command_dict[arg])
            params = sig.parameters

            if len(params) > 1:
                result[0] += " \nArgs : "
            else:
                return result

            for name, param in params.items():
                try:
                    is_literal = param.annotation.__origin__ == Literal
                except AttributeError:
                    is_literal = False
                if is_literal:
                    result.append(param.annotation.__args__.__str__().replace("(", "").replace(")", "\n\nOptions : ").replace("'", "").replace(", ", "\n").replace("-", "     -"))
                else:
                    # TODO optional arguments
                    result.append("     -" + param.annotation.__name__.capitalize())
            return result
        return ["Command not found"]
