from typing import Callable

import pygame

from singletons import resourceHandler
from singletons.keyBus import key_bus


class ContextMenuOption():
    def __init__(self, mouse_pos: tuple[int, int], pos: tuple[int, int], text: str, call: Callable[[None], None]) -> None:
        self.pos: tuple[int, int] = pos
        self.text: str = text
        self.size: tuple[int, int] = (164, 24)
        self.call: Callable[[None], None] = call
        
        self.image: pygame.Surface = pygame.Surface(self.size, pygame.SRCALPHA)
        
        self.rect: pygame.Rect = self.image.get_rect(topleft=(mouse_pos[0] + self.pos[0], mouse_pos[1] + self.pos[1]))
        
        self.font: pygame.Font = resourceHandler.load_font('.\\assets\\fonts\\noto-sans.regular.ttf', 18)

        self.hovering: bool = False
        self.clicked: bool = False

        self.hover_background: pygame.Surface = resourceHandler.load_image('.\\assets\\backgrounds\\ContextMenuHoverBackground.png')
        self.clciked_background: pygame.Surface = resourceHandler.load_image('.\\assets\\backgrounds\\ContextMenuClickedBackground.png')
        
        key_bus.register('mouse_left_down', self.on_click)
        
    def deregister(self) -> None:
        key_bus.deregister('mouse_left_down', self.on_click)
        
    def draw(self, screen: pygame.Surface) -> None:
        if self.text == '': return

        if self.hovering:
            screen.blit(self.hover_background, (self.pos[0] - 9, self.pos[1] + 2))
        if self.clicked:
            screen.blit(self.clciked_background, (self.pos[0] - 9, self.pos[1] + 2))

        screen.blit(self.font.render(self.text, True, '#000000'), (self.pos[0], self.pos[1] + 1))
        screen.blit(self.font.render(self.text, True, '#DED2B8'), (self.pos))

    def hover(self) -> None:
        self.hovering = True

    def no_hover(self) -> None:
        if not self.hovering:
            return
        
        self.hovering = False
        
    def on_click(self) -> None:
        if not self.text or not self.hovering: return
        
        self.clicked = True
        self.call()