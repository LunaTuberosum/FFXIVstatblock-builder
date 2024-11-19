from settings import *

from components.component import Component


class MarkerComponent(Component):
    def __init__(self, width: int, height: int, markerArea: list[list[int]], parentWidth: int, parent: object):
        super().__init__(
            "MarkerComponent",
            [25 * width, 25 * height],
            [parentWidth - ((25 * width) + 20), 22],
            0,
            parent
        )
        self.gridSize: list[int] = [width, height]

        self.markerArea: list[list[int]] = markerArea
        self.type: int = 3

        self.STATIONARY: int = 3
        self.STACK: int = 1
        self.MOBILE: int = 2
        self.PROXIMITY: int = 0

        self.gridImage: pygame.Surface = pygame.image.load('assets/markerIcons/SquareGrid.png').convert_alpha()
        self.markerIcon: pygame.Surface = pygame.image.load('assets/markerIcons/SquareMarker.png').convert_alpha()
        self.originIcon: pygame.Surface = pygame.image.load('assets/markerIcons/SquareOrigin.png').convert_alpha()
        self.originOutlineIcon: pygame.Surface = pygame.image.load('assets/markerIcons/SquareOriginOutline.png').convert_alpha()
        self.stakeMarkerIcon: pygame.Surface = pygame.image.load('assets/markerIcons/StakeMarker.png').convert_alpha()

        self.tankIcon: pygame.Surface = pygame.image.load('assets/markerIcons/TankMarker.png').convert_alpha()
        self.healerIcon: pygame.Surface = pygame.image.load('assets/markerIcons/HealerMarker.png').convert_alpha()
        self.dpsIcon: pygame.Surface = pygame.image.load('assets/markerIcons/DPSMarker.png').convert_alpha()

        self.proximityMarkerIcon: pygame.Surface = pygame.image.load('assets/markerIcons/ProximityMarker.png').convert_alpha()

        self.markerImages()

        self.GRID: int = 0
        self.MARKER: int = 1
        self.ORIGIN: int = 2

        self.createGrid()

        self.parentWidth: int = parentWidth
        self.adjustSize()

    def draw(self, screen: pygame.Surface, parentPos: list[int]):
        self.createGrid()
        self.adjustSize()
        screen.blit(self.image, (parentPos[0] + self.x(), parentPos[1] + self.y()))

    def createGrid(self) -> None:
        self.size = [25 * self.gridSize[0], 25 * self.gridSize[1]]
        self.image = pygame.Surface(self.size)

        _origin: list[list[int]] = []

        _x: int = 0
        _y: int = 0
        for _r in self.markerArea:
            if self.type == self.PROXIMITY:
                for _c in _r:
                    self.image.blit(self.markerImage if _c == 2 else self.gridImage, (_x, _y))
                    _x += 25
                _y += 25
                _x = 0
                continue
            for _c in _r:
                match(_c):
                    case 0:
                        self.image.blit(self.gridImage, (_x, _y))
                    case 1:
                        self.image.blit(self.markerImage, (_x, _y))
                    case 2:
                        self.image.blit(self.originImage, (_x, _y))
                        _origin.append([_x, _y])
                    case 3:
                        self.image.blit(self.tankIcon, (_x, _y))
                    case 4:
                        self.image.blit(self.healerIcon, (_x, _y))
                    case 5:
                        self.image.blit(self.dpsIcon, (_x, _y))

                _x += 25
            _y += 25
            _x = 0

        if self.type == self.MOBILE and len(_origin):
            for _o in _origin:
                self.image.blit(self.stakeMarkerIcon, [_o[0], _o[1] - 25])
        elif self.type == self.PROXIMITY:
            _prox: pygame.Surface = pygame.transform.scale(self.proximityMarkerIcon, self.size)
            self.image.blit(_prox, [0,0])

    def adjustSize(self):
        if self.width() > 150:
            self.size = (150, self.height())
            self.image = pygame.transform.scale(self.image, self.size)
            self.pos[0] = self.parentWidth - 170

        if self.height() > 150:
            self.size = (self.width(), 150)
            self.image = pygame.transform.scale(self.image, self.size)

        self.pos = [self.parentWidth - (self.width() + 20), 22]

    def markerImages(self):
        self.markerImage: pygame.Surface = self.markerIcon
        if self.type == self.STACK:
            self.markerImage = self.originIcon

        self.originImage: pygame.Surface = self.originIcon
        if self.type == self.STACK:
            self.originImage = self.markerIcon
        elif self.type == self.MOBILE:
            self.originImage = self.originOutlineIcon

    def save(self) -> dict:
        return {
            'type': self.type,
            'gridSize': self.gridSize,
            'markerArea': self.markerArea,
            'type': self.type
        }