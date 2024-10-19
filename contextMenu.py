from contextMenuOption import ContextMenuOption
from settings import *
        # Size 186, 96

class ContextMenu(pygame.sprite.Sprite):
    def __init__(self, size: list[int], options: dict[str, callable]):
        super().__init__()

        self.contextMenuBackgound: dict[str, pygame.Surface] = _splitBackground()
        
        self.image = pygame.Surface(size)
        _mouse: list[int] = pygame.mouse.get_pos()
        self.rect: pygame.Rect = pygame.Rect(_mouse[0], _mouse[1], size[0], size[1])

        self.size: list[int] = size

        self.options: list[ContextMenuOption] = []
        _y: int = 11
        for _option, _call in options.items():
            self.options.append(ContextMenuOption([23, _y], _option, [164, 24], _call))
            _y += 25

    def draw(self, screen: pygame.Surface, mousePos: list[int]):
        self.image.fill('#ff00b6')
        self.image.set_colorkey('#ff00b6')

        self.image.blit(self.contextMenuBackgound['TopLeft'], (0, 0))
        self.image.blit(self.contextMenuBackgound['TopRight'], (self.size[0] - 14, 0))
        self.image.blit(self.contextMenuBackgound['BottomLeft'], (0, self.size[1] - 14))
        self.image.blit(self.contextMenuBackgound['BottomRight'], (self.size[0] - 14, self.size[1] - 14))

        self.image.blit(pygame.transform.scale(self.contextMenuBackgound['TopMiddle'], (self.size[0] - 28, 14)), (14, 0))
        self.image.blit(pygame.transform.scale(self.contextMenuBackgound['Left'], (14, self.size[1] - 28)), (0, 14))
        self.image.blit(pygame.transform.scale(self.contextMenuBackgound['Right'], (14, self.size[1] - 28)), (self.size[0] - 14, 14))
        self.image.blit(pygame.transform.scale(self.contextMenuBackgound['BottomMiddle'], (self.size[0] - 28, 14)), (14, self.size[1] - 14))

        self.image.blit(pygame.transform.scale(self.contextMenuBackgound['Middle'], (self.size[0] - 28, self.size[1] - 28)), (14, 14))

        for _option in self.options:
            _option.draw(self.image)

        screen.blit(self.image, mousePos)

def _splitBackground() -> dict[str, pygame.Surface]:
    _img = pygame.image.load('assets/backgrounds/ContextMenuBackground.png').convert_alpha()

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

    _temp['TopLeft'] = pygame.surface.Surface((14, 14))
    _temp['TopLeft'].fill('#ff00b6')
    _temp['TopLeft'].set_colorkey('#ff00b6')
    _temp['TopLeft'].blit(_img, (0, 0))
    _temp['TopMiddle'] = pygame.surface.Surface((14, 14))
    _temp['TopMiddle'].fill('#ff00b6')
    _temp['TopMiddle'].set_colorkey('#ff00b6')
    _temp['TopMiddle'].blit(_img, (-14, 0))
    _temp['TopRight'] = pygame.surface.Surface((14, 14))
    _temp['TopRight'].fill('#ff00b6')
    _temp['TopRight'].set_colorkey('#ff00b6')
    _temp['TopRight'].blit(_img, (-28, 0))

    _temp['Left'] = pygame.surface.Surface((14, 14))
    _temp['Left'].fill('#ff00b6')
    _temp['Left'].set_colorkey('#ff00b6')
    _temp['Left'].blit(_img, (0, -14))
    _temp['Middle'] = pygame.surface.Surface((14, 14))
    _temp['Middle'].fill('#ff00b6')
    _temp['Middle'].set_colorkey('#ff00b6')
    _temp['Middle'].blit(_img, (-14, -14))
    _temp['Right'] = pygame.surface.Surface((14, 14))
    _temp['Right'].fill('#ff00b6')
    _temp['Right'].set_colorkey('#ff00b6')
    _temp['Right'].blit(_img, (-28, -14))

    _temp['BottomLeft'] = pygame.surface.Surface((14, 14))
    _temp['BottomLeft'].fill('#ff00b6')
    _temp['BottomLeft'].set_colorkey('#ff00b6')
    _temp['BottomLeft'].blit(_img, (0, -28))
    _temp['BottomMiddle'] = pygame.surface.Surface((14, 14))
    _temp['BottomMiddle'].fill('#ff00b6')
    _temp['BottomMiddle'].set_colorkey('#ff00b6')
    _temp['BottomMiddle'].blit(_img, (-14, -28))
    _temp['BottomRight'] = pygame.surface.Surface((14, 14))
    _temp['BottomRight'].fill('#ff00b6')
    _temp['BottomRight'].set_colorkey('#ff00b6')
    _temp['BottomRight'].blit(_img, (-28, -28))

    return _temp