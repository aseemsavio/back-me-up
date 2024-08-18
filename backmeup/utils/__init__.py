from rich.console import Console
from rich.panel import Panel


def _boxed_text(title: str, message: str, border_color: str):
    console = Console()
    console.print(Panel(message, title=title, title_align="left", highlight=True, border_style=border_color))
    console.line()


def print_error(message: str = "Something went wrong!"):
    _boxed_text(title="Error!", message=message, border_color="red")
