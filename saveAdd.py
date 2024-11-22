from settings import *
from ui.background import Background


class SaveAdd(Background):
    def __init__(self, menu: object):
        super().__init__(
            'SaveAdd',
            'New Save',
            [250, 250],
            [0, 0],
            False
        )

        self.image: pygame.Surface = pygame.Surface((250, 250))

        self.rect: pygame.Rect = self.image.get_rect(topleft=(0, 0))

        self.hovering: bool = False

    def draw(self, screen: pygame.Surface, x: int, y: int):
        self.pos = [x, y]
        super().draw(screen, 0, [0, 0])
        self.rect = self.image.get_rect(topleft=(x, y))

        self.image.blit(self.font.render('Create New Stat Sheet', True, '#000000'), (125 - (self.font.size('Create New Stat Sheet')[0] / 2), (125 - (self.font.size('Create New Stat Sheet')[1] / 2) + 1)))
        self.image.blit(self.font.render('Create New Stat Sheet', True, '#CCCCCC' if not self.hovering else '#dedede'), (125 - (self.font.size('Create New Stat Sheet')[0] / 2), 125 - (self.font.size('Create New Stat Sheet')[1] / 2)))

        screen.blit(self.image, (x, y))

    def noHover(self):
        if not self.hovering:
            return
        self.hovering = False

    def hover(self):
        self.hovering = True
