from asciimatics.screen import Screen
from asciimatics.effects import Print
from asciimatics.renderers import FigletText
from asciimatics.scene import Scene
from asciimatics.exceptions import StopApplication, NextScene
from time import sleep


def title_screen(screen: Screen):
    """
    Create the title screen. 
    """
    title = FigletText("Gitfish", font="big")
    effects = [
        Print(
            screen,
            title,
            x=(screen.width // 2) - 20,
            y=2,
            speed=1,
            transparent=False,
        )
    ]
    #     screen.play([Scene(effects, -1)])
    # Screen.wrapper(_title_screen)

    for effect in effects:
        effect.reset()

    welcome_prompt = "Welcome to Gitfish! Press any key to start fishing."
    frame = 0

    while True:
        screen.clear()

        for effect in effects:
            effect.update(frame)
        
        if (frame // 20) % 2 == 0:
            screen.print_at(
                welcome_prompt,
                (screen.width // 2) - (len(welcome_prompt) // 2),
                screen.height - 4
            )
        
        screen.refresh()
        frame += 1

        if screen.has_resized():
            screen.clear()
            for effect in effects:
                effect.reset()

        event = screen.get_event()
        if event:
            return
        
        sleep(0.02)
