import pygame

from singletons.keyBus import key_bus


LEFT: int = 1
MIDDLE: int = 2
RIGHT: int = 3

class MouseHandler():
    def __init__(self) -> None:
        self.mouse_pos: tuple[int, int] = ()
        self.mouse_rel: tuple[int, int] = ()
        self.scroll_wheel: tuple[int, int] = ()
        
    def handle_mouse(self, events: list[pygame.Event]) -> None:
        self.mouse_pos = pygame.mouse.get_pos()
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == LEFT:
                    key_bus.sign('mouse_left_down')
                    
                if event.button == MIDDLE:
                    key_bus.sign('mouse_middle_down')
                    
                if event.button == RIGHT:
                    key_bus.sign('mouse_right_down')
                    
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == LEFT:
                    key_bus.sign('mouse_left_up')
                    
                if event.button == MIDDLE:
                    key_bus.sign('mouse_middle_up')
                    
                if event.button == RIGHT:
                    key_bus.sign('mouse_right_up')
                    
            if event.type == pygame.MOUSEMOTION:
                self.mouse_rel = event.rel
                
            if event.type == pygame.MOUSEWHEEL:
                self.scroll_wheel = (event.x, event.y)