from settings import *

from components.component import Component
from components.marker import MarkerComponent


class AbilityComponent(Component):
    def __init__(self, name: str, types: str, effects: dict[str, str], marker: list[list[int]] = None):
        super().__init__(
            "AbilityComponent",
            [518, 40],
            [12, 12],
            3
        )

        self.name: str = name
        self.types: str = types
        self.effects: dict[str, str] = effects

        self.marker: MarkerComponent = None
        if marker:
            self.marker = MarkerComponent(7, 7, marker, self.width())

        self.last: bool = False

        self.fontTitle: pygame.font.Font = pygame.font.SysFont('Noto Sans', 19, True)
        self.font: pygame.font.Font = pygame.font.Font('assets/fonts/noto-sans.regular.ttf', 15)

        self.fontBolded: pygame.font.Font = pygame.font.Font('assets/fonts/noto-sans.regular.ttf', 15)
        self.fontBolded.bold = True

        self.fontItalic: pygame.font.Font = pygame.font.Font('assets/fonts/noto-sans.regular.ttf', 15)
        self.fontItalic.italic = True

        self.divider: pygame.Surface = pygame.image.load('assets/backgrounds/StatCardDivider.png').convert_alpha()

        self._findHeight()

    def _findHeight(self):
        self.lines: list[str] = []

        _size: int = 0

        _right: int = self.width()
        if self.marker:
            _right -= self.marker.width() + 10

        for _name, _effect in self.effects.items():
            _text = '{n} ' + _name + ' {/n} '
            _size = self.fontBolded.size(_name)[0]

            _words: list[str] = _effect.split()

            for _w in _words:
                if _size + self.font.size(_w)[0] >= _right:
                    self.lines.append(_text)
                    _text = _w + ' '
                    _size = self.font.size(_w + ' ')[0]
                    continue

                if _w == '{b}' or _w == '{/b}' or _w == '{i}' or _w == '{\i}' or _w == '{a}' or _w == '{/a}' or _w == '{t}' or _w == '{/t}':
                    _text += _w + ' '
                    continue

                _text += _w + ' '
                _size += self.font.size(_w + ' ')[0]

            self.lines.append(_text)

        self.size = ((
            518,
            40 + (18 * len(self.lines))
        ))
        self.image = pygame.Surface(self.size)

    def draw(self, screen: pygame.Surface, parentPos: list[int]) -> None:
        _text: str = ''

        _bold: bool = False
        _italic: bool = False
        _red: bool = False
        _blue: bool = False
        _dark: bool = False

        super().draw(screen, parentPos)

        self.image.blit(self.fontTitle.render(self.name, True, '#000000'), (1,0))
        self.image.blit(self.fontItalic.render(self.types, True, '#000000'), (self.width() - self.fontItalic.size(self.types)[0], 4))

        _y: int = 26
        _x: int = 1
        for _l in self.lines:
            _words: list[str] = _l.split()
            for _w in _words:
                if _w == '{n}':
                    _name = True
                    continue
                if _w == '{/n}':
                    _name = False
                    continue

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

                if _name:
                    self.image.blit(self.fontBolded.render(_w, True, '#995745'), (_x, _y))
                    _x += self.font.size(_w)[0] + 10
                elif _bold:
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

            _y += 18
            _x = 1

        _name = False
        _bold = False
        _italic = False
        _red = False
        _blue = False

        if self.marker:
            self.marker.draw(self.image, self.pos)

        if not self.last:
            self.image.blit(self.divider, (0, self.height() - 5))
        screen.blit(self.image, (20 + self.x(), parentPos[1] + self.y()))


