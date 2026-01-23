from typing import Callable

import pygame

from singletons.eventBus import event_bus

from uiComponents.button import Button

from ui.uiElement import UIElement


ELEMENT_SIZE: tuple[int, int] = (500, 200)
W_HALF: int = 250
H_HALF: int = 100

TEXT_DECREASE: int = 10

class ConfirmElement(UIElement):
    def __init__(self, text: str, confrim_command: Callable[[None], None], confirm_text: str = 'Confirm', cancel_text: str = 'Cancel') -> None:
        screen = pygame.display.get_surface()
        
        super().__init__(
            name='Confirm',
            title='Confirmation',
            size=ELEMENT_SIZE,
            pos=(
                (screen.size[0] / 2) - W_HALF,
                (screen.size[1] / 2) - H_HALF,
            ),
            write_config=False
        )
        
        self.text: str = text

        self.confrim_command: Callable[[None], None] = self.cancel
        if confrim_command:
            self.confrim_command = confrim_command

        self.confirm_text: str = confirm_text
        self.cancel_text: str = cancel_text
        
        self.add_component(
            'Confirm',
            Button(
                pos=(30, 135),
                size=(198, 38),
                image='.\\assets\\icons\\button.png',
                image_hover='.\\assets\\icons\\button_hover.png',
                command=self.confirm,
                text=self.confirm_text
            )
        )
        
        self.add_component(
            'Cancel',
            Button(
                pos=(272, 135),
                size=(198, 38),
                image='.\\assets\\icons\\button.png',
                image_hover='.\\assets\\icons\\button_hover.png',
                command=self.cancel,
                text=self.cancel_text
            )
        )
    
    def change_cancel_commnad(self, command: Callable[[None], None]) -> None:
        self.get_component('Cancel').command = command
        
    def draw(self, screen: pygame.Surface) -> None:
        super().draw(screen)
        
        if self.pos[0] != (screen.size[0] / 2) - W_HALF \
        or self.pos[1] != (screen.size[1] / 2) - H_HALF:
                    
            self.pos = (
                (screen.size[0] / 2) - W_HALF,
                (screen.size[1] / 2) - H_HALF
            )
        
        lines: list[str] = self.text.split('\n')
        
        text_size: tuple[int, int] = self.font.size(self.text)
        y: float = H_HALF - ((text_size[1] * len(lines)) / 2) - TEXT_DECREASE
        
        for line in lines:
            self.render_text(line, '#EEE1C5', (W_HALF - (self.font.size(line)[0] / 2), y))
            y += text_size[1]
            
        screen.blit(self.image, self.pos)
        
        for comp in self.components.values():
            comp.draw(screen, self.pos)
        
    def confirm(self) -> None:
        event_bus.sign('play_se', 'confirm')
        self.confrim_command()
        
    def cancel(self) -> None:
        event_bus.sign('play_se', 'cancel')
        self.deregister()
            
        event_bus.sign('ui_window', None)