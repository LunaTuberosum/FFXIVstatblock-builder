from settings import *

from components.component import Component
from components.marker import MarkerComponent
from ui.ability import AbilityUI


class AbilityComponent(Component):
    def __init__(self, name: str, types: str, effects: dict[str, str], parent: object, marker: list[list[int]] = None):
        super().__init__(
            "AbilityComponent",
            [518, 40],
            [12, 12],
            3,
            parent
        )

        self.name: str = name
        self.types: str = types
        self.effects: dict[str, str] = effects

        self.marker: MarkerComponent = None
        if marker:
            self.marker = MarkerComponent(len(marker[0]), len(marker), marker, self.width())

        self.last: bool = False
        self.invk: bool = False

        self.invkImage: pygame.Surface = pygame.image.load('.//assets//icons//INVK.png').convert_alpha()

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
                if _w == '{lb}':
                    _text += _w
                    self.lines.append(_text)
                    _text = ''
                    _size = 0
                    continue

                if _size + self.font.size(_w)[0] >= _right:
                    self.lines.append(_text)
                    _text = _w + ' '
                    _size = self.font.size(_w + ' ')[0]
                    continue

                if _w == '{b}' or _w == '{/b}' or _w == '{i}' or _w == '{\i}' or _w == '{a}' or _w == '{/a}' or _w == '{t}' or _w == '{/t}' or _w == '{lb}':
                    _text += _w + ' '
                    continue

                _text += _w + ' '
                _size += self.font.size(_w + ' ')[0]

            self.lines.append(_text)

        self.size = ((
            518,
            40 + (10 + self.marker.height() if self.marker and self.marker.height() > (18 * len(self.lines)) else (18 * len(self.lines)))
        ))
        self.image = pygame.Surface(self.size)

    def draw(self, screen: pygame.Surface, parentPos: list[int]) -> None:
        self.parentPos: list[int] = parentPos
        _text: str = ''

        _bold: bool = False
        _italic: bool = False
        _red: bool = False
        _blue: bool = False
        _dark: bool = False

        self._findHeight()
        super().draw(screen, parentPos)

        _nameWidth: int = self.fontTitle.size(self.name)[0]
        _typesWidth: int = self.fontItalic.size(self.types)[0]
        _typesTooLong: bool = False

        if self.invk:
            self.image.blit(self.invkImage, (0, 0))
            self.image.blit(self.fontTitle.render(self.name, True, '#000000'), (78,0))
            if _nameWidth + self.invkImage.get_width() + 12 + _typesWidth >= self.size[0]:
                _typesTooLong = True

        else:
            self.image.blit(self.fontTitle.render(self.name, True, '#000000'), (1,0))
            if _nameWidth + 11 + _typesWidth >= self.size[0]:
                _typesTooLong = True

        self.image.blit(self.fontItalic.render(self.types, True, '#000000'), (self.width() - self.fontItalic.size(self.types)[0], 26 if _typesTooLong else 4))


        _y: int = 26 + (22 if _typesTooLong else 0)
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

                if _w == '{lb}':
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
            self.marker.draw(self.image, [self.pos[0], self.pos[1] + (20 if _typesTooLong else 0)])

        if not self.last:
            self.image.blit(self.divider, (0, self.height() - 5))
        screen.blit(self.image, (20 + self.x() + parentPos[0], parentPos[1] + self.y()))

    def onClick(self):
        if self.window:
            self.window = None
            return
        self.window = AbilityUI([-15, self.parentPos[1] + self.y() + 30], self)

    def save(self) -> dict:
        return {
            'name': self.name,
            'invk': self.invk,
            'types': self.types,
            'effects': self.effects,
            'marker': self.marker.save() if self.marker else None
        }