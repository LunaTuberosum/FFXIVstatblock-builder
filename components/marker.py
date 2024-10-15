from settings import *

from components.component import Component


class MarkerComponent(Component):
    def __init__(self, width: int, height: int, markerArea: list[list[int]], parentWidth: int):
        super().__init__(
            "MarkerComponent",
            [25 * width, 25 * height],
            [parentWidth - ((25 * width) + 20), 22],
            0
        )

        self.markerArea: list[list[int]] = markerArea

        self.gridImage: pygame.Surface = pygame.image.load('assets/markerIcons/SquareGrid.png').convert_alpha()
        self.markerImage: pygame.Surface = pygame.image.load('assets/markerIcons/SquareMarker.png').convert_alpha()
        self.originImage: pygame.Surface = pygame.image.load('assets/markerIcons/SquareOrigin.png').convert_alpha()

        self.GRID: int = 0
        self.MARKER: int = 1
        self.ORIGIN: int = 2

        self.createGrid()

        if self.width() > 150:
            self.size = (150, self.height())
            self.image = pygame.transform.scale(self.image, self.size)
            self.pos[0] = parentWidth - 170

        if self.height() > 150:
            self.size = (self.width(), 150)
            self.image = pygame.transform.scale(self.image, self.size)

    def draw(self, screen: pygame.Surface, parentPos: list[int]):
        screen.blit(self.image, (parentPos[0] + self.x(), parentPos[1] + self.y()))

    def createGrid(self) -> None:

        _x: int = 0
        _y: int = 0
        for _r in self.markerArea:
            for _c in _r:
                match(_c):
                    case 0:
                        self.image.blit(self.gridImage, (_x, _y))
                    case 1:
                        self.image.blit(self.markerImage, (_x, _y))
                    case 2:
                        self.image.blit(self.originImage, (_x, _y))

                _x += 25
            _y += 25
            _x = 0