from settings import *

from components.component import Component


class NameComponent(Component):
    def __init__(self):
        super().__init__(
            "NameComponent",
            [520, 36],
            [12, 5],
            0
        )

        self.name: str = "Odin, Lord of the Eternal Hall [L50]"
        self.fontCap: pygame.font.Font = pygame.font.Font('assets/fonts/LibreBaskerville.ttf', 24)
        self.font: pygame.font.Font = pygame.font.Font('assets/fonts/LibreBaskerville.ttf', 20)

    def draw(self, screen: pygame.Surface, parentPos: list[int]) -> None:

        _words: list[str] = self.name.split()
        _text: str = ''
        _lines: list[str] = []

        
        for _w in _words:
            if self.fontCap.size(_text + _w)[0] >= 500:
                _lines.append(_text)
                _text = _w + ' '

                continue

            _text += _w + ' '

        _lines.append(_text)

        if len(_lines) >= 2:
            self.size = (520, 36 + (30 * len(_lines) - 1))
            self.image = pygame.Surface(self.size)
        self.image.fill('#F3E1C6')

        _y: int = 0
        for _l in _lines:
            self._renderSmallCase(_l, _y)
            _y += 30
        screen.blit(self.image, (parentPos[0] + self.x(), parentPos[1] + self.y()))



