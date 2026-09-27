import re

import pygame

from menu.ui.changelogElement import ChangelogElement

from singletons import resourceHandler

from singletons.dataBus import data_bus
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
        
        y: int = 55
        X_POS: int = 30
        SIZE: tuple[int, int] = (370, 24)
        
        changelogs: list[str] = resourceHandler.load_dir('.\\changelogs\\')
        changelogs.reverse()
        
        for change in changelogs:
            name: str = change.split('_')[1][:-5]
            
            if name == 'recent':
                log: dict[str, str] = resourceHandler.load_json('.\\changelogs\\changelog_recent.json')
                name = log['name'].split()[1]
                
            name = 'Version ' + name
            
            self.add_component(name,
                Button(
                    pos=(X_POS, y),
                    size=SIZE,
                    image=None,
                    image_hover=f'.\\assets\\ui\\{data_bus.sign('get_theme')}\\backgrounds\\EscapeMenuHoverBackground.png',
                    command=self.load_changelog,
                    text=name
                )
            )
            
            y += 25
        
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