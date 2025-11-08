import typer
from rich.console import Console
from rich.panel import Panel

app = typer.Typer()
console = Console()

@app.command()
def start():
    """Greeting message"""
    console.print(Panel("Fishing awaits!", title="Gitfish", style="bold green"))

@app.command()
def cast():
    """cast out your line"""
    console.print(Panel("you cast out your line", style="red"))

@app.command()
def sync():
    """sync your github activity"""
    console.print(Panel("syncing github activity", style="blue"))

if __name__ == "__main__":
    app()