from settings import *

from components.component import Component

from ui.name import NameUI


class NameComponent(Component):
    def __init__(self, parent: object):
        super().__init__(
            "NameComponent",
            [512, 36],
            [12, 5],
            0,
            parent
        )

        self.name: str = 'Character Name'
        self.level: str = '00'
        self.levelPositon: bool = False # False = end, true = top left
        self.fontCap: pygame.font.Font = pygame.font.Font('assets/fonts/LibreBaskerville.ttf', 24)
        self.font: pygame.font.Font = pygame.font.Font('assets/fonts/LibreBaskerville.ttf', 20)

    def draw(self, screen: pygame.Surface, parentPos: list[int]) -> None:

        _words: list[str] = self.name.split()
        if not self.levelPositon:
            _words.append(f'[L{self.level}]')
        _text: str = ''
        _lines: list[str] = []

        _limit: int = 512 if not self.levelPositon else 430
        
        for _w in _words:
            if self._sizeSmallCase(_text + _w) > _limit:
                _lines.append(_text)
                _text = _w + ' '

                continue

            _text += _w + ' '

        _lines.append(_text)

        self.size = (512, 36 + (30 * (len(_lines) - 1)))
        self.image = pygame.Surface(self.size)
        super().draw(screen, parentPos)

        _y: int = 0
        for _l in _lines:
            self._renderSmallCase(_l, _y)
            _y += 30

        if self.levelPositon:
            self._renderSmallCase(f'[L{self.level}]', 0, 430)
        screen.blit(self.image, (20 + self.x(), parentPos[1] + self.y()))

    def onClick(self):
        if self.window:
            self.window = None
            return
        self.window = NameUI([-15, 55], self)

    def save(self) -> dict:
        return {
            'name': self.name,
            'level': self.level,
            'levelPosition': self.levelPositon
        }

