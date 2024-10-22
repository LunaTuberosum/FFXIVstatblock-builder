from settings import *


class SwitchButton():
    def __init__(self, pos: list[int], size: list[int], image: str, imageHover: str, command: callable, commandDeactive: callable, commandUpdate: callable):
        self.pos: list[int] = pos
        self.size: list[int] = size
        self.image: pygame.Surface = pygame.image.load(image).convert_alpha()
        self.imageHover: pygame.Surface = pygame.image.load(imageHover).convert_alpha()
        self.rect: pygame.Rect = pygame.Rect(self.pos, self.size)
        self.command: callable = command
        self.commandDeactive: callable = commandDeactive
        self.commandUpdate: callable = commandUpdate

        self.hovering: bool = False
        self.on: bool = False

    def update(self):
        self.commandUpdate()

    def draw(self, screen: pygame.Surface, right: int):
        self.rect: pygame.Rect = pygame.Rect((self.pos[0] + right, self.pos[1]), self.image.size)

        screen.blit(self.imageHover if self.hovering or self.on else self.image, (self.pos[0] + right, self.pos[1]))

    def hover(self):
        self.hovering = True

    def noHover(self):
        if not self.hovering:
            return
        self.hovering = False

    def onClick(self):
        if self.on:
            self.on = False
            self.commandDeactive()
            return
        
        self.on = True
        self.command()