from settings import *

from statCard import StatCard


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

def draw(screen: pygame.Surface, statCards: list[StatCard], scroll: list[float]):

    _x: int = 20
    for _card in statCards:
        _card.draw(screen, scroll, _x)
        _x += _card.totalWidth + 20

def main(screen: pygame.Surface, clock: pygame.time.Clock, file: int) -> None:
    font: pygame.font.Font = pygame.font.Font('assets/fonts/jupiter_pro_regular.otf', 40)
    tempScreen: pygame.Surface = pygame.surface.Surface((SCREEN_WIDTH * 3, SCREEN_HEIGHT * 3))
    tempScreen.fill('#b7b7b7')

    statCardBackground: dict[str, pygame.Surface] = _splitStatCardBackground()
    scrollY: float = 0.0
    scrollX: float = 0.0
    horiScroll: bool = False
    pan: list[bool] = [False, False]
    
    zoom: bool = False
    zoomScroll: float = 1

    center: bool = False

    statCards: list[StatCard] = []
    statCards.append(StatCard(statCardBackground, 1, 0))

    while True:
        clock.tick(30)
        screen.fill('#B7B7B7')
        tempScreen.fill('#B7B7B7')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT:
                    horiScroll = True

                if event.key == pygame.K_SPACE:
                    pan[0] = True
                    if center:
                        scrollX = 0
                        scrollY = 0

                if event.key == pygame.K_LCTRL:
                    center = True
                    zoom = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LSHIFT:
                    horiScroll = False

                if event.key == pygame.K_SPACE:
                    pan[0] = False

                if event.key == pygame.K_LCTRL:
                    center = False
                    zoom = False

            if event.type == pygame.MOUSEWHEEL:
                if zoom:
                    zoomScroll += -event.y / 2
                    if zoomScroll > 2: zoomScroll = 2
                    if zoomScroll < .5: zoomScroll = .5 # change to 1

                elif horiScroll:
                    scrollX += event.y * (20 * zoomScroll)
                    if scrollX > 0:
                        scrollX = 0
                else:
                    scrollY += event.y * (20 * zoomScroll)
                    if scrollY > 0:
                        scrollY = 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pan[1] = True

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    pan[1] = False

            if event.type == pygame.MOUSEMOTION:
                if pan[0] and pan[1]:
                    scrollX += event.rel[0]
                    if scrollX > 0:
                        scrollX = 0
                    scrollY += event.rel[1]
                    if scrollY > 0:
                        scrollY = 0

        draw(tempScreen, statCards, [scrollX, scrollY])
        _image: pygame.Surface = pygame.transform.scale(tempScreen, (tempScreen.get_width() / zoomScroll, tempScreen.get_height() / zoomScroll))

        screen.blit(_image, (0, 0))

        pygame.display.flip()

                