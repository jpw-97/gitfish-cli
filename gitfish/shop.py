from rich.console import Console
from rich.table import Table
from gitfish.state import load_state, save_state
from gitfish.models import BAIT_OPTIONS

console = Console()

def show_shop():
    """
    Command to show the Gitfish shop. Displays bait and equipment alongside their associated price, bonus, etc.
    """
    table = Table(title="Gitfish Shop", show_header=True, header_style="bold magenta")
    for column in ["Item", "Price", "Bonus"]:
        table.add_column(column)

    for key, item in BAIT_OPTIONS.items():
        table.add_row(
            f"{item['name']} ({key})",
            str(item['price']),
            f"+{item['bite_bonus']*100:.0f}% bite chance"
        )
    console.print(table)

def buy_item(item: str, quantity: int = 1):
    """
    Purchase items from shop above based on user input.
    """
    state = load_state()

    if item not in BAIT_OPTIONS:
        console.print(f"[red]{item} is not stocked.[/red]")
        return

    # bait = BAIT_OPTIONS.items()
    bait = BAIT_OPTIONS[item]
    cost = int(bait["price"]) * int(quantity)
    print(cost)

    if state["user"]["coins"] < cost:
        console.print(f"You cannot afford {quantity} {item}!")
        return

    state["user"]["coins"] -= cost

    inv = state.setdefault("inventory", {}).setdefault("bait", {})
    inv[item] = inv.get(item, 0) + int(quantity)

    save_state(state)
    console.print(f"Purchased {quantity}x {item} for {cost} coins.")