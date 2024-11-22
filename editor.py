import json
from components.ability import AbilityComponent
from components.marker import MarkerComponent
from components.name import NameComponent
from components.sectionName import SectionNameComponent
from components.topStats import TopStatsComponent
from components.trait import TraitComponent
from contextMenu import ContextMenu
from settings import *

from statCard import StatCard
from ui.background import Background
from ui.confirm import ConfirmUI
from ui.editCard import EditCardUI
from ui.newCard import NewCardUI

class Editor():
    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock, file: int):
        self.screen: pygame.Surface = screen
        self.clock: pygame.time.Clock = clock
        self.file: int = file

        self.statCardBackground: dict[str, pygame.Surface] = _splitStatCardBackground()
        self.statCards: pygame.sprite.Group[StatCard] = pygame.sprite.Group()

        self.load()

        self.window: Background = None

        self.tempScreen: pygame.Surface = pygame.surface.Surface((SCREEN_WIDTH * 3, SCREEN_HEIGHT * 3))

        self.font: pygame.font.Font = pygame.font.Font('assets/fonts/noto-sans.regular.ttf', 18)

        self.scrollY: float = 0.0
        self.scrollX: float = 0.0
        self.horiScroll: bool = False
        self.pan: list[bool] = [False, False]
        
        self.zoom: bool = False
        self.zoomScroll: float = 1

        self.center: bool = False

        #temp
        self.contextMenu: ContextMenu = None
        self.contextMenuPos: list[int] = []

        self.game: bool = True

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

        if event.key == pygame.K_ESCAPE:
            self.escape()

        if self.window:
            for _comp in self.window.components:
                if hasattr(_comp, 'typing'):
                    _comp.typing(event)

        for _statCard in self.statCards:
            for _component in _statCard.components:
                if not _component.window:
                    continue
                if hasattr(_component.window, 'effectsList'):
                    for _effect in _component.window.effectsList:
                        for _comp in _effect:
                            if hasattr(_comp, 'typing'):
                                _comp.typing(event)
                if hasattr(_component.window, 'window') and _component.window.window:
                    for _comp in _component.window.window.components:
                        if hasattr(_comp, 'typing'):
                            _comp.typing(event)
                for _comp in _component.window.components:
                    if hasattr(_comp, 'typing'):
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
            self.scrollX += event.y * (40 * self.zoomScroll)
            if self.scrollX > 0:
                self.scrollX = 0
        else:
            self.scrollY += event.y * (40 * self.zoomScroll)
            if self.scrollY > 0:
                self.scrollY = 0

    def mouseDown(self, event: pygame.event.Event):
        if event.button == 1:
            self.pan[1] = True

            if self.window:
                if not self.window.rect.collidepoint(pygame.mouse.get_pos()):
                    self.window = None
                    return
                
                for _comp in self.window.components:
                    if hasattr(_comp, 'active'): 
                        if _comp.active:
                            _comp.exitField()
                        _comp.active = False
                    if _comp.rect.collidepoint(pygame.mouse.get_pos()):
                        _comp.onClick()
                        return

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
                    if _component.window:
                        if hasattr(_component.window, 'window') and _component.window.window:
                            if _component.window.window.rect.collidepoint(pygame.mouse.get_pos()):
                                _component.window.window.onClick()
                                return
                        if _component.window.rect.collidepoint(pygame.mouse.get_pos()):
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
                
                if _component.window:
                    if hasattr(_component.window, 'window') and _component.window.window:
                        if _component.window.window.rect.collidepoint(pygame.mouse.get_pos()):
                            _component.window.window.hover()
                    if _component.window.rect.collidepoint(pygame.mouse.get_pos()):
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
        while self.game:
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                self.keyHandler(event)

                self.mouseHandler(event)

            self.statCardHover()

            if self.window:

                for _comp in self.window.components:
                    _comp.noHover()

                    if _comp.rect.collidepoint(pygame.mouse.get_pos()):
                        if not _comp.hovering:
                            _comp.hover()

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

            if self.window: self.window.draw(self.screen, 0, [0, 0])

            pygame.display.flip()
        
        return self.save()

    def escape(self):
        def escapeConfirm():
            self.game = False
            self.window = False

        self.window = ConfirmUI(self, 'Are you sure you want to leave this sheet?', escapeConfirm, 'Save and Quit')

    def new(self):
        self.window = NewCardUI(self)

    def edit(self, statCard: StatCard):
        self.window = EditCardUI(self, statCard)

    def save(self):
        _saveDict: dict = {}
        for _i, _card in enumerate(self.statCards):
            _saveDict[str(_i)] = _card.save()

        _jsonSave: str = json.dumps(_saveDict, indent=4)

        with open(f'saves/statSheet{self.file}.json', 'w') as _jsonFile:
            _jsonFile.write(_jsonSave)

        return _saveDict

    def load(self):
        try:
            with open(f'saves/statSheet{self.file}.json', 'r') as _jsonFile:
                _saveDict: dict = json.load(_jsonFile)

            for _i, _card in _saveDict.items():
                _c: StatCard = StatCard(self.statCardBackground, _card['width'], _card['height'], self)

                _c.addComponent(NameComponent(_c))
                _c.components[0].name = _card['components']['NameComponent [0]']['name']
                _c.components[0].level = _card['components']['NameComponent [0]']['level']
                _c.components[0].levelPosition = _card['components']['NameComponent [0]']['levelPosition']

                _c.addComponent(TopStatsComponent(_c, _card['components']['TopStatsComponent [1]']['token']))
                _c.components[1].creatureSize = _card['components']['TopStatsComponent [1]']['creatureSize']
                _c.components[1].species = _card['components']['TopStatsComponent [1]']['species']
                _c.components[1].vigilance = _card['components']['TopStatsComponent [1]']['vigilance']
                _c.components[1].defense = _card['components']['TopStatsComponent [1]']['defense']
                _c.components[1].magicDefense = _card['components']['TopStatsComponent [1]']['magicDefense']
                _c.components[1].maxHP = _card['components']['TopStatsComponent [1]']['maxHP']
                _c.components[1].speed = _card['components']['TopStatsComponent [1]']['speed']
                _c.components[1].str = _card['components']['TopStatsComponent [1]']['str']
                _c.components[1].dex = _card['components']['TopStatsComponent [1]']['dex']
                _c.components[1].vit = _card['components']['TopStatsComponent [1]']['vit']
                _c.components[1].int = _card['components']['TopStatsComponent [1]']['int']
                _c.components[1].mnd = _card['components']['TopStatsComponent [1]']['mnd']

                for _compN, _compV in _card['components'].items():
                    _compName: str = _compN.split(' ')[0]

                    match (_compName):
                        case 'SectionNameComponent':
                            _c.addComponent(SectionNameComponent(_compV['section'], 2, _c))
                            continue
                        case 'TraitComponent':
                            _c.addComponent(TraitComponent(_compV['name'], _compV['desc'], _c))
                            continue
                        case 'AbilityComponent':
                            _a: AbilityComponent = AbilityComponent(
                                _compV['name'],
                                _compV['types'],
                                _compV['effects'],
                                _c
                            )
                            if _compV['marker']:
                                _a.marker = MarkerComponent(
                                    _compV['marker']['gridSize'][0],
                                    _compV['marker']['gridSize'][1],
                                    _compV['marker']['markerArea'],
                                    _a.width(),
                                    _a
                                )
                                _a.marker.type = _compV['marker']['type']
                            _c.addComponent(_a)
                            continue

                self.statCards.add(_c)
            
        except:
            _jsonSave: str = json.dumps({}, indent=4)

            with open(f'saves/statSheet{self.file}.json', 'w') as _jsonFile:
                _jsonFile.write(_jsonSave)

    def export(self):
        _width: int = 40
        _height: int = 40

        for _card in self.statCards:
            _width += _card.totalWidth + 20
            if _height < _card.image.get_height() + 40:
                _height = _card.image.get_height() + 40

        _exp: pygame.Surface = pygame.Surface((_width + 40, _height + 40))
        _exp.fill('#313031')

        _x: int = 40
        for _card in self.statCards:
            for _comp in _card.components:
                _comp.noHover()
            _card.draw(_exp, [0, 0], _x)
            _x += _card.totalWidth + 20

        pygame.image.save(_exp, f'./exports/statSheet{self.file}.png')

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