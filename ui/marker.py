from components.marker import MarkerComponent
from settings import *


class MarkerUI():
    def __init__(self, pos: list[int], parentMarker: MarkerComponent):
        self.pos: list[int] = pos
        self.parentMarker: MarkerComponent = parentMarker

        self.markerArea: list[list[int]] = self.parentMarker.markerArea
        self.gridSize: list[int] = [len(self.markerArea[0]), len(self.markerArea)]

        self.image: pygame.Surface = pygame.Surface([400, 400])
        self.rect: pygame.Rect = self.image.get_rect(topleft=self.pos)

        self.type: int = self.parentMarker.type

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

        self.hoverIcon: pygame.Surface = pygame.image.load('assets/markerIcons/HoverIcon.png').convert_alpha()
        self.hoverSpot: list[int] = None

        self.markerImages()

        self.GRID: int = 0
        self.MARKER: int = 1
        self.ORIGIN: int = 2
        self.TANK: int = 3
        self.HEALER: int = 4
        self.DPS: int = 5

        self.paint: int = 0

    def draw(self, screen: pygame.Surface, right: int, scroll: list[int]):
        self.createGrid()
        self.rect: pygame.Rect = pygame.Rect((self.pos[0] + right, self.pos[1] + scroll[1]), self.image.size)

        screen.blit(self.image, (self.pos[0] + right, self.pos[1] + scroll[1]))

    def hover(self):
        _mouse: tuple[int] = pygame.mouse.get_pos()
        _pos: list[int] = [_mouse[0] - self.rect.x, _mouse[1] - self.rect.y]
        _scale: list[int] = [
            25 / ((self.gridSize[0] * 25) / 400),
            25 / ((self.gridSize[1] * 25) / 400)
        ]
        _relative: list[int] = [int(_pos[0] // _scale[0]), int(_pos[1] // _scale[1])]
        self.hoverSpot = _relative

    def noHover(self):
        if not self.hoverSpot:
            return
        self.hoverSpot = None

    def onClick(self):
        if not self.hoverSpot:
            return
        
        self.markerArea[self.hoverSpot[1]][self.hoverSpot[0]] = self.paint

    def createGrid(self) -> None:
        self.gridSize = [len(self.markerArea[0]), len(self.markerArea)]
        _size = [25 * self.gridSize[0], 25 * self.gridSize[1]]
        _image = pygame.Surface(_size)

        _origin: list[list[int]] = []

        _x: int = 0
        _y: int = 0
        for _index, _r in enumerate(self.markerArea):
            if self.type == self.PROXIMITY:
                for _i, _c in enumerate(_r):
                    _image.blit(self.markerImage if _c == 2 else self.gridImage, (_x, _y))
                    if self.hoverSpot and _i == self.hoverSpot[0] and _index == self.hoverSpot[1]:
                        _image.blit(self.hoverIcon, (_x, _y))
                    _x += 25
                _y += 25
                _x = 0
                continue
            for _i, _c in enumerate(_r):
                match(_c):
                    case 0:
                        _image.blit(self.gridImage, (_x, _y))
                    case 1:
                        _image.blit(self.markerImage, (_x, _y))
                    case 2:
                        _image.blit(self.originImage, (_x, _y))
                        _origin.append([_x, _y])
                    case 3:
                        _image.blit(self.tankIcon, (_x, _y))
                    case 4:
                        _image.blit(self.healerIcon, (_x, _y))
                    case 5:
                        _image.blit(self.dpsIcon, (_x, _y))

                if self.hoverSpot and _i == self.hoverSpot[0] and _index == self.hoverSpot[1]:
                    _image.blit(self.hoverIcon, (_x, _y))

                _x += 25
            _y += 25
            _x = 0

        if self.type == self.MOBILE and len(_origin):
            for _o in _origin:
                _image.blit(self.stakeMarkerIcon, [_o[0], _o[1] - 25])
        elif self.type == self.PROXIMITY:
            _prox: pygame.Surface = pygame.transform.scale(self.proximityMarkerIcon, _size)
            _image.blit(_prox, [0,0])

        self.adjustSize(_image)

    def adjustSize(self, image: pygame.surface):
        self.size = (400, 400)
        self.image = pygame.transform.scale(image, self.size)

    def markerImages(self):
        self.markerImage: pygame.Surface = self.markerIcon
        if self.type == self.STACK:
            self.markerImage = self.originIcon

        self.originImage: pygame.Surface = self.originIcon
        if self.type == self.STACK:
            self.originImage = self.markerIcon
        elif self.type == self.MOBILE:
            self.originImage = self.originOutlineIcon