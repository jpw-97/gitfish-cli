import typer
import asyncio
from asciimatics.screen import Screen
from gitfish.graphics.title_screen import title_screen
from gitfish.state import load_state, save_state
from gitfish.github_sync import sync_from_github
from gitfish.game import cast_loop
from gitfish.shop import show_shop, buy_item
from gitfish.equip import equip_bait, equip_show
from rich.console import Console
from rich.panel import Panel


app = typer.Typer()
console = Console()

@app.command()
def start():
    """Start a Gitfish Session"""
    Screen.wrapper(title_screen)

    state = load_state()
    console.print(
        Panel("Fishing awaits!", title="Gitfish", style="bold green"))
    console.print(Panel(
        f"Your current stats: {state['user']['xp']} xp, {state['user']['coins']} coins."))
    console.print(Panel(
        "Type 'cast' to fish, 'sync' to sync any recent GitHub activity, and 'quit' to quit."))

    while True:
        cmd = input("> ").strip().lower()
        if cmd in ("quit", "exit", "q"):
            save_state(state)
            console.print("Progress has been saved. Goodbye!")
            break
        elif cmd == "cast":
            asyncio.run(cast_loop())
            state = load_state()
        elif cmd == "sync":
            res = sync_from_github()
            console.print(f"""Synced your Github activity. Most recent event found: {res["debug"]["most_recent_event_time"]} /n
            XP gained: {res["xp"]}, coins gained: {res["coins"]}.
            """)
        elif cmd == "stats":
            s = load_state()
            console.print(f"XP: {s['user']['xp']} | Coins: {s['user']['coins']} | Gear: {s['gear']}")
        elif cmd.startswith("equip"):
            parts = cmd.split()
            if len(parts) < 2:
                console.print("Usage: equip <bait_type>, equip show")
                continue
            bait_type = parts[1]
            if bait_type != "show":
                equip_bait(bait_type)
                state = load_state()
                continue
            else:
                equip_show()
                continue
        elif cmd.startswith("shop"):
            parts = cmd.split()
            if len(parts) < 2:
                console.print("Usage: shop view / shop buy <item> <quantity>.")
                continue
            if parts[1] == "view":
                show_shop()
            elif parts[1] == "buy":
                buy_item(parts[2], parts[3])
            continue
        else:
            console.print("Unknown command. Try cast, sync, stats, quit.")

if __name__ == "__main__":
    app()
