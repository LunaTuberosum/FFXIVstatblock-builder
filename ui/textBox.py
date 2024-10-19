from settings import *


class TextBox():
    def __init__(self, pos: list[int], size: list[int], maxChars: int, exitCommand: callable):
        self.backgroundSelected: dict[str, pygame.Surface] = _splitBackground('assets/backgrounds/UITextBoxBackground_selected.png')
        self.background: dict[str, pygame.Surface] = _splitBackground('assets/backgrounds/UITextBoxBackground.png')

        self.pos: list[int] = pos
        self.size: list[int] = size ## H = number of rows, w = number of pixels
        self.maxChars: int = maxChars
        self.exitCommand: callable = exitCommand

        self.image: pygame.Surface = pygame.Surface((self.size[0], self.size[1] * 30))
        self.rect: pygame.Rect = pygame.Rect(self.pos, self.image.size)

        self.text: str = ''

        self.active: bool = False
        self.hovering: bool = False

        self.font: pygame.font.Font = pygame.font.Font('assets/fonts/noto-sans.regular.ttf', 18)

    def exitField(self):
        self.active = False

        if self.exitCommand:
            self.exitCommand()

    def typing(self, event: pygame.Event):
        if self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]

            elif event.key == pygame.K_RETURN:
                self.exitField()
                return
            
            else:
                if self.maxChars == 0 or len(self.text) <= self.maxChars:
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
        if self.font.size(self.text)[0] > _size[0]:
            _pos = [_size[0] - self.font.size(self.text)[0] - 10, _size[1] / 2 - self.font.size(self.text)[1] / 2]
        self.image.blit(self.font.render(self.text, True, '#000000'), (_pos[0] + 1, _pos[1] + 1))
        self.image.blit(self.font.render(self.text, True, '#ffffff'), _pos)
        
        self.rect: pygame.Rect = pygame.Rect((self.pos[0] + right, self.pos[1]), self.image.size)

        screen.blit(self.image, (self.pos[0] + right, self.pos[1]))

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