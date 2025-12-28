from typing import Callable

import pygame

from singletons.eventBus import event_bus

from ui.confirmElement import ConfirmElement
from ui.uiElement import UIElement

from uiComponents.button import Button


ELEMENT_SIZE: tuple[int, int] = (430, 104)
H_BUFFER: int = 60
W_HALF: int = 215

class EscapeMenu(UIElement):
    def __init__(self, quit_options: dict[str, Callable[[None], None]]) -> None:
        screen = pygame.display.get_surface()
        
        super().__init__(
            name='EscapeMenu',
            title='System',
            size=(
                ELEMENT_SIZE[0],
                ELEMENT_SIZE[1] + H_BUFFER + (len(quit_options) * 25)
            ),
            pos=(
                (screen.size[0] / 2) - W_HALF,
                (screen.size[1] / 2) - ((ELEMENT_SIZE[1] + H_BUFFER + (len(quit_options) * 25)) / 2),
            ),
            write_config=False
        )
        
        self.add_component('Bug Report',
            Button(
                pos=(30, 55),
                size=(370, 24),
                image=None,
                image_hover='.\\assets\\backgrounds\\EscapeMenuHoverBackground.png',
                command=self.in_progress,
                text='Support Desk'
            )
        )
        
        self.add_component('Playguide',
            Button(
                pos=(30, 80),
                size=(370, 24),
                image=None,
                image_hover='.\\assets\\backgrounds\\EscapeMenuHoverBackground.png',
                command=self.in_progress,
                text='Playguide'
            )
        )
        
        self.add_component('Settings',
            Button(
                pos=(30, 105),
                size=(370, 24),
                image=None,
                image_hover='.\\assets\\backgrounds\\EscapeMenuHoverBackground.png',
                command=None,
                text='System Configuration'
            )
        )
        
        y: int = 130
        for option, call in quit_options.items():
            self.add_component(option,
                Button(
                    pos=(30, y),
                    size=(370, 24),
                    image=None,
                    image_hover='.\\assets\\backgrounds\\EscapeMenuHoverBackground.png',
                    command=call,
                    text=option
                )
            )
            
            y += 25
        
        for button in self.components.values():
            if not isinstance(button, Button):
                continue
            
            button.left_algin_text()
            button.change_text_color('#DED2B8')
        
    def draw(self, screen: pygame.Surface) -> None:
        super().draw(screen)
        
        if self.pos[0] != (screen.size[0] / 2) - W_HALF \
        or self.pos[1] != (screen.size[1] / 2) - self.size[1] / 2:
                    
            self.pos = (
                (screen.size[0] / 2) - W_HALF,
                (screen.size[1] / 2) - self.size[1] / 2
            )
            
        screen.blit(self.image, self.pos)
        
        for comp in self.components.values():
            comp.draw(screen, self.pos)
            
    def in_progress(self) -> None:
        event_bus.sign('ui_window', ConfirmElement(
            text='No yet implemented.\nSorry :P',
            confrim_command=None,
            confirm_text='Close',
            cancel_text='Close'
        ))
        