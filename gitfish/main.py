import typer
import asyncio
from rich.console import Console
from rich.panel import Panel
from gitfish.game import cast_loop

app = typer.Typer()
console = Console()

@app.command()
def start():
    """Greeting message"""
    console.print(Panel("Fishing awaits!", title="Gitfish", style="bold green"))

@app.command()
def cast():
    try:
        asyncio.run(cast_loop())
    except KeyboardInterrupt:
        console.print("You reel your line in.")

@app.command()
def sync():
    """sync your github activity"""
    console.print(Panel("syncing github activity", style="blue"))

if __name__ == "__main__":
    app()