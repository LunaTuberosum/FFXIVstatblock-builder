from settings import *

from components.component import Component
from ui.trait import TraitUI


class TraitComponent(Component):
    def __init__(self, name: str, desc: str):
        super().__init__(
            "TraitComponent",
            [518, 50], # Might need to change
            [12, 12],
            2
        )

        self.fontTitle: pygame.font.Font = pygame.font.SysFont('Noto Sans', 19, True)

        self.font: pygame.font.Font = pygame.font.Font('assets/fonts/noto-sans.regular.ttf', 15)

        self.fontBolded: pygame.font.Font = pygame.font.Font('assets/fonts/noto-sans.regular.ttf', 15)
        self.fontBolded.bold = True

        self.fontItalic: pygame.font.Font = pygame.font.Font('assets/fonts/noto-sans.regular.ttf', 15)
        self.fontItalic.italic = True

        self.last: bool = False
        self.divider: pygame.Surface = pygame.image.load('assets/backgrounds/StatCardDivider.png').convert_alpha()

        self.name: str = name
        self.desc: str = desc 

        self._findSize()

    def _findSize(self):
        _words: list[str] = self.desc.split()
        _text: str = ''
        self.lines: list[str] = []

        _backset: int = 0

        for _w in _words:
            if self.font.size(_text + _w)[0] - _backset >= self.width():
                self.lines.append(_text)
                _text = _w + ' '
                _backset = 0
                continue

            if _w == '{b}' or _w == '{/b}' or _w == '{i}' or _w == '{\i}' or _w == '{a}' or _w == '{/a}' or _w == '{t}' or _w == '{/t}':
                _backset += self.font.size(_w)[0] + 4 
                _text += _w + ' '
                continue

            _text += _w + ' '

        self.lines.append(_text)

        self.size = (518, 50 + (14 * len(self.lines) - 1))
        self.image = pygame.Surface(self.size)

    def draw(self, screen: pygame.Surface, parentPos: list[int], scroll: list[int]) -> None:
        self._findSize()
        self.parentPos: list[int] = parentPos

        _bold: bool = False
        _italic: bool = False
        _red: bool = False
        _blue: bool = False

        super().draw(screen, parentPos, scroll)

        self.image.blit(self.fontTitle.render(self.name, True, '#000000'), (1,0))

        _y: int = 26
        _x: int = 1
        for _l in self.lines:
            _words: list[str] = _l.split()
            for _w in _words:
                if _w == '{b}':
                    _bold = True
                    continue
                if _w == '{/b}':
                    _bold = False
                    continue

                if _w == '{i}':
                    _italic = True
                    continue
                if _w == '{/i}':
                    _italic = False
                    continue

                if _w == '{a}':
                    _red = True
                    continue
                if _w == '{/a}':
                    _red = False
                    continue

                if _w == '{t}':
                    _blue = True
                    continue
                if _w == '{/t}':
                    _blue = False
                    continue

                if _bold:
                    self.image.blit(self.fontBolded.render(_w, True, '#000000'), (_x, _y))
                    _x += self.font.size(_w)[0] + 10
                elif _italic:
                    self.image.blit(self.fontItalic.render(_w, True, '#000000'), (_x, _y))
                    _x += self.font.size(_w)[0] + 3
                elif _red:
                    self.image.blit(self.fontBolded.render(_w, True, '#D34D35'), (_x, _y))
                    _x += self.font.size(_w)[0] + 10
                elif _blue:
                    self.image.blit(self.fontBolded.render(_w, True, '#2D638E'), (_x, _y))
                    _x += self.font.size(_w)[0] + 10
                else:
                    self.image.blit(self.font.render(_w, True, '#000000'), (_x, _y))
                    _x += self.font.size(_w)[0] + 3

            _y += 16
            _x = 1

        _bold = False
        _italic = False
        _red = False
        _blue = False

        if not self.last:
            self.image.blit(self.divider, (0, self.height() - 5))

        screen.blit(self.image, (20 + self.x(), parentPos[1] + self.y()))

    def onClick(self):
        if self.window:
            self.window = None
            return
        self.window = TraitUI([-15, self.parentPos[1] + self.y() + 30], self)



