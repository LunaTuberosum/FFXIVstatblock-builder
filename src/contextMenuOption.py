from typing import Callable

import pygame

from singletons import resourceHandler

from singletons.keyBus import key_bus
from singletons.eventBus import event_bus


IMAGE_POS: tuple[int, int] = (10, 2)

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
        self.clicked_background: pygame.Surface = resourceHandler.load_image('.\\assets\\backgrounds\\ContextMenuClickedBackground.png')
        
        key_bus.register('mouse_left_down', self.on_click)
        
    def deregister(self) -> None:
        key_bus.deregister('mouse_left_down', self.on_click)
        
    def draw(self, screen: pygame.Surface) -> None:
        if self.text == '': return

        if self.hovering:
            screen.blit(self.hover_background, (self.pos[0] - IMAGE_POS[0], self.pos[1] + IMAGE_POS[1]))
        if self.clicked:
            screen.blit(self.clicked_background, (self.pos[0] - IMAGE_POS[0], self.pos[1] + IMAGE_POS[1]))

        screen.blit(self.font.render(self.text, True, '#000000'), (self.pos[0], self.pos[1] + 1))
        screen.blit(self.font.render(self.text, True, '#DED2B8'), (self.pos))

    def hover(self) -> None:
        if self.hovering:
            return
        
        event_bus.sign('play_se', 'hover')
        self.hovering = True

    def no_hover(self) -> None:
        if not self.hovering:
            return
        
        self.hovering = False
        
    def on_click(self) -> None:
        if not self.text or not self.hovering: return
        
        event_bus.sign('play_se', 'confirm')
        
        self.clicked = True
        self.call()