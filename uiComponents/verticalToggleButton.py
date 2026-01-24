from typing import Callable
import pygame

from singletons import resourceHandler

from singletons.keyBus import key_bus
from singletons.eventBus import event_bus

from uiComponents.componet import Component


class ButtonOption():
    def __init__(self, text: str, command: Callable[[str], None], pos: tuple[int, int]) -> None:
        self.text: str = text
        self.command: Callable[[str], None] = command
        self.pos: tuple[int, int] = pos
        
        self.font: pygame.Font = resourceHandler.load_font('.\\assets\\fonts\\noto-sans.regular.ttf', 20)
        
        text: pygame.Surface = self.font.render(self.text, True, '#EEE1C5')
        self.text_face: pygame.Surface = pygame.Surface((25 + text.size[0], 20), pygame.SRCALPHA)
        self.text_face.blit(text, (25, -8))
        
        self.rect: pygame.Rect = self.text_face.get_rect(topleft=self.pos)
        
        self.hovering: bool = False
        self.selected: bool = False
        
        self.button_image: pygame.Surface = resourceHandler.load_image('.\\assets\\icons\\ToggleButton.png')
        self.button_image_hover: pygame.Surface = resourceHandler.load_image('.\\assets\\icons\\ToggleButton_hover.png')
        self.button_image_selected: pygame.Surface = resourceHandler.load_image('.\\assets\\icons\\ToggleButton_selected.png')
        
        key_bus.register('mouse_left_down', self.on_click)
        
    def deregister(self) -> None:
        key_bus.deregister('mouse_left_down', self.on_click)
        
    def draw(self, screen: pygame.Surface, parent_pos: tuple[int, int]) -> None:
        self.rect.topleft = (self.pos[0] + parent_pos[0], self.pos[1] + parent_pos[1])
        
        screen.blit(self.text_face, (self.pos[0], self.pos[1] + 3))
        if self.selected: 
            screen.blit(self.button_image_selected, self.pos)
        elif self.hovering:
            screen.blit(self.button_image_hover, self.pos)
        else:
            screen.blit(self.button_image, self.pos)
        
    def on_click(self) -> None:
        if not self.hovering:
            return
        
        event_bus.sign('play_se', 'confirm')
        self.command(self.text)
        
    def no_hover(self) -> None:
        if not self.hovering:
            return
        self.hovering = False

    def hover(self) -> None:
        self.hovering = True

class VerticalToggleButtons(Component):
    def __init__(self, pos: tuple[int, int], size: tuple[int, int], options: dict[str, Callable[[str], None]], default: str) -> None:
        super().__init__(
            pos,
            size
        )
        
        self.options: dict[str, ButtonOption] = {}
        
        y: int = 0
        for option, call in options.items():
            button: ButtonOption = ButtonOption(option, call, (0, y))
            self.options[option] = button
            
            y += button.rect.height + 10
            
        self.button_selected: ButtonOption = self.options[default]
        
    def deregister(self):
        super().deregister()

        for button in self.options.values():
            button.deregister()
        
    def draw(self, screen: pygame.Surface, parent_pos: tuple[int, int]) -> None:
        super().draw(screen, parent_pos)
        
        for button in self.options.values():
            button.selected = button == self.button_selected
            button.draw(self.image, self.rect.topleft)

        screen.blit(self.image, self.rect.topleft)
        
    def no_hover(self) -> None:
        if not self.hovering:
            return
        
        for button in self.options.values():
            button.no_hover()
            
    def hover(self) -> None:
        self.hovering = True
        
        for button in self.options.values():
            button.no_hover()
            
            if button.rect.collidepoint(pygame.mouse.get_pos()):
                button.hover()
                
    def set_option(self, new_option: str) -> None:
        self.button_selected = self.options[new_option]