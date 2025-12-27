from typing import Callable
import pygame

from singletons import resourceHandler

from singletons.keyBus import key_bus

from uiComponents.componet import Component


class Button(Component):
    def __init__(self, pos: tuple[int, int], size: tuple[int, int], image: str, image_hover: str, command: Callable[[None], None], text: str = ''):
        super().__init__(
            pos,
            size
        )
        
        self.face: pygame.Surface = resourceHandler.load_image(image)
        self.face_hover: pygame.Surface = resourceHandler.load_image(image_hover)
                
        self.command: Callable[[None], None] = command
        self.text: str = text
        
        self.face_text: pygame.Surface = resourceHandler.load_font('.\\assets\\fonts\\noto-sans.regular.ttf', 18).render(self.text, True, '#ffffff')
        
        text_size: tuple[int, int] = self.face_text.size
        self.text_pos: tuple[int, int] = [
            (self.size[0] / 2) - (text_size[0] / 2),
            (self.size[1] / 2) - (text_size[1] / 2)
        ]
        
        key_bus.register('mouse_left_down', self.on_click)
        
    def draw(self, screen: pygame.Surface, parent_pos: tuple[int, int]) -> None:
        super().draw(screen, parent_pos)
        
        if self.hovering:
            self.image.blit(self.face_hover, (0, 0))
        else:
            self.image.blit(self.face, (0, 0))
            
        self.image.blit(self.face_text, self.text_pos)
        
        screen.blit(self.image, self.rect.topleft)
        
    def deregister(self) -> None:
        super().deregister()
        
        key_bus.deregister('mouse_left_down', self.on_click)
        
    def on_click(self) -> None:
        if not self.hovering:
            return
        
        self.command()