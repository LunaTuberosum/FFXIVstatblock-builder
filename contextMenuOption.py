from settings import *


class ContextMenuOption():
    def __init__(self, pos: list[int], text: str, size: list[int], call: callable):
        self.pos: list[int] = pos
        self.text: str = text
        self.size: list[int] = size
        self.call: callable = call

        _mousePos: list[int] = pygame.mouse.get_pos()
        self.rect: pygame.Rect = pygame.Rect(_mousePos[0] + self.pos[0], _mousePos[1] + self.pos[1], self.size[0], self.size[1])

        self.font: pygame.font.Font = pygame.font.Font('assets/fonts/noto-sans.regular.ttf', 18)

        self.hovering: bool = False
        self.clicked: bool = False

        self.contextMenuHoverBackground: pygame.Surface = pygame.image.load('assets/backgrounds/ContextMenuHoverBackground.png').convert_alpha()
        self.contextMenuClickedBackground: pygame.Surface = pygame.image.load('assets/backgrounds/ContextMenuClickedBackground.png').convert_alpha()

    def draw(self, screen: pygame.Surface):
        if self.hovering:
            screen.blit(self.contextMenuHoverBackground, (self.pos[0] - 9, self.pos[1] + 2))
        if self.clicked:
            screen.blit(self.contextMenuClickedBackground, (self.pos[0] - 9, self.pos[1] + 2))

        screen.blit(self.font.render(self.text, True, '#000000'), (self.pos[0], self.pos[1] + 1))
        screen.blit(self.font.render(self.text, True, '#DED2B8'), (self.pos))

    def hover(self):
        self.hovering = True

    def noHover(self):
        if not self.hovering:
            return
        self.hovering = False

    def onClick(self):
        self.clicked = True
        self.call()