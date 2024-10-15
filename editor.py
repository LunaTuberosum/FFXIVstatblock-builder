from settings import *

from statCard import StatCard

class Editor():
    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock, file: int):
        self.screen: pygame.Surface = screen
        self.clock: pygame.time.Clock = clock
        self.file: int = file

        self.tempScreen: pygame.Surface = pygame.surface.Surface((SCREEN_WIDTH * 3, SCREEN_HEIGHT * 3))
        self.statCardBackground: dict[str, pygame.Surface] = _splitStatCardBackground()

        self.scrollY: float = 0.0
        self.scrollX: float = 0.0
        self.horiScroll: bool = False
        self.pan: list[bool] = [False, False]
        
        self.zoom: bool = False
        self.zoomScroll: float = 1

        self.center: bool = False

        self.statCards: list[StatCard] = []

    def draw(self):

        _x: int = 20
        for _card in self.statCards:
            _card.draw(self.tempScreen, [self.scrollX, self.scrollY], _x)
            _x += _card.totalWidth + 20

    def keyHandler(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            self.keyDown(event)

        if event.type == pygame.KEYUP:
            self.keyUp(event)

    def keyDown(self, event: pygame.event.Event):
        if event.key == pygame.K_LSHIFT:
            self.horiScroll = True

        if event.key == pygame.K_SPACE:
            self.pan[0] = True
            if self.center:
                self.scrollX = 0
                self.scrollY = 0

        if event.key == pygame.K_LCTRL:
            self.center = True
            self.zoom = True

    def keyUp(self, event: pygame.event.Event):
        if event.key == pygame.K_LSHIFT:
            self.horiScroll = False

        if event.key == pygame.K_SPACE:
            self.pan[0] = False

        if event.key == pygame.K_LCTRL:
            self.center = False
            self.zoom = False

    def mouseHandler(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEWHEEL:
            self.mouseWheel(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.mouseDown(event)

        if event.type == pygame.MOUSEBUTTONUP:
            self.mouseUp(event)

        if event.type == pygame.MOUSEMOTION:
            self.mouseMotion(event)

    def mouseWheel(self, event: pygame.event.Event):
        if self.zoom:
            self.zoomScroll += -event.y / 2
            if self.zoomScroll > 2: self.zoomScroll = 2
            if self.zoomScroll < .5: self.zoomScroll = .5 # change to 1

        elif self.horiScroll:
            self.scrollX += event.y * (20 * self.zoomScroll)
            if self.scrollX > 0:
                self.scrollX = 0
        else:
            self.scrollY += event.y * (20 * self.zoomScroll)
            if self.scrollY > 0:
                self.scrollY = 0

    def mouseDown(self, event: pygame.event.Event):
        if event.button == 1:
            self.pan[1] = True

    def mouseUp(self, event: pygame.event.Event):
        if event.button == 1:
            self.pan[1] = False

    def mouseMotion(self, event: pygame.event.Event):
        if self.pan[0] and self.pan[1]:
            self.scrollX += event.rel[0]
            if self.scrollX > 0:
                self.scrollX = 0
            self.scrollY += event.rel[1]
            if self.scrollY > 0:
                self.scrollY = 0

    def main(self) -> None:
        self.statCards.append(
            StatCard(self.statCardBackground, 1, 0) # Temp
        )

        while True:
            self.clock.tick(30)
            self.tempScreen.fill('#B7B7B7')

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                self.keyHandler(event)

                self.mouseHandler(event)

            self.draw()
            _image: pygame.Surface = pygame.transform.scale(self.tempScreen, (self.tempScreen.get_width() / self.zoomScroll, self.tempScreen.get_height() / self.zoomScroll))

            self.screen.blit(_image, (0, 0))

            pygame.display.flip()

def _splitStatCardBackground() -> dict[str, pygame.Surface]:
        _img = pygame.image.load('assets/backgrounds/StatCardBackground.png').convert_alpha()

        _temp: dict[str, pygame.Surface] = {
            'TopLeft': None,
            'TopMiddle': None,
            'TopRight': None,
            'Left': None,
            'Middle': None,
            'Right': None,
            'BottomLeft': None,
            'BottomMiddle': None,
            'BottomRight': None
        }

        _temp['TopLeft'] = pygame.surface.Surface((194, 194))
        _temp['TopLeft'].fill('#b7b7b7')
        _temp['TopLeft'].blit(_img, (0, 0))
        _temp['TopMiddle'] = pygame.surface.Surface((194, 194))
        _temp['TopMiddle'].fill('#b7b7b7')
        _temp['TopMiddle'].blit(_img, (-194, 0))
        _temp['TopRight'] = pygame.surface.Surface((194, 194))
        _temp['TopRight'].fill('#b7b7b7')
        _temp['TopRight'].blit(_img, (-388, 0))

        _temp['Left'] = pygame.surface.Surface((194, 194))
        _temp['Left'].fill('#b7b7b7')
        _temp['Left'].blit(_img, (0, -194))
        _temp['Middle'] = pygame.surface.Surface((194, 194))
        _temp['Middle'].fill('#b7b7b7')
        _temp['Middle'].blit(_img, (-194, -194))
        _temp['Right'] = pygame.surface.Surface((194, 194))
        _temp['Right'].fill('#b7b7b7')
        _temp['Right'].blit(_img, (-388, -194))

        _temp['BottomLeft'] = pygame.surface.Surface((194, 194))
        _temp['BottomLeft'].fill('#b7b7b7')
        _temp['BottomLeft'].blit(_img, (0, -388))
        _temp['BottomMiddle'] = pygame.surface.Surface((194, 194))
        _temp['BottomMiddle'].fill('#b7b7b7')
        _temp['BottomMiddle'].blit(_img, (-194, -388))
        _temp['BottomRight'] = pygame.surface.Surface((194, 194))
        _temp['BottomRight'].fill('#b7b7b7')
        _temp['BottomRight'].blit(_img, (-388, -388))

        return _temp  