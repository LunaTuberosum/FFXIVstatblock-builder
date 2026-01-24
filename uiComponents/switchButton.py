from typing import Callable
import pygame

from singletons import resourceHandler

from singletons.eventBus import event_bus
from singletons.keyBus import key_bus

from uiComponents.componet import Component


class SwitchButton(Component):
    def __init__(
            self, 
            pos: tuple[int, int], 
            face: pygame.Surface, 
            face_hover: pygame.Surface, 
            face_switch: pygame.Surface, 
            face_switch_hover: pygame.Surface, 
            command: Callable [[None], None]
        ):
        super().__init__(
            pos,
            (18, 18)
        )
        
        self.face: pygame.Surface = resourceHandler.load_image(face)
        self.face_hover: pygame.Surface = resourceHandler.load_image(face_hover)
        self.face_switch: pygame.Surface = resourceHandler.load_image(face_switch)
        self.face_switch_hover: pygame.Surface = resourceHandler.load_image(face_switch_hover)
        
        self.command: Callable [[None], None] = command
        
        self.active: bool = False
        
        key_bus.register('mouse_left_down', self.on_click)
        
    def deregister(self) -> None:
        key_bus.deregister('mouse_left_down', self.on_click)
        
        super().deregister()
        
    def on_click(self) -> None:
        if not self.hovering:
            return
        
        event_bus.sign('play_se', 'confirm')
        
        self.active = not self.active
        
        self.command()
        
    def draw(self, screen: pygame.Surface, parent_pos: tuple[int, int]) -> None:
        super().draw(screen, parent_pos)
        
        if self.active:
            if self.hovering: self.image.blit(self.face_switch_hover)
            else: self.image.blit(self.face_switch)
            
        else:
            if self.hovering: self.image.blit(self.face_hover)
            else: self.image.blit(self.face)
            
        screen.blit(self.image, self.rect.topleft)