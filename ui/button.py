from settings import *


class Button():
    def __init__(self, pos: list[int], size: list[int], image: str, imageHover: str, command: callable, text: str = ''):
        self.pos: list[int] = pos
        self.size: list[int] = size
        self.image: pygame.Surface = pygame.image.load(image).convert_alpha()
        self.imageHover: pygame.Surface = pygame.image.load(imageHover).convert_alpha()
        self.rect: pygame.Rect = pygame.Rect(self.pos, self.size)
        self.command: callable = command
        self.text = text
        
        self.font: pygame.font.Font = pygame.font.Font('assets/fonts/noto-sans.regular.ttf', 18)

        self.hovering: bool = False

    def draw(self, screen: pygame.Surface, right: int, scroll: list[int]):
        self.rect: pygame.Rect = pygame.Rect((self.pos[0] + right, self.pos[1] + scroll[1]), self.image.size)
        _image: pygame.surface = self.imageHover.copy() if self.hovering else self.image.copy()

        if self.hovering:
            _image.blit(self.font.render(self.text, True, '#ffffff'), ((self.size[0] / 2) - (self.font.size(self.text)[0] / 2), (self.size[1] / 2) - (self.font.size(self.text)[1] / 2)))
            screen.blit(_image, (self.pos[0] + right, self.pos[1] + scroll[1]))
        else:
            _image.blit(self.font.render(self.text, True, '#ffffff'), ((self.size[0] / 2) - (self.font.size(self.text)[0] / 2), (self.size[1] / 2) - (self.font.size(self.text)[1] / 2)))
            screen.blit(_image, (self.pos[0] + right, self.pos[1] + scroll[1]))

    def hover(self):
        self.hovering = True

    def noHover(self):
        if not self.hovering:
            return
        self.hovering = False

    def onClick(self):
        self.command()