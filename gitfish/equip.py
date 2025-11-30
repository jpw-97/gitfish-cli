from rich.console import Console
from gitfish.models import BAIT_OPTIONS
from gitfish.state import load_state, save_state

console = Console()

def equip_bait(bait_type: str):
    """
    Action to equip specific bait that you have acquired.
    """
    state = load_state()

    if bait_type not in BAIT_OPTIONS:
        console.print("That bait does not exist. Check your spelling!")
        return

    inventory = state["inventory"]["bait"]
    if inventory.get(bait_type, 0) <= 0:
        console.print(f"You don't own any {bait_type}! Buy some by typing ex. 'shop {bait_type} 5'")
        return

    state["equipped_bait"] = bait_type
    save_state(state)

    bait = BAIT_OPTIONS[bait_type]
    console.print(f"Equipped {bait}!")

