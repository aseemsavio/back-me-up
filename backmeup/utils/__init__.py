from rich.console import Console


def print_error(message: str = "Something went wrong!"):
    console = Console()
    console.print(f"[bold red]Error:[/] {message}")
