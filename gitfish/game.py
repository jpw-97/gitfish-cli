import asyncio
import random
from datetime import datetime, timezone
from rich.console import Console
from rich.panel import Panel
from gitfish.state import load_state, save_state
from gitfish.github_sync import sync_from_github

console = Console()


async def cast_loop(tick_interval=5):
    """
    Commences idle fishing loop for the specific tick duration.
    """

    state = load_state()
    user = state["user"]
    gear = state["gear"]

    console.print("You cast your line out...")
    console.print("Press CTRL+C to reel in.")

    # todo refine all _mod parameters / 'luck' system
    base_bite_chance = 0.8
    gear_mod = 0.01 * gear.get("rod_level", 1)
    level_mod = 0.01 * user.get("level", 1)
    total_mod = gear_mod + level_mod
    bite_chance = base_bite_chance + total_mod

    tick = 0

    try:
        while True:
            tick += 1
            await asyncio.sleep(tick_interval)

            if random.random() < bite_chance:
                console.print("Bite!!")
                await asyncio.sleep(1)

                # modifiers for catch success:
                catch_mod = 0.2
                # todo difficulty determined on type of fish
                fish_difficulty = random.randint(1, 10)
                catch_chance = 0.2 + (catch_mod - fish_difficulty)
                catch_chance = max(0.0, min(1.0, catch_chance))

                if random.random() < catch_chance:
                    # todo refine xp + coin gain
                    xp_gain = random.randint(5, 15)
                    coin_gain = random.randint(5, 15)
                    user["xp"] += xp_gain
                    user["coins"] += coin_gain

                    # todo level up logic

                    save_state(state)
                    console.print(Panel(
                        f"You caught a fish! {xp_gain} xp gained, {coin_gain} coins gained.",
                        title="Success!",
                        style="bold green"
                    ))
                    break
                else:
                    console.print("The fish got away...")
            else:
                console.print("Blub...")
    except KeyboardInterrupt:
        console.print("You reel your line in.")

