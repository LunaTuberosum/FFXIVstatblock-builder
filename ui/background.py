from settings import *


class Background():
    def __init__(self, name: str, title: str, size: list[int], pos: list[int]):
        self.uiBackground: dict[str, pygame.Surface] = _splitBackground()

        self.id: str = name
        self.title: str = title
        self.size: list[int] = size
        self.pos: list[int] = pos

        self.image: pygame.Surface = pygame.Surface(self.size)
        self.rect: pygame.Rect = pygame.Rect(self.pos, self.size)

        self.components: list[object] = []

        self.font: pygame.font.Font = pygame.font.Font('assets/fonts/noto-sans.regular.ttf', 18)

        self.fontTitle: pygame.font.Font = pygame.font.Font('assets/fonts/Deutschlander.otf', 25)
        self.seperator: pygame.Surface = pygame.image.load('assets/backgrounds/UISeperator.png').convert_alpha()

    def draw(self, screen: pygame.Surface, right: int):
            self.image.fill('#ff00b6')
            self.image.set_colorkey('#ff00b6')
            self.rect = pygame.Rect(self.pos[0] + right, self.pos[1], self.size[0], self.size[1])

            self.image.blit(self.uiBackground['TopLeft'], (0, 0))
            self.image.blit(self.uiBackground['TopRight'], (self.size[0] - 50, 0))
            self.image.blit(self.uiBackground['BottomLeft'], (0, self.size[1] - 50))
            self.image.blit(self.uiBackground['BottomRight'], (self.size[0] - 50, self.size[1] - 50))

            self.image.blit(pygame.transform.scale(self.uiBackground['TopMiddle'], (self.size[0] - 100, 50)), (50, 0))
            self.image.blit(pygame.transform.scale(self.uiBackground['Left'], (50, self.size[1] - 100)), (0, 50))
            self.image.blit(pygame.transform.scale(self.uiBackground['Right'], (50, self.size[1] - 100)), (self.size[0] - 50, 50))
            self.image.blit(pygame.transform.scale(self.uiBackground['BottomMiddle'], (self.size[0] - 100, 50)), (50, self.size[1] - 50))

            self.image.blit(pygame.transform.scale(self.uiBackground['Middle'], (self.size[0] - 100, self.size[1] - 100)), (50, 50))

            self.image.blit(pygame.transform.scale(self.seperator, (self.size[0] - 50, 3)), (25, 45))

            self.image.blit(self.fontTitle.render(f'{self.title} Configuration', True, '#000000'), (25, 21))
            self.image.blit(self.fontTitle.render(f'{self.title} Configuration', True, '#CCCCCC'), (25, 20))


def _splitBackground() -> dict[str, pygame.Surface]:
    _img = pygame.image.load('assets/backgrounds/UIBackground.png').convert_alpha()

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

    _temp['TopLeft'] = pygame.surface.Surface((50, 50))
    _temp['TopLeft'].fill('#ff00b6')
    _temp['TopLeft'].set_colorkey('#ff00b6')
    _temp['TopLeft'].blit(_img, (0, 0))
    _temp['TopMiddle'] = pygame.surface.Surface((50, 50))
    _temp['TopMiddle'].fill('#ff00b6')
    _temp['TopMiddle'].set_colorkey('#ff00b6')
    _temp['TopMiddle'].blit(_img, (-50, 0))
    _temp['TopRight'] = pygame.surface.Surface((50, 50))
    _temp['TopRight'].fill('#ff00b6')
    _temp['TopRight'].set_colorkey('#ff00b6')
    _temp['TopRight'].blit(_img, (-100, 0))

    _temp['Left'] = pygame.surface.Surface((50, 50))
    _temp['Left'].fill('#ff00b6')
    _temp['Left'].set_colorkey('#ff00b6')
    _temp['Left'].blit(_img, (0, -50))
    _temp['Middle'] = pygame.surface.Surface((50, 50))
    _temp['Middle'].fill('#ff00b6')
    _temp['Middle'].set_colorkey('#ff00b6')
    _temp['Middle'].blit(_img, (-50, -50))
    _temp['Right'] = pygame.surface.Surface((50, 50))
    _temp['Right'].fill('#ff00b6')
    _temp['Right'].set_colorkey('#ff00b6')
    _temp['Right'].blit(_img, (-100, -50))

    _temp['BottomLeft'] = pygame.surface.Surface((50, 50))
    _temp['BottomLeft'].fill('#ff00b6')
    _temp['BottomLeft'].set_colorkey('#ff00b6')
    _temp['BottomLeft'].blit(_img, (0, -100))
    _temp['BottomMiddle'] = pygame.surface.Surface((50, 50))
    _temp['BottomMiddle'].fill('#ff00b6')
    _temp['BottomMiddle'].set_colorkey('#ff00b6')
    _temp['BottomMiddle'].blit(_img, (-50, -100))
    _temp['BottomRight'] = pygame.surface.Surface((50, 50))
    _temp['BottomRight'].fill('#ff00b6')
    _temp['BottomRight'].set_colorkey('#ff00b6')
    _temp['BottomRight'].blit(_img, (-100, -100))

    return _temp