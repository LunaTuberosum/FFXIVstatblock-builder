from settings import *


class ToggleButtons():
    def __init__(self, pos: list[int], size: list[int], buttons: dict[str, callable], default: str):
        self.pos: list[int] = pos
        self.size: list[int] = size
        self.buttons: dict[str, callable] = buttons

        self.buttonRects: dict[str, pygame.Rect] = {}

        self.buttonHovering: dict[str, bool] = {}
        for _label in self.buttons:
            self.buttonHovering[_label] = False
        
        self.buttonSelected: str = default

        self.image: pygame.Surface = pygame.Surface(self.size)
        self.rect: pygame.Rect = pygame.Rect(self.pos, self.size)

        self.buttonImage: pygame.Surface = pygame.image.load('assets/icons/ToggleButton.png').convert_alpha()
        self.buttonImage_hover: pygame.Surface = pygame.image.load('assets/icons/ToggleButton_hover.png').convert_alpha()
        self.buttonImage_selected: pygame.Surface = pygame.image.load('assets/icons/ToggleButton_selected.png').convert_alpha()

        self.font: pygame.font.Font = pygame.font.Font('assets/fonts/noto-sans.regular.ttf', 20)

        self.hovering: bool = False

    def draw(self, screen: pygame.Surface, right: int):
        self.image.fill('#313031')
        self.rect: pygame.Rect = pygame.Rect((self.pos[0] + right, self.pos[1]), self.image.size)
        
        _x: int = self.size[0]
        for label in self.buttons.keys():
            _x -= self.font.size(label)[0]
            self.image.blit(self.font.render(label, True, '#EEE1C5'), (_x, -5))
            _x -= 25
            if label == self.buttonSelected:
                self.image.blit(self.buttonImage_selected, (_x, 0))
            elif self.buttonHovering[label]:
                self.image.blit(self.buttonImage_hover, (_x, 0))
            else:
                self.image.blit(self.buttonImage, (_x, 0))
            self.buttonRects[label] = pygame.Rect(_x + self.pos[0] + right, 0 + self.pos[1], 25 + self.font.size(label)[0], 20)
            _x -= 20 + 30


        screen.blit(self.image, (self.pos[0] + right, self.pos[1]))

    def hover(self):
        self.hovering = True
        for _label, _rect in self.buttonRects.items():
            if _rect.collidepoint(pygame.mouse.get_pos()):
                self.buttonHovering[_label] = True

    def noHover(self):
        if not self.hovering:
            return
        self.hovering = False
        for _label in self.buttonRects.keys():
            self.buttonHovering[_label] = False

    def onClick(self):
        for _label, _rect in self.buttonRects.items():
            if _rect.collidepoint(pygame.mouse.get_pos()):
                self.buttonSelected = _label
                self.buttons[_label]()
                return
