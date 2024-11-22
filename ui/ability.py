from components.marker import MarkerComponent
from settings import *

from ui.button import Button
from ui.background import Background
from ui.markerBuilder import MarkerBuilderUI
from ui.switchButton import SwitchButton
from ui.textBox import TextBox
from ui.toggleButtons import ToggleButtons


class AbilityUI(Background):
    def __init__(self, pos: list[int], parent: object):
        super().__init__(
            'AbilityUI',
            'Ability',
            [620, 395],
            pos
        )

        self.parent: object = parent

        self.window: MarkerBuilderUI = None

        self.lastClickEffect: list[TextBox] = None
        self.effectsList: list[list[TextBox]] = []

        self._makeEffectList()

        self.components.append(
            TextBox([(self.size[0] - 360), 80 + self.pos[1]], [300, 1], self.changeName)
        )
        self.components[0].text = parent.name

        self.components.append(
            ToggleButtons(
                [self.size[0] - 330, 140 + self.pos[1]], 
                [270, 25],
                {
                    'On': self.on,
                    'Off': self.off
                },
                'Off'
            )
        )
        self.components[1].buttonSelected = 'On' if self.parent.invk else 'Off'

        self.components.append(
            TextBox([(self.size[0] - 360), 190 + self.pos[1]], [300, 2], self.changeTypes)
        )
        self.components[2].text = parent.types

        self.components.append(
            TextBox([450, 285 + self.pos[1]], [50, 1], self.changeEffect)
        )
        self.components[3].text = str(len(parent.effects))

        self.components.append(
            Button(
                [500, 285 + self.pos[1]],
                [30, 32],
                'assets/icons/AddButton.png',
                'assets/icons/AddButton_hover.png',
                self.addEffect
            )
        )
        self.components.append(
            Button(
                [530, 285 + self.pos[1]],
                [30, 32],
                'assets/icons/MinusButton.png',
                'assets/icons/MinusButton_hover.png',
                self.minusEffect
            )
        )

        self.components.append(
            Button(
                [332, (self.size[1] - 65) + self.pos[1]],
                [198, 38],
                'assets/icons/button.png',
                'assets/icons/button_hover.png',
                self.makeMarker,
                'Marker Builder'
            )
        )

    def _makeEffectList(self):
        self.effectsList = []
        _y: int = 320
        for _name, _effect in self.parent.effects.items():

            _list: list[TextBox] = []
            _list.append(TextBox([self.size[0] - 390, _y + self.pos[1]], [300, 1], self.changeEffects))
            _list[0].text = _name

            _y += 35
            _list.append(TextBox([self.size[0] - 390, _y + self.pos[1]], [300, 3], self.changeEffects, True))
            _list[1].text = _effect

            _list.append(
                SwitchButton(
                    [self.size[0] - 90, _y - 5 + self.pos[1]],
                    [30, 32],
                    'assets/icons/BoldButton.png', 
                    'assets/icons/BoldButton_hover.png', 
                    self.addBold, 
                    self.removeBold,
                    self.updateBold
                )
            )
            _list.append(
                SwitchButton(
                    [self.size[0] -  90, _y + 27 + self.pos[1]],
                    [30, 32],
                    'assets/icons/ItalicButton.png', 
                    'assets/icons/ItalicButton_hover.png', 
                    self.addItalic, 
                    self.removeItalic,
                    self.updateItalic
                )
            )
            _list.append(
                SwitchButton(
                    [self.size[0] -  90, _y + 59 + self.pos[1]],
                    [30, 32],
                    'assets/icons/AbilityButton.png', 
                    'assets/icons/AbilityButton_hover.png', 
                    self.addAbility, 
                    self.removeAbility,
                    self.updateAbility
                )
            )

            _y += 105
            self.effectsList.append(_list)

        self.size = [self.size[0], 395 + (140 * len(self.effectsList))]
        self.image = pygame.Surface(self.size)

    def draw(self, screen: pygame.Surface, right: int, scroll: list[int]):
        for _component in self.components:
            if hasattr(_component, 'commandUpdate'):
                _component.update()

        for _effect in self.effectsList:
            for _component in _effect:
                if hasattr(_component, 'commandUpdate'):
                    _component.commandUpdate(_effect)

        super().draw(screen, right, scroll)

        if self.window:
            self.window.draw(screen, self.rect.right, scroll)

        self.image.blit(self.font.render('Name', True, '#000000'), (25, 56))
        self.image.blit(self.font.render('Name', True, '#C2C2C2'), (25, 55))

        self.image.blit(self.font.render('Ability Name', True, '#000000'), (50, 81))
        self.image.blit(self.font.render('Ability Name', True, '#EEE1C5'), (50, 80))

        self.image.blit(self.font.render('Invoked', True, '#000000'), (25, 116))
        self.image.blit(self.font.render('Invoked', True, '#C2C2C2'), (25, 115))

        self.image.blit(self.font.render('Is Invoked', True, '#000000'), (50, 141))
        self.image.blit(self.font.render('Is Invoked', True, '#EEE1C5'), (50, 140))

        self.image.blit(self.font.render('Types', True, '#000000'), (25, 166))
        self.image.blit(self.font.render('Types', True, '#C2C2C2'), (25, 165))

        self.image.blit(self.font.render('Ability Types', True, '#000000'), (50, 191))
        self.image.blit(self.font.render('Ability Types', True, '#EEE1C5'), (50, 190))

        self.image.blit(self.font.render('Effects', True, '#000000'), (25, 251))
        self.image.blit(self.font.render('Effects', True, '#C2C2C2'), (25, 250))

        self.image.blit(self.font.render('Number of Effects', True, '#000000'), (50, 286))
        self.image.blit(self.font.render('Number of Effects', True, '#EEE1C5'), (50, 285))

        for _effect in self.effectsList:
            self.image.blit(self.font.render('Effect Name', True, '#000000'), (50, _effect[0].pos[1] - self.pos[1] + 1))
            self.image.blit(self.font.render('Effect Name', True, '#EEE1C5'), (50, _effect[0].pos[1] - self.pos[1]))

            self.image.blit(self.font.render('Effect Description', True, '#000000'), (50, _effect[1].pos[1] - self.pos[1] + 1))
            self.image.blit(self.font.render('Effect Description', True, '#EEE1C5'), (50, _effect[1].pos[1] - self.pos[1]))

        self.image.blit(self.font.render('Marker', True, '#000000'), (25, self.size[1] - 86))
        self.image.blit(self.font.render('Marker', True, '#C2C2C2'), (25, self.size[1] - 85))

        self.image.blit(self.font.render('Edit Marker', True, '#000000'), (50, self.size[1] - 61))
        self.image.blit(self.font.render('Edit Marker', True, '#EEE1C5'), (50, self.size[1] - 60))

        screen.blit(self.image, (self.pos[0] + right, self.pos[1] + scroll[1]))

        for _effect in self.effectsList:
            _effect[0].draw(screen, right, scroll)
            
            _effect[1].draw(screen, right, scroll)

            _effect[2].draw(screen, right, scroll)
            _effect[3].draw(screen, right, scroll)
            _effect[4].draw(screen, right, scroll)

        self.components[-1].pos[1] = self.size[1] - 65 + self.pos[1]

        for _component in self.components:
            _component.draw(screen, right, scroll)

    def hover(self):
        for _effect in self.effectsList:
            for _comp in _effect:
                _comp.noHover()
                if _comp.rect.collidepoint(pygame.mouse.get_pos()):
                    _comp.hover()

    def onClick(self):
        for _effect in self.effectsList:
            for _comp in _effect:
                if hasattr(_comp, 'active'): 
                    if _comp.active:
                        _comp.exitField()
                    _comp.active = False
                    
                if _comp.rect.collidepoint(pygame.mouse.get_pos()):
                    self.lastClickEffect = _effect
                    _comp.onClick()

    def changeName(self):
        self.parent.name = self.components[0].text

    def on(self):
        self.parent.invk = True

    def off(self):
        self.parent.invk = False

    def changeTypes(self):
        self.parent.types = self.components[1].text

    def changeEffect(self):
        try:
            _newDict: dict[str, str] = {}
            for _ef in range(int(self.components[2].text)):
                if _ef > len(self.effectsList) - 1:
                    _newDict[f'Effect {_ef + 1}:'] = ''
                    continue
                _newDict[self.effectsList[_ef][0].text] = self.effectsList[_ef][1].text 
            self.parent.effects = _newDict
            self._makeEffectList()
        except:
            self.components[2].text = str(len(self.parent.effects))
            return

    def addEffect(self):
        try:
            self.parent.effects[f'Effect {len(self.parent.effects)}:'] = ''
            self.components[2].text = str(len(self.parent.effects))
            self._makeEffectList()

        except:
            self.components[2].text = str(len(self.parent.effects))
            return

    def minusEffect(self):
        try:
            _els = list(self.parent.effects.items())
            _last = _els[-1]
            self.parent.effects.pop(_last[0])
            self.components[2].text = str(len(self.parent.effects))
            self._makeEffectList()

        except:
            self.components[2].text = str(len(self.parent.effects))
            return

    def addBold(self):
        self.lastClickEffect[1].text += ' {b} '
        self.lastClickEffect[1].active = True

    def removeBold(self):
        self.lastClickEffect[1].text += ' {/b} '
        self.lastClickEffect[1].active = True

    def updateBold(self, _lastClickEffect: list[TextBox]):
        if _lastClickEffect[1].currentFormat['bold']:
            _lastClickEffect[2].on = True
        else:
            _lastClickEffect[2].on = False

    def addItalic(self):
        self.lastClickEffect[1].text += ' {i} '
        self.lastClickEffect[1].active = True

    def removeItalic(self):
        self.lastClickEffect[1].text += ' {/i} '
        self.lastClickEffect[1].active = True

    def updateItalic(self, _lastClickEffect: list[TextBox]):
        if _lastClickEffect[1].currentFormat['italic']:
            _lastClickEffect[3].on = True
        else:
            _lastClickEffect[3].on = False

    def addAbility(self):
        self.lastClickEffect[1].text += ' {a} '
        self.lastClickEffect[1].active = True

    def removeAbility(self):
        self.lastClickEffect[1].text += ' {/a} '
        self.lastClickEffect[1].active = True

    def updateAbility(self, _lastClickEffect: list[TextBox]):
        if _lastClickEffect[1].currentFormat['red']:
            _lastClickEffect[4].on = True
        else:
            _lastClickEffect[4].on = False

    def changeEffects(self):
        _newDict: dict[str, str] = {}
        for _effect in self.effectsList:
            _newDict[_effect[0].text] = _effect[1].text

        self.parent.effects = _newDict

    def makeMarker(self):
        if self.window:
            self.window = None
            return
        if not self.parent.marker:
            _marker: list[list[int]] = [
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
            ]
            self.parent.marker = MarkerComponent(len(_marker[0]), len(_marker), _marker, self.parent.width(), self.parent)
        self.window = MarkerBuilderUI([self.pos[0] - 15, self.pos[1] + 20], self)