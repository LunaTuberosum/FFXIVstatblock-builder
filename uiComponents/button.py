from typing import Callable
import pygame

from singletons import resourceHandler

from singletons.keyBus import key_bus

from uiComponents.componet import Component


TEXT_ALIGN_LEFT: int = 20
TEXT_ALIGN_RIGHT: int = 8

class Button(Component):
    def __init__(self, pos: tuple[int, int], size: tuple[int, int], image: str, image_hover: str, command: Callable[[None], None], text: str = ''):
        super().__init__(
            pos,
            size
        )
        
        self.face: pygame.Surface = pygame.Surface(self.size, pygame.SRCALPHA)
        if image:
            self.face = pygame.transform.scale(resourceHandler.load_image(image), self.size)
            
        self.face_hover: pygame.Surface = pygame.transform.scale(resourceHandler.load_image(image_hover), self.size)
                
        self.command: Callable[[None], None] = command
        self.text: str = text
        
        self.font: pygame.Font = resourceHandler.load_font('.\\assets\\fonts\\noto-sans.regular.ttf', 18)
        self.back_text: pygame.Surface = self.font.render(self.text, True, '#000000')
        self.face_text: pygame.Surface = self.font.render(self.text, True, '#ffffff')
        
        self.text_size: tuple[int, int] = self.face_text.size
        self.text_pos: tuple[int, int] = (
            (self.size[0] / 2) - (self.text_size[0] / 2),
            (self.size[1] / 2) - (self.text_size[1] / 2)
        )
        
        key_bus.register('mouse_left_down', self.on_click)
        
    def change_text_color(self, color: str) -> None:
        self.face_text = self.font.render(self.text, True, color)
        
    def left_algin_text(self) -> None:
        self.text_pos = (
            TEXT_ALIGN_LEFT,
            -2
        )
        
    def right_algin_text(self) -> None:
        self.text_pos = (
            self.size[0] - TEXT_ALIGN_RIGHT,
            (self.size[1] / 2) - (self.text_size[1] / 2)
        )
        
    def draw(self, screen: pygame.Surface, parent_pos: tuple[int, int]) -> None:
        super().draw(screen, parent_pos)
        
        if self.hovering:
            self.image.blit(self.face_hover, (0, 0))
        else:
            self.image.blit(self.face, (0, 0))
            
        self.image.blit(self.back_text, (self.text_pos[0], self.text_pos[1] + 1))
        self.image.blit(self.face_text, self.text_pos)
        
        screen.blit(self.image, self.rect.topleft)
        
    def deregister(self) -> None:
        super().deregister()
        
        key_bus.deregister('mouse_left_down', self.on_click)
        
    def on_click(self) -> None:
        if not self.hovering:
            return
        
        self.command()