import pygame

from singletons import resourceHandler


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
    
    def _render_small_case(self, text: str, y: int, x: int = 0) -> None:
        characters: list[str] = list(text)

        _x: int = x
        for _c in characters:
            if _c.isspace():
                _x += 5
                
            elif _c == '[' or _c == ']':
                _render: pygame.Surface = self.font_cap.render(_c, True, '#954E40')
                self.text_face.blit(_render, (_x, 2 + y))
                _x += self.font_cap.size(_c)[0] + 2    
                
            elif _c.isupper() or _c.isnumeric():
                _render: pygame.Surface = self.font_cap.render(_c, True, '#954E40')
                self.text_face.blit(_render, (_x, 4 + y))
                _x += self.font_cap.size(_c)[0] + 2
                
            else:
                _render: pygame.Surface = self.font.render(_c.upper(), True, '#954E40')
                self.text_face.blit(_render, (_x, 8 + y))
                _x += self.font.size(_c)[0] + 2