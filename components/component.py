from settings import *


class Component():
    def __init__(self, name: str, size: list[int], pos: list[int], priority: int) -> None:
        self.id: str = name
        self.size: list[int] = size
        self.pos: list[int] = pos

        self.image: pygame.Surface = pygame.Surface(self.size)
        self.image.fill('#F3E1C6')

        self.priority: int = priority

    def draw(self, screen: pygame.Surface, parentPos: list[int]) -> None:
        pass

    def width(self) -> int:
        return self.size[0]
    
    def height(self) -> int:
        return self.size[1]
    
    def x(self) -> int:
        return self.pos[0]
    
    def y(self) -> int:
        return self.pos[1]
    
    def changeOrder(self, order: int) -> None:
        self.order = order

    def _renderSmallCase(self, text: str, y: int) -> None:
        _characters: list[str] = [c for c in text]

        _x: int = 0
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