from settings import *


class TextBox():
    def __init__(self, pos: list[int], size: list[int], exitCommand: callable, topleft: bool = False):
        self.backgroundSelected: dict[str, pygame.Surface] = _splitBackground('assets/backgrounds/UITextBoxBackground_selected.png')
        self.background: dict[str, pygame.Surface] = _splitBackground('assets/backgrounds/UITextBoxBackground.png')

        self.pos: list[int] = pos
        self.size: list[int] = size ## H = number of rows, w = number of pixels
        self.exitCommand: callable = exitCommand

        self.image: pygame.Surface = pygame.Surface((self.size[0], self.size[1] * 30))
        self.rect: pygame.Rect = pygame.Rect(self.pos, self.image.size)

        self.topleft: bool = topleft

        self.text: str = ''

        self.active: bool = False
        self.hovering: bool = False

        self.font: pygame.font.Font = pygame.font.Font('assets/fonts/noto-sans.regular.ttf', 18)

        self.fontBolded: pygame.font.Font = pygame.font.Font('assets/fonts/noto-sans.regular.ttf', 18)
        self.fontBolded.bold = True

        self.fontItalic: pygame.font.Font = pygame.font.Font('assets/fonts/noto-sans.regular.ttf', 18)
        self.fontItalic.italic = True

        self.bold: bool = False
        self.italic: bool = False
        self.red: bool = False
        self.blue: bool = False

        self.currentFormat: int = 0

    def exitField(self):
        self.active = False

        if self.exitCommand:
            self.exitCommand()

    def typing(self, event: pygame.Event):
        if self.active:
            if event.key == pygame.K_BACKSPACE:
                if len(self.text) > 0 and self.text[-1] == '}':
                    _words: list[str] = self.text.split()
                    _text: str = ''

                    for _i, _w in enumerate(_words):
                        if _i == len(_words) - 1:
                            continue
                        _text += _w + ' '

                    self.text = _text.strip()
                    return
                self.text = self.text[:-1]

            elif event.key == pygame.K_RETURN:
                self.exitField()
                return
            
            else:
                self.text += event.unicode

    def draw(self, screen: pygame.Surface, right: int):
        _background: dict[str, pygame.Surface] = self.background if not self.hovering else self.backgroundSelected
        if self.active:
            _background = self.backgroundSelected

        _size = self.image.size

        self.image.blit(_background['TopLeft'], (0, 0))
        self.image.blit(_background['TopRight'], (_size[0] - 10, 0))
        self.image.blit(_background['BottomLeft'], (0, _size[1] - 10))
        self.image.blit(_background['BottomRight'], (_size[0] - 10, _size[1] - 10))

        self.image.blit(pygame.transform.scale(_background['TopMiddle'], (_size[0] - 20, 10)), (10, 0))
        self.image.blit(pygame.transform.scale(_background['Left'], (10, _size[1] - 20)), (0, 10))
        self.image.blit(pygame.transform.scale(_background['Right'], (10, _size[1] - 20)), (_size[0] - 10, 10))
        self.image.blit(pygame.transform.scale(_background['BottomMiddle'], (_size[0] - 20, 10)), (10, _size[1] - 10))

        self.image.blit(pygame.transform.scale(_background['Middle'], (_size[0] - 20, _size[1] - 20)), (10, 10))

        _pos: list[int] = [_size[0] / 2 - self.font.size(self.text)[0] / 2, _size[1] / 2 - self.font.size(self.text)[1] / 2]
        if self.topleft:
            _pos = [8, 5]
        elif self.font.size(self.text)[0] > _size[0]:
            _pos = [_size[0] - self.font.size(self.text)[0] - 10, _size[1] / 2 - self.font.size(self.text)[1] / 2]
            
        if self.size[1] > 1:
            self.multiLineBlit()

        else:
            self.image.blit(self.font.render(self.text, True, '#000000'), (_pos[0] + 1, _pos[1] + 1))
            self.image.blit(self.font.render(self.text, True, '#ffffff'), _pos)
        
        self.rect: pygame.Rect = pygame.Rect((self.pos[0] + right, self.pos[1]), self.image.size)

        screen.blit(self.image, (self.pos[0] + right, self.pos[1]))

    def multiLineBlit(self):
        _size: list[int] = self.image.size
        _lines: list[str] = []
        _words: list[str] = self.text.split()
        _text: str = ''

        _backset: int = 0

        for _w in _words:
            if self.font.size(_text + _w)[0] - _backset >= _size[0] - 16:
                _lines.append(_text)
                _text = _w + ' '
                _backset = 0
                continue

            if _w == '{b}' or _w == '{/b}' or _w == '{i}' or _w == '{\i}' or _w == '{a}' or _w == '{/a}' or _w == '{t}' or _w == '{/t}':
                _backset += self.font.size(_w + ' ')[0]
                _text += _w + ' '
                continue

            _text += _w + ' '

        _lines.append(_text)

        _y: int = 5
        _x: int = 8
        for _l in _lines:
            _words: list[str] = _l.split()
            for _w in _words:
                if _w == '{b}':
                    self.bold = True
                    self.currentFormat = 1
                    continue
                if _w == '{/b}':
                    self.bold = False
                    self.currentFormat = 0
                    continue

                if _w == '{i}':
                    self.italic = True
                    self.currentFormat = 2
                    continue
                if _w == '{/i}':
                    self.italic = False
                    self.currentFormat = 0
                    continue

                if _w == '{a}':
                    self.red = True
                    self.currentFormat = 3
                    continue
                if _w == '{/a}':
                    self.red = False
                    self.currentFormat = 0
                    continue

                if _w == '{t}':
                    self.blue = True
                    continue
                if _w == '{/t}':
                    self.blue = False
                    continue

                if self.bold:
                    self.image.blit(self.fontBolded.render(_w, True, '#000000'), (_x, _y + 1))
                    self.image.blit(self.fontBolded.render(_w, True, '#ffffff'), (_x, _y))
                    _x += self.font.size(_w)[0] + 10
                elif self.italic:
                    self.image.blit(self.fontItalic.render(_w, True, '#000000'), (_x, _y + 1))
                    self.image.blit(self.fontItalic.render(_w, True, '#ffffff'), (_x, _y))
                    _x += self.font.size(_w)[0] + 3
                elif self.red:
                    self.image.blit(self.fontBolded.render(_w, True, '#000000'), (_x, _y + 1))
                    self.image.blit(self.fontBolded.render(_w, True, '#D34D35'), (_x, _y))
                    _x += self.font.size(_w)[0] + 10
                elif self.blue:
                    self.image.blit(self.fontBolded.render(_w, True, '#000000'), (_x, _y + 1))
                    self.image.blit(self.fontBolded.render(_w, True, '#2D638E'), (_x, _y))
                    _x += self.font.size(_w)[0] + 10
                else:
                    self.image.blit(self.font.render(_w, True, '#000000'), (_x, _y + 1))
                    self.image.blit(self.font.render(_w, True, '#ffffff'), (_x, _y))
                    _x += self.font.size(_w)[0] + 3

            _y += 20
            _x = 8

        self.bold = False
        self.italic = False
        self.red = False
        self.blue = False

    def hover(self):
        self.hovering = True

    def noHover(self):
        if not self.hovering:
            return
        self.hovering = False

    def onClick(self):
        self.active = True

def _splitBackground(file: str) -> dict[str, pygame.Surface]:
    _img = pygame.image.load(file).convert_alpha()

    _temp: dict[str, pygame.Surface] = {
        'TopLeft': None,
        'TopMiddle': None,
        'TopRight': None,
        'Left': None,
        'Middle': None,
        'Right': None,
        'BottomLeft': None,
        'BottomMiddle': None,
        'BottomRight': None
    }

    _temp['TopLeft'] = pygame.surface.Surface((10, 10))
    _temp['TopLeft'].fill('#ff00b6')
    _temp['TopLeft'].set_colorkey('#ff00b6')
    _temp['TopLeft'].blit(_img, (0, 0))
    _temp['TopMiddle'] = pygame.surface.Surface((10, 10))
    _temp['TopMiddle'].fill('#ff00b6')
    _temp['TopMiddle'].set_colorkey('#ff00b6')
    _temp['TopMiddle'].blit(_img, (-10, 0))
    _temp['TopRight'] = pygame.surface.Surface((10, 10))
    _temp['TopRight'].fill('#ff00b6')
    _temp['TopRight'].set_colorkey('#ff00b6')
    _temp['TopRight'].blit(_img, (-20, 0))

    _temp['Left'] = pygame.surface.Surface((10, 10))
    _temp['Left'].fill('#ff00b6')
    _temp['Left'].set_colorkey('#ff00b6')
    _temp['Left'].blit(_img, (0, -10))
    _temp['Middle'] = pygame.surface.Surface((10, 10))
    _temp['Middle'].fill('#ff00b6')
    _temp['Middle'].set_colorkey('#ff00b6')
    _temp['Middle'].blit(_img, (-10, -10))
    _temp['Right'] = pygame.surface.Surface((10, 10))
    _temp['Right'].fill('#ff00b6')
    _temp['Right'].set_colorkey('#ff00b6')
    _temp['Right'].blit(_img, (-20, -10))

    _temp['BottomLeft'] = pygame.surface.Surface((10, 10))
    _temp['BottomLeft'].fill('#ff00b6')
    _temp['BottomLeft'].set_colorkey('#ff00b6')
    _temp['BottomLeft'].blit(_img, (0, -20))
    _temp['BottomMiddle'] = pygame.surface.Surface((10, 10))
    _temp['BottomMiddle'].fill('#ff00b6')
    _temp['BottomMiddle'].set_colorkey('#ff00b6')
    _temp['BottomMiddle'].blit(_img, (-10, -20))
    _temp['BottomRight'] = pygame.surface.Surface((10, 10))
    _temp['BottomRight'].fill('#ff00b6')
    _temp['BottomRight'].set_colorkey('#ff00b6')
    _temp['BottomRight'].blit(_img, (-20, -20))

    return _temp