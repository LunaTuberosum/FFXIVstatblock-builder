from typing import Callable
import pygame

from editor.cardComponents.abilityComponent import EffectData

from singletons import resourceHandler
from singletons.keyBus import key_bus

from src.timer import Timer


class ListItem():
    def __init__(self, size: tuple[int, int], effect_name: str, effect_data: EffectData, command: Callable[['ListItem'], None]) -> None:
        self.size: tuple[int, int] = size
        self.effect_name: str = effect_name
        self.effect_data: EffectData = effect_data
        
        self.command: Callable[['ListItem'], None] = command
        
        self.rect: pygame.Rect = pygame.Rect((0, 0), self.size)
        
        self.hovering: bool = False
        
        self.current: bool = False
        self.click_timer: Timer = Timer(300)
        
        self.font_bolded: pygame.Font = resourceHandler.load_font('.\\assets\\fonts\\noto-sans.regular.ttf', 15)
        self.font_bolded.bold = True
        
        self.active: bool = True
        
        key_bus.register('mouse_left_down', self.on_click)
        
    def deregister(self) -> None:
        key_bus.deregister('mouse_left_down', self.on_click)
        
    def draw(self, screen: pygame.Surface, pos: tuple[int, int]) -> None:
        self.rect = pygame.Rect(pos, self.size)
        
        if self.hovering:
            pygame.draw.rect(screen, '#cccccc', self.rect)
        elif self.current:
            pygame.draw.rect(screen, "#d6a7a7", self.rect)
        else:
            pygame.draw.rect(screen, '#ffffff', self.rect)
            
        screen.blit(self.font_bolded.render(self.effect_name, True, '#995745'), (self.rect.x + 5, self.rect.y + 5))
        
    def on_click(self) -> None:
        if not self.hovering:
            return
        
        if self.click_timer.time_left() > 0:
            self.command(self)
            return
        
        self.click_timer.start()
        
    def no_hover(self) -> None:
        if not self.hovering:
            return
        
        self.hovering = False
        
    def hover(self) -> None:
        self.hovering = True
        
    def is_hover(self, mouse_pos: tuple[int, int]) -> bool:
        return self.rect.collidepoint(mouse_pos)