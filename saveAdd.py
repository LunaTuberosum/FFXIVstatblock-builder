from settings import *


class SaveAdd(pygame.sprite.Sprite):
    def __init__(self, menu: object):
        super().__init__()

        self.image: pygame.Surface = pygame.Surface((250, 250))

        self.rect: pygame.Rect = self.image.get_rect(topleft=(0, 0))
        self.font: pygame.font.Font = pygame.font.Font('assets/fonts/LibreBaskerville.ttf', 20)

        self.hovering: bool = False

    def draw(self, screen: pygame.Surface, x: int, y: int):
        self.image.fill('#efefef' if self.hovering else '#dedede')
        self.rect = self.image.get_rect(topleft=(x, y))

        self.image.blit(self.font.render('Create New Stat Sheet', True, '#000000', wraplength=240), (125 - (self.font.size('Create New Stat Sheet')[0] / 2), 125 - (self.font.size('Create New Stat Sheet')[1] / 2)))

        screen.blit(self.image, (x, y))

    def noHover(self):
        if not self.hovering:
            return
        self.hovering = False

    def hover(self):
        self.hovering = True
