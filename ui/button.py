from settings import *


class Button():
    def __init__(self, pos: list[int], size: list[int], image: str, imageHover: str, command: callable):
        self.pos: list[int] = pos
        self.size: list[int] = size
        self.image: pygame.Surface = pygame.image.load(image).convert_alpha()
        self.imageHover: pygame.Surface = pygame.image.load(imageHover).convert_alpha()
        self.rect: pygame.Rect = pygame.Rect(self.pos, self.size)
        self.command: callable = command

        self.hovering: bool = False

    def draw(self, screen: pygame.Surface, right: int, scroll: list[int]):
        self.rect: pygame.Rect = pygame.Rect((self.pos[0] + right, self.pos[1] + scroll[1]), self.image.size)

        screen.blit(self.image if not self.hovering else self.imageHover, (self.pos[0] + right, self.pos[1] + scroll[1]))

    def hover(self):
        self.hovering = True

    def noHover(self):
        if not self.hovering:
            return
        self.hovering = False

    def onClick(self):
        self.command()