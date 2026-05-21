import pygame

from ui.uiElement import UIElement

from uiComponents.button import Button


ELEMENT_SIZE: tuple[int, int] = (610, 200)
W_HALF: int = 305
H_HALF: int = 100

class ChangelogElement(UIElement):
    def __init__(self):
        screen = pygame.display.get_surface()
        
        super().__init__(
            name='Changelog',
            title='Changelog',
            size=ELEMENT_SIZE,
            pos=(
                (screen.size[0] / 2) - W_HALF,
                (screen.size[1] / 2) - H_HALF,
            )
        )