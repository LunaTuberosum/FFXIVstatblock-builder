import pygame

from singletons import resourceHandler

from singletons.keyBus import key_bus


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
        
        self.text_face: pygame.Surface = pygame.Surface(self.size, pygame.SRCALPHA)
        
        self.font_cap: pygame.Font = resourceHandler.load_font('.\\assets\\fonts\\LibreBaskerville.ttf', 24)
        self.font: pygame.Font = resourceHandler.load_font('.\\assets\\fonts\\LibreBaskerville.ttf', 20)
        
        self.hovering: bool = False
        
        key_bus.register('mouse_left_down', self.on_click)
        
    def deregister(self) -> None:
        key_bus.deregister('mouse_left_down', self.on_click)
        
    def draw(self, screen: pygame.Surface) -> None:
        self.rect.topleft = (self.pos[0] + self.card.rect.x, self.pos[1] + self.card.rect.y)
        
        self.image.fill((0, 0, 0, 0))
        if self.hovering:
            self.image.fill('#E0D3BF')
        
    def on_click(self) -> None:
        pass
        
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