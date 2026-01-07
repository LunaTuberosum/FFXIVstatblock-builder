import pygame

from singletons import resourceHandler

from singletons.keyBus import key_bus

from src.timer import Timer


SMALL_CASE_BRACKET: int = 2
SMALL_CASE_UPPER: int = 4
SMALL_CASE_LOWER: int = 8

class CardComponent():
    def __init__(self, name: str, size: tuple[int, int], pos: tuple[int, int], card: object) -> None:
        self.name: str = name
        self.size: tuple[int, int] =  size
        self.pos: tuple[int, int] = pos 
        
        from editor.statcard import StatCard
        self.card: StatCard = card
        
        self.image: pygame.Surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.rect: pygame.Rect = self.image.get_rect(topleft=self.pos)
        
        self.offset: tuple[int, int] = (0, 0)
                
        self.text_face: pygame.Surface = pygame.Surface(self.size, pygame.SRCALPHA)
        
        self.font_cap: pygame.Font = resourceHandler.load_font('.\\assets\\fonts\\LibreBaskerville.ttf', 24)
        self.font: pygame.Font = resourceHandler.load_font('.\\assets\\fonts\\LibreBaskerville.ttf', 20)
        
        self.hovering: bool = False
        
        self.click_timer: Timer = Timer(300)
        self.drag: bool = False
        self.can_drag: bool = True
        self.drag_pos = tuple[int, int]
        
        self.is_last: bool = False
        self.divider: pygame.Surface = resourceHandler.load_image('.\\assets\\backgrounds\\StatCardDivider.png')
        
        key_bus.register('mouse_left_down', self.on_click)
        key_bus.register('mouse_left_up', self.on_release)
        
        key_bus.register('space_down', self.space_down)
        key_bus.register('space_up', self.space_up)
        
    def deregister(self) -> None:
        key_bus.deregister('mouse_left_down', self.on_click)
        key_bus.deregister('mouse_left_up', self.on_release)
        
        key_bus.deregister('space_down', self.space_down)
        key_bus.deregister('space_up', self.space_up)
        
    def space_down(self) -> None:
        self.can_drag = False
        self.drag = False
        
    def space_up(self) -> None:
        self.can_drag = True
        
    def update(self, offset: tuple[int, int]) -> None:
        self.rect.topleft = (
            self.pos[0] + self.card.rect.x + offset[0], 
            self.pos[1] + self.card.rect.y + offset[1]
        )
        
        self.offset = offset
        
    def draw(self, screen: pygame.Surface) -> None:
        self.image.fill((0, 0, 0, 0))
        if self.hovering:
            self.image.fill('#E4D2B7')    
                        
    def refresh(self) -> None:
        pass
               
    def on_click(self) -> bool:
        if self.click_timer.time_left() < 0:
            self.click_timer.start()
            
            if not self.can_drag:
                return False
            
            if not self.drag:
                mouse: tuple[int, int] = pygame.mouse.get_pos()
                self.drag_pos = (mouse[0] - self.rect.x, mouse[1] - self.rect.y)
                
            self.drag = True
            return False
        
        return True
    
    def on_release(self) -> bool:
        if not self.hovering or not self.drag:
            return False
        
        self.drag = False
        return True

    def no_hover(self) -> None:
        if not self.hovering:
            return
        self.hovering = False

    def hover(self) -> None:
        self.hovering = True
        
    def save(self) -> dict:
        return {}
    
    def load(self, data: dict[str]) -> None:
        pass
    
    def __draw_text_face(self) -> None:
        pass
    
    def _size_small_case(self, text: str) -> int:
        characters: list[str] = list(text)
        
        x: int = 0
        for char in characters:
            if char.isspace():
                x += self.font.size(' ')[0]
                
            elif char == '[' or char == ']':
                render: pygame.Surface = self.font_cap.render(char, True, '#954E40')
                x += render.get_width()
                
            elif char.isupper() or char.isnumeric():
                render: pygame.Surface = self.font_cap.render(char, True, '#954E40')
                x += render.get_width()
                
            else:
                render: pygame.Surface = self.font.render(char.upper(), True, '#954E40')
                x += render.get_width()
                
        return x
    
    def _render_small_case(self, text: str, pos: tuple[int, int]) -> None:
        characters: list[str] = list(text)
        
        x: int = pos[0]
        for char in characters:
            if char.isspace():
                x += self.font.size(' ')[0]
                
            elif char == '[' or char == ']':
                render: pygame.Surface = self.font_cap.render(char, True, '#954E40')
                self.text_face.blit(render, (x, pos[1] + SMALL_CASE_BRACKET))
                x += render.get_width()
                
            elif char.isupper() or char.isnumeric():
                render: pygame.Surface = self.font_cap.render(char, True, '#954E40')
                self.text_face.blit(render, (x, pos[1] + SMALL_CASE_UPPER))
                x += render.get_width()
                
            else:
                render: pygame.Surface = self.font.render(char.upper(), True, '#954E40')
                self.text_face.blit(render, (x, pos[1] + SMALL_CASE_LOWER))
                x += render.get_width()
                