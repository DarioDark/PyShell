from typing import Literal
import inspect


class CommandHandler:
    def __init__(self, master, console):
        self.master = master
        self.console = console

        self.last_function: str = ""

    def get_command_function(self, command: str) -> str:
        command: str = command.split(" ")[0]
        self.last_function = command
        return command

    @staticmethod
    def get_command_arg(command: str) -> str:
        arg: list[str] = command.split(" ")
        if len(arg) > 1:
            return arg[1]
        return "No argument provided"

    @staticmethod
    def get_command_options(command: str) -> list[str | None]:
        options: list[str] = command.split(" ")
        if len(options) > 2:
            return options[2:]
        return []

    def process_command(self, command: str) -> None:
        function = self.get_command_function(command)
        arg = self.get_command_arg(command)
        options = self.get_command_options(command)
        if function == '':
            self.console.new_line()
            return

        self.console.break_line()
        function_found: bool = function in CommandHandler.command_dict
        if not function_found:
            self.console.print_line(f"Command '{function}' not found")
            self.console.new_line()
            return

        # No argument needed
        if function == "clear":
            self.clear()
            return
        elif function == "exit":
            self.exit()
            return

        # Argument needed
        arg_provided: bool = arg != "No argument provided"
        if not arg_provided:
            self.console.print_line("No argument provided")
            self.console.new_line()
            return

        result: list[str] = CommandHandler.command_dict[function](arg, *options)
        for i in range(len(result)):
            self.console.print_line(result[i])
        self.console.break_line()
        self.console.new_line()
        return

    @staticmethod
    def calculate(arg: str, *options: str) -> list[str]:
        """Calculate the result of a mathematical expression."""
        try:
            return [str(eval(arg))]
        except ZeroDivisionError:
            return ["You can't divide by zero"]

    @staticmethod
    def pyshell(arg: str, *options: Literal["-f", "-c", "-p"]) -> list[str]:
        """Interact with the Python shell."""
        if arg == "":
            return ["This is a Python shell"]
        if arg == "-p":
            return ["Change properties: font, color, etc."]
        return ["Error : Invalid argument"]

    def clear(self) -> str:
        """Clear the console."""
        self.console.clear()
        return ""

    def exit(self) -> str:
        """Exit the shell."""
        self.console.print_line("Exiting...")
        self.master.master.after(500, self.master.master.on_close)
        return "Exiting..."

    def show_help(self, arg: str, *options: str) -> list[str]:
        """Display help information about commands."""
        print(f"arg: {arg}")
        if arg == "":
            return [f"{func.__name__.upper()} : {func.__doc__}" for func in CommandHandler.command_dict.values()] +[""] + ["For more info about a command, type HELP and then the command"]

        if arg in CommandHandler.command_dict.keys():
            result = []
            for name, param in inspect.signature(CommandHandler.command_dict[arg]).parameters.items():
                if param.annotation == Literal:
                    result.append(f"{arg.upper()} : {CommandHandler.command_dict[arg].__doc__} : {param.annotation.__args__}")
                else:
                    result.append(f"{arg.upper()} : {CommandHandler.command_dict[arg].__doc__} : {param.annotation}")
            return result
        return ["Command not found"]

    command_dict: dict[str, callable] = {"calc": calculate,
                                         "exit": exit,
                                         "help": show_help,
                                         "clear": clear,
                                         "pyshell": pyshell}
