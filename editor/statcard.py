import pygame

from singletons import resourceHandler


BACKGROUND_TILE_SIZE: int = 194
BACKGROUND_TILE_SIZE_X2: int = 388

class StatCard():
    def __init__(self, width: int, height: int) -> None:
        
        self.width: int = width * 3
        self.height: int = height
        self.actual_height: int = (self.height + 1) * 2
        
        self.size: tuple[int, int] = (self.width * BACKGROUND_TILE_SIZE, self.actual_height * BACKGROUND_TILE_SIZE)
        
        self.background: pygame.Surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.__draw_background()
        
        self.image: pygame.Surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.rect: pygame.Rect = self.image.get_rect(topleft=(0, 40))
        
    def draw(self, screen: pygame.Surface, pan: tuple[int, int], x: int) -> None:
        self.image.fill((0, 0, 0, 0))
        self.rect.topleft = (x + pan[0], 40 + pan[1])
        
        self.image.blit(self.background)
        
        screen.blit(self.image, self.rect.topleft)
        
    def __draw_background(self) -> None:
        _background: dict[str, pygame.Surface] = StatCard.__split_background()

        x: int = 0
        y: int = 0
        section: str = 'Top'

        for height in range(self.actual_height):
            if height == self.actual_height - 1:
                section = 'Bottom'

            elif height != 0:
                section = ''

            for _w in range(self.width):
                if _w == 0:
                    self.background.blit(_background[f'{section}Left'], (x, y))

                elif _w == self.width - 1:
                    self.background.blit(_background[f'{section}Right'], (x, y))

                else:
                    if _w == 4: x -= 48
                    self.background.blit(_background[f'{section}Middle'], (x, y))

                x += 194

            x = 0
            y += 194
        
    def __split_background() -> dict[str, pygame.Surface]:
        _img = resourceHandler.load_image('.\\assets\\backgrounds\\StatCardBackground.png')

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

        _temp['TopLeft'] = pygame.surface.Surface((BACKGROUND_TILE_SIZE, BACKGROUND_TILE_SIZE), pygame.SRCALPHA)
        _temp['TopLeft'].blit(_img, (0, 0))
        _temp['TopMiddle'] = pygame.surface.Surface((BACKGROUND_TILE_SIZE, BACKGROUND_TILE_SIZE), pygame.SRCALPHA)
        _temp['TopMiddle'].blit(_img, (-BACKGROUND_TILE_SIZE, 0))
        _temp['TopRight'] = pygame.surface.Surface((BACKGROUND_TILE_SIZE, BACKGROUND_TILE_SIZE), pygame.SRCALPHA)
        _temp['TopRight'].blit(_img, (-BACKGROUND_TILE_SIZE_X2, 0))

        _temp['Left'] = pygame.surface.Surface((BACKGROUND_TILE_SIZE, BACKGROUND_TILE_SIZE), pygame.SRCALPHA)
        _temp['Left'].blit(_img, (0, -BACKGROUND_TILE_SIZE))
        _temp['Middle'] = pygame.surface.Surface((BACKGROUND_TILE_SIZE, BACKGROUND_TILE_SIZE), pygame.SRCALPHA)
        _temp['Middle'].blit(_img, (-BACKGROUND_TILE_SIZE, -BACKGROUND_TILE_SIZE))
        _temp['Right'] = pygame.surface.Surface((BACKGROUND_TILE_SIZE, BACKGROUND_TILE_SIZE), pygame.SRCALPHA)
        _temp['Right'].blit(_img, (-BACKGROUND_TILE_SIZE_X2, -BACKGROUND_TILE_SIZE))

        _temp['BottomLeft'] = pygame.surface.Surface((BACKGROUND_TILE_SIZE, BACKGROUND_TILE_SIZE), pygame.SRCALPHA)
        _temp['BottomLeft'].blit(_img, (0, -BACKGROUND_TILE_SIZE_X2))
        _temp['BottomMiddle'] = pygame.surface.Surface((BACKGROUND_TILE_SIZE, BACKGROUND_TILE_SIZE), pygame.SRCALPHA)
        _temp['BottomMiddle'].blit(_img, (-BACKGROUND_TILE_SIZE, -BACKGROUND_TILE_SIZE_X2))
        _temp['BottomRight'] = pygame.surface.Surface((BACKGROUND_TILE_SIZE, BACKGROUND_TILE_SIZE), pygame.SRCALPHA)
        _temp['BottomRight'].blit(_img, (-BACKGROUND_TILE_SIZE_X2, -BACKGROUND_TILE_SIZE_X2))

        return _temp