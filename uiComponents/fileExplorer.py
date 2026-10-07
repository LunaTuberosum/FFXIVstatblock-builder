from typing import Callable
import pygame

from singletons import resourceHandler

from singletons.eventBus import event_bus
from singletons.dataBus import data_bus
from singletons.keyBus import key_bus

from uiComponents.componet import Component


class FileExplorer(Component):
    def __init__(self, pos: tuple[int, int]):
        super().__init__(
            pos,
            (350, 320)
        )
        self.face: pygame.Surface = resourceHandler.load_image(f'.\\assets\\ui\\{data_bus.sign('get_theme')}\\backgrounds\\ExplorerBackground.png')
        
        self.font: pygame.Font = resourceHandler.load_font('.\\assets\\fonts\\noto-sans.regular.ttf', 16)
        
        key_bus.register('mouse_left_down', self.on_click)
        key_bus.register('mouse_left_up', self.on_release)
        
    def deregister(self) -> None:
        key_bus.deregister('mouse_left_down', self.on_click)
        key_bus.deregister('mouse_left_up', self.on_release)
        
        super().deregister()
        
    def is_hover(self, mouse_pos: tuple[int, int]) -> bool:
        return False
        
    def on_click(self) -> None:
        if not self.hovering:
            return
        
        event_bus.sign('play_se', 'confirm')
        
    def on_release(self) -> None:
        pass
        
    def draw(self, screen: pygame.Surface, parent_pos: tuple[int, int]) -> None:
        super().draw(screen, parent_pos)
        
        self.image.blit(self.face)

        _y: int = 10
        for m_obj in resourceHandler.load_dir('.\\saves'):
            self.image.blit(self.font.render(f'{'> ' if not m_obj.endswith('.json') else ''}{m_obj}', True, '#CCCCCC'), (15, _y))
            _y += 25
            
        
        self.image.blit(self.font.render('123456789 123456789 123456789 12345678', True, '#CCCCCC'), (10, 290))
        
        screen.blit(self.image, self.rect.topleft)
        
    