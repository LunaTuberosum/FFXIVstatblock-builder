from typing import Callable
import pygame

from singletons import resourceHandler

from singletons.keyBus import key_bus
from singletons.eventBus import event_bus

from uiComponents.componet import Component


class Bar(Component):
    def __init__(self, pos: tuple[int, int], command: Callable[[None], None]):
        super().__init__(
            pos,
            (202, 4)
        )
        
        self.command: Callable[[None], None] = command
        
        self.background: pygame.Surface = resourceHandler.load_image('.\\assets\\backgrounds\\BarBackground.png')
        
        self.foreground: pygame.Surface = resourceHandler.load_image('.\\assets\\backgrounds\\BarForeground.png')
        self.face: pygame.Surface = self.foreground.copy()
        
        self.handle: pygame.Surface = resourceHandler.load_image('.\\assets\\icons\\BarHandle.png')
        
        self.font: pygame.Font = resourceHandler.load_font('.\\assets\\fonts\\noto-sans.regular.ttf', 16)
        
        self.drag: bool = False
        
        self.percentage: int = 100
        
        key_bus.register('mouse_left_down', self.on_click)
        key_bus.register('mouse_left_up', self.on_release)
        
    def deregister(self) -> None:
        key_bus.deregister('mouse_left_down', self.on_click)
        key_bus.deregister('mouse_left_up', self.on_release)
        
        super().deregister()
        
    def on_click(self) -> None:
        if not self.hovering:
            return
        
        event_bus.sign('play_se', 'confirm')
        
        self.drag = True
        
        mouse: tuple[int, int] = pygame.mouse.get_pos()
        
        realtive: tuple[int, int] = (
            mouse[0] - self.rect.x,
            mouse[1] - self.rect.y
        )
        
        self.percentage = max(min(realtive[0] // 2, 100), 0)
        self.command()
        
    def on_release(self) -> None:
        self.drag = False
        
    def draw(self, screen: pygame.Surface, parent_pos: tuple[int, int]) -> None:
        super().draw(screen, parent_pos)
        
        if self.drag:
            mouse: tuple[int, int] = pygame.mouse.get_pos()
        
            realtive: tuple[int, int] = (
                mouse[0] - self.rect.x,
                mouse[1] - self.rect.y
            )
            self.percentage = max(min(realtive[0] // 2, 100), 0)
            self.command()
        
        self.image.blit(self.background)
        
        per = self.percentage / 100
        
        self.image.blit(
            pygame.transform.scale(self.face, (200 * per, 3)), 
            (1, 1)
        )
        
        screen.blit(self.image, self.rect.topleft)
        
        screen.blit(self.handle, (
            self.rect.x - 3 + (200 * per), 
            self.rect.y - 3
        ))
        
        screen.blit(self.font.render(str(round(per * 100)), True, '#CFCFCF'), (
            self.rect.right + 6,
            self.rect.y - 10
        ))
        
    