from components.ability import AbilityComponent
from components.name import NameComponent
from components.sectionName import SectionNameComponent
from components.topStats import TopStatsComponent
from components.trait import TraitComponent
from contextMenu import ContextMenu
from settings import *

from statCard import StatCard
from ui.name import NameUI

class Editor():
    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock, file: int):
        self.screen: pygame.Surface = screen
        self.clock: pygame.time.Clock = clock
        self.file: int = file

        self.tempScreen: pygame.Surface = pygame.surface.Surface((SCREEN_WIDTH * 3, SCREEN_HEIGHT * 3))
        self.statCardBackground: dict[str, pygame.Surface] = _splitStatCardBackground()

        self.font: pygame.font.Font = pygame.font.Font('assets/fonts/noto-sans.regular.ttf', 18)

        self.scrollY: float = 0.0
        self.scrollX: float = 0.0
        self.horiScroll: bool = False
        self.pan: list[bool] = [False, False]
        
        self.zoom: bool = False
        self.zoomScroll: float = 1

        self.center: bool = False

        self.statCards: pygame.sprite.Group[StatCard] = pygame.sprite.Group()

        #temp
        self.contextMenu: ContextMenu = None
        self.contextMenuPos: list[int] = []

    def draw(self):
        self.tempScreen.fill('#313031')

        _x: int = 40
        for _card in self.statCards:
            _card.draw(self.tempScreen, [self.scrollX, self.scrollY], _x)
            _x += _card.totalWidth + 20

    def drawUI(self):
        for _card in self.statCards:
            for _component in _card.components:
                if _component.window:
                    _component.window.draw(self.tempScreen, _card.rect.right, [self.scrollX, self.scrollY])

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

        for _statCard in self.statCards:
            for _component in _statCard.components:
                if not _component.window:
                    continue
                if hasattr(_component.window, 'effectsList'):
                    for _effect in _component.window.effectsList:
                        for _comp in _effect:
                            if hasattr(_comp, 'text'):
                                _comp.typing(event)
                for _comp in _component.window.components:
                    if hasattr(_comp, 'text'):
                        _comp.typing(event)

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

            if self.contextMenu:
                if not self.contextMenu.rect.collidepoint(pygame.mouse.get_pos()):
                    self.contextMenu = None
                    return

                for _option in self.contextMenu.options:
                    _option.clicked = False

                    if _option.rect.collidepoint(pygame.mouse.get_pos()):
                        _option.onClick()
                        self.contextMenu = None
                        return

            for _statCard in self.statCards:
                for _component in _statCard.components:
                    if _component.window and _component.window.rect.collidepoint(pygame.mouse.get_pos()):

                        for _comp in _component.window.components:
                            if hasattr(_comp, 'active'): 
                                if _comp.active:
                                    _comp.exitField()
                                _comp.active = False
                            if _comp.rect.collidepoint(pygame.mouse.get_pos()):
                                _comp.onClick()
                                
                        if hasattr(_component.window, 'onClick'):
                            _component.window.onClick()
                            return
                        return
                    
                    
                    
                    if _component.rect.collidepoint(pygame.mouse.get_pos()):
                        _component.onClick()
                    else:
                        _component.window = None

        elif event.button == 3:
            for _statCard in self.statCards:
                if _statCard.rect.collidepoint(pygame.mouse.get_pos()):
                    self.contextMenu = _statCard.contextMenu()
                    self.contextMenuPos = pygame.mouse.get_pos()
                    return
            self.contextMenu = ContextMenu([186, 96], {
                'New Card': self.new,
                'Save': self.save,
                'Export as PNG': self.export
            })
            self.contextMenuPos = pygame.mouse.get_pos()

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

    def statCardHover(self):
        for _statCard in self.statCards:
            for _component in _statCard.components:
                _component.noHover()
                
                if _component.window and _component.window.rect.collidepoint(pygame.mouse.get_pos()):
                    for _statCard in self.statCards:
                        for _component in _statCard.components:
                            _component.noHover()

                            if not _component.window:
                                continue
                            if hasattr(_component.window, 'hover'):
                                _component.window.hover()
                            for _comp in _component.window.components:
                                _comp.noHover()
                                if _comp.rect.collidepoint(pygame.mouse.get_pos()):
                                    _comp.hover()
                    return
                if _component.rect.collidepoint(pygame.mouse.get_pos()):
                    if not _component.hovering:
                        _component.hover()

    def main(self) -> None:
        while True:
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                self.keyHandler(event)

                self.mouseHandler(event)

            self.statCardHover()

            if self.contextMenu:

                for _option in self.contextMenu.options:
                    _option.noHover()

                    if _option.rect.collidepoint(pygame.mouse.get_pos()):
                        if not _option.hovering:
                            _option.hover()

            self.draw()
            self.drawUI()
            _image: pygame.Surface = pygame.transform.scale(self.tempScreen, (self.tempScreen.get_width() / self.zoomScroll, self.tempScreen.get_height() / self.zoomScroll))

            self.screen.blit(_image, (0, 0))

            if self.contextMenu:
                self.contextMenu.draw(self.screen, self.contextMenuPos)

            pygame.display.flip()

    def new(self):
        _card: StatCard = StatCard(self.statCardBackground, 1, 0, self)
        _card.addComponent(NameComponent())
        _card.addComponent(TopStatsComponent())

        _card.addComponent(SectionNameComponent('Traits', 2))
        _card.addComponent(TraitComponent(
            'Elite Foe: Lord of the Corpse Hall',
            'This character cannot be {b} Stunned {/b} and markers they have generated cannot be removed. Be sure to inform players of this before beginning the encounter.'
        ))
        _card.addComponent(TraitComponent(
            'Survive and Receive Valhalla',
            'This creature summons 2 [Gungnir] 3 spaces from itself at the start of each round.'
        ))

        _card.addComponent(SectionNameComponent('Abilites', 2))

        _card.addComponent(AbilityComponent(
            'Shin-Zantetsiken',
            'Primary, Physical',
            {
                'Marker Area:': 'The entire encounter map',
                'Target:': 'All enemies within the marker area',
                'Marker Trigger:': 'The beginning of the 3rd round',
                'Marker Effect:': 'Deals 999 damage.'
            }
        ))

        _card.addComponent(AbilityComponent(
            'Gungnir',
            'Primary, Mobile Marker, Magic',
            {
                'Origin:': 'Two squares occupied by two separate enemy characters without {b} Enmity {/b}',
                'Marker Area:': 'A mobile 5x5 area centered on the origins',
                'Target:': 'All enemies within the marker area',
                'Marker Trigger:': 'The beginning of this character\'s next turn',
                'Marker Effect:': 'Deals 3d6 damage and summons a [Gungnir] in an unoccupied adjacenet area to the center.'
            },
            [
                [0, 0, 0, 0, 0, 0, 0],
                [0, 1, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 0],
                [0, 1, 1, 2, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 0],
                [0, 0, 0, 0, 0, 0, 0]
            ]
        ))
        self.statCards.add(
            _card
        )

    def save(self):
        print('Save')

    def export(self):
        print('Export')

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
    _temp['TopLeft'].fill('#313031')
    _temp['TopLeft'].blit(_img, (0, 0))
    _temp['TopMiddle'] = pygame.surface.Surface((194, 194))
    _temp['TopMiddle'].fill('#313031')
    _temp['TopMiddle'].blit(_img, (-194, 0))
    _temp['TopRight'] = pygame.surface.Surface((194, 194))
    _temp['TopRight'].fill('#313031')
    _temp['TopRight'].blit(_img, (-388, 0))

    _temp['Left'] = pygame.surface.Surface((194, 194))
    _temp['Left'].fill('#313031')
    _temp['Left'].blit(_img, (0, -194))
    _temp['Middle'] = pygame.surface.Surface((194, 194))
    _temp['Middle'].fill('#313031')
    _temp['Middle'].blit(_img, (-194, -194))
    _temp['Right'] = pygame.surface.Surface((194, 194))
    _temp['Right'].fill('#313031')
    _temp['Right'].blit(_img, (-388, -194))

    _temp['BottomLeft'] = pygame.surface.Surface((194, 194))
    _temp['BottomLeft'].fill('#313031')
    _temp['BottomLeft'].blit(_img, (0, -388))
    _temp['BottomMiddle'] = pygame.surface.Surface((194, 194))
    _temp['BottomMiddle'].fill('#313031')
    _temp['BottomMiddle'].blit(_img, (-194, -388))
    _temp['BottomRight'] = pygame.surface.Surface((194, 194))
    _temp['BottomRight'].fill('#313031')
    _temp['BottomRight'].blit(_img, (-388, -388))

    return _temp