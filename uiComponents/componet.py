import pygame

from singletons.eventBus import event_bus


class Component():
    def __init__(self, pos: tuple[int, int], size: tuple[int, int]) -> None:
        self.pos: tuple[int, int] = pos
        self.size: tuple[int, int] = size
        
        self.image: pygame.Surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.rect: pygame.Rect = self.image.get_rect(topleft=self.pos)
        
        self.hovering: bool = False
        
    def draw(self, screen: pygame.Surface, parent_pos: tuple[int, int]) -> None:
        self.rect.topleft = (self.pos[0] + parent_pos[0], self.pos[1] + parent_pos[1])
        self.image.fill((0, 0, 0, 0))
        
    def no_hover(self) -> None:
        if not self.hovering:
            return
        self.hovering = False

    def hover(self) -> None:
        if self.hovering:
            return
        
        event_bus.sign('play_se', 'hover')
        self.hovering = True
        
    def is_hover(self, mouse_pos: tuple[int, int]) -> bool:
        return self.rect.collidepoint(mouse_pos)
        
    def deregister(self) -> None:
        pass