import re

import pygame

from menu.ui.changelogElement import ChangelogElement
from singletons import resourceHandler

from singletons.eventBus import event_bus
from singletons.keyBus import key_bus

from uiComponents.button import Button

from ui.uiElement import UIElement


ELEMENT_SIZE: tuple[int, int] = (400, 360)
W_HALF: int = 200
H_HALF: int = 180

class ChangelogViewElement(UIElement):
    def __init__(self) -> None:
        screen = pygame.display.get_surface()
        
        super().__init__(
            name='Changelogs',
            title='Changelogs',
            size=ELEMENT_SIZE,
            pos=(
                (screen.size[0] / 2) - W_HALF,
                (screen.size[1] / 2) - H_HALF,
            ),
            write_config=False
        )
        
        self.add_component('Version 0.94',
            Button(
                pos=(30, 55),
                size=(370, 24),
                image=None,
                image_hover='.\\assets\\backgrounds\\EscapeMenuHoverBackground.png',
                command=self.load_changelog,
                text='Version 0.94'
            )
        )
        
        self.add_component('Version 0.93.1',
            Button(
                pos=(30, 80),
                size=(370, 24),
                image=None,
                image_hover='.\\assets\\backgrounds\\EscapeMenuHoverBackground.png',
                command=self.load_changelog,
                text='Version 0.93.1'
            )
        )
        
        self.add_component('Version 0.93',
            Button(
                pos=(30, 105),
                size=(370, 24),
                image=None,
                image_hover='.\\assets\\backgrounds\\EscapeMenuHoverBackground.png',
                command=self.load_changelog,
                text='Version 0.93'
            )
        )
        
        self.add_component('Version 0.92.x',
            Button(
                pos=(30, 130),
                size=(370, 24),
                image=None,
                image_hover='.\\assets\\backgrounds\\EscapeMenuHoverBackground.png',
                command=self.load_changelog,
                text='Version 0.92.x'
            )
        )
        
        for button in self.components.values():
            if not isinstance(button, Button):
                continue
            
            button.left_algin_text()
            button.change_text_color('#DED2B8')
            
        key_bus.deregister('mouse_left_down', self.check_off_click)
        
    def draw(self, screen: pygame.Surface) -> None:
        super().draw(screen)
        
        if self.pos[0] != (screen.size[0] / 2) - W_HALF \
        or self.pos[1] != (screen.size[1] / 2) - H_HALF:
                    
            self.pos = (
                (screen.size[0] / 2) - W_HALF,
                (screen.size[1] / 2) - H_HALF
            )
        
        screen.blit(self.image, self.pos)
        
        for comp in self.components.values():
            comp.draw(screen, self.pos)
            
    def load_changelog(self) -> None:
        changelog: str = ''
        for comp in self.components.values():
            if not isinstance(comp, Button):
                continue
            
            if comp.hovering:
                changelog = comp.text
                break
            
        for log in resourceHandler.load_dir('.\\changelogs\\'):
            log_file: dict = resourceHandler.load_json(f'.\\changelogs\\{log}')
            
            if changelog.split()[1] in log_file['name'].split():
                event_bus.sign('ui_window', ChangelogElement(log_file), True)
                return