from settings import *

from ui.background import Background


class Component():
    def __init__(self, name: str, size: list[int], pos: list[int], priority: int) -> None:
        self.id: str = name
        self.size: list[int] = size
        self.pos: list[int] = pos

        self.image: pygame.Surface = pygame.Surface(self.size)
        self.rect: pygame.Rect = pygame.Rect(pos, size)
        self.image.fill('#F3E1C6')

        self.priority: int = priority
        self.window: Background = None

        self.hovering: bool = False

    def draw(self, screen: pygame.Surface, parentPos: list[int], scroll: list[int]) -> None:
        self.rect: pygame.Rect = pygame.Rect(self.pos[0] + parentPos[0] + scroll[0], self.pos[1] + parentPos[1] + 40 + scroll[1], self.size[0], self.size[1])
        if self.hovering:
            self.image.fill('#E0D3BF')
            return
        self.image.fill('#F3E1C6')

    def width(self) -> int:
        return self.size[0]
    
    def height(self) -> int:
        return self.size[1]
    
    def x(self) -> int:
        return self.pos[0]
    
    def y(self) -> int:
        return self.pos[1]
    
    def hover(self):
        self.hovering = True

    def noHover(self):
        if not self.hovering:
            return
        self.hovering = False

    def onClick(self):
        print(f'Clicked on {self.id}')

    def _sizeSmallCase(self, text: str) -> int:
        _characters: list[str] = [c for c in text]

        _x: int = 0
        for _c in _characters:
            if _c.isspace():
                _x += 5
            elif _c == '[' or _c == ']':
                _render: pygame.Surface = self.fontCap.render(_c, True, '#954E40')
                _x += _render.get_width()
            elif _c.isupper() or _c.isnumeric():
                _render: pygame.Surface = self.fontCap.render(_c, True, '#954E40')
                _x += _render.get_width()
            else:
                _render: pygame.Surface = self.font.render(_c.upper(), True, '#954E40')
                _x += _render.get_width() - 1

        return _x

    def _renderSmallCase(self, text: str, y: int, x: int = 0) -> None:
        _characters: list[str] = [c for c in text]

        _x: int = x
        for _c in _characters:
            if _c.isspace():
                _x += 5
            elif _c == '[' or _c == ']':
                _render: pygame.Surface = self.fontCap.render(_c, True, '#954E40')
                self.image.blit(_render, (_x, 2 + y))
                _x += _render.get_width()
            elif _c.isupper() or _c.isnumeric():
                _render: pygame.Surface = self.fontCap.render(_c, True, '#954E40')
                self.image.blit(_render, (_x, 4 + y))
                _x += _render.get_width()
            else:
                _render: pygame.Surface = self.font.render(_c.upper(), True, '#954E40')
                self.image.blit(_render, (_x, 8 + y))
                _x += _render.get_width() - 1

    def _renderLargeNumber(self, text: str, x: int, y: int, font: pygame.font.Font, fontCap: pygame.font.Font, miedinger: pygame.font.Font) -> None:
        _characters: list[str] = [c for c in text]

        _x: int = 0
        for _c in _characters:
            if _c.isnumeric():
                _render: pygame.Surface = miedinger.render(_c, True, '#ffffff')
                self.image.blit(_render, (_x + x, 2 + y))
                _x += _render.get_width()
            elif _c.isupper():
                _render: pygame.Surface = fontCap.render(_c, True, '#ffffff')
                self.image.blit(_render, (_x + x, 0 + y))
                _x += _render.get_width()
            elif _c == '(' or _c == ')':
                _render: pygame.Surface = font.render(_c, True, '#ffffff')
                self.image.blit(_render, (_x + x, 2 + y))
                _x += _render.get_width()
            elif _c == '-':
                _render: pygame.Surface = font.render(_c, True, '#ffffff')
                self.image.blit(_render, (_x + x, 0 + y))
                _x += _render.get_width()
            else:
                _render: pygame.Surface = font.render(_c, True, '#ffffff')
                self.image.blit(_render, (_x + x, 2 + y))
                _x += _render.get_width()
