from settings import *

from ui.button import Button
from ui.background import Background
from ui.switchButton import SwitchButton
from ui.textBox import TextBox


class AbilityUI(Background):
    def __init__(self, pos: list[int], parent: object):
        super().__init__(
            'AbilityUI',
            'Ability',
            [620, 345],
            pos
        )

        self.parent: object = parent

        self.lastClickEffect: list[TextBox] = None
        self.effectsList: list[list[TextBox]] = []

        self._makeEffectList()

        self.components.append(
            TextBox([(self.size[0] - 360), 80 + self.pos[1]], [300, 1], self.changeName)
        )
        self.components[0].text = parent.name

        self.components.append(
            TextBox([(self.size[0] - 360), 140 + self.pos[1]], [300, 2], self.changeTypes)
        )
        self.components[1].text = parent.types

        self.components.append(
            TextBox([450, 235 + self.pos[1]], [50, 1], self.changeEffect)
        )
        self.components[2].text = str(len(parent.effects))

        self.components.append(
            Button(
                [500, 235 + self.pos[1]],
                [30, 32],
                'assets/icons/AddButton.png',
                'assets/icons/AddButton_hover.png',
                self.addEffect
            )
        )
        self.components.append(
            Button(
                [530, 235 + self.pos[1]],
                [30, 32],
                'assets/icons/MinusButton.png',
                'assets/icons/MinusButton_hover.png',
                self.minusEffect
            )
        )

    def _makeEffectList(self):
        self.effectsList = []
        _y: int = 270
        for _name, _effect in self.parent.effects.items():

            _list: list[TextBox] = []
            _list.append(TextBox([self.size[0] - 390, _y + self.pos[1]], [300, 1], self.changeEffects))
            _list[0].text = _name

            _y += 35
            _list.append(TextBox([self.size[0] - 390, _y + self.pos[1]], [300, 3], self.changeEffects))
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

        self.size = [self.size[0], 345 + (140 * len(self.effectsList))]
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

        self.image.blit(self.font.render('Name', True, '#000000'), (25, 56))
        self.image.blit(self.font.render('Name', True, '#C2C2C2'), (25, 55))

        self.image.blit(self.font.render('Ability Name', True, '#000000'), (50, 81))
        self.image.blit(self.font.render('Ability Name', True, '#EEE1C5'), (50, 80))

        self.image.blit(self.font.render('Types', True, '#000000'), (25, 116))
        self.image.blit(self.font.render('Types', True, '#C2C2C2'), (25, 115))

        self.image.blit(self.font.render('Ability Types', True, '#000000'), (50, 141))
        self.image.blit(self.font.render('Ability Types', True, '#EEE1C5'), (50, 140))

        self.image.blit(self.font.render('Effects', True, '#000000'), (25, 201))
        self.image.blit(self.font.render('Effects', True, '#C2C2C2'), (25, 200))

        self.image.blit(self.font.render('Number of Effects', True, '#000000'), (50, 236))
        self.image.blit(self.font.render('Number of Effects', True, '#EEE1C5'), (50, 235))

        self.image.blit(self.font.render('Marker', True, '#000000'), (25, self.size[1] - 86))
        self.image.blit(self.font.render('Marker', True, '#C2C2C2'), (25, self.size[1] - 85))

        self.image.blit(self.font.render('Edit Marker', True, '#000000'), (50, self.size[1] - 61))
        self.image.blit(self.font.render('Edit Marker', True, '#EEE1C5'), (50, self.size[1] - 60))

        for _effect in self.effectsList:
            self.image.blit(self.font.render('Effect Name', True, '#000000'), (50, _effect[0].pos[1] - self.pos[1] + 1))
            self.image.blit(self.font.render('Effect Name', True, '#EEE1C5'), (50, _effect[0].pos[1] - self.pos[1]))

            self.image.blit(self.font.render('Effect Description', True, '#000000'), (50, _effect[1].pos[1] - self.pos[1] + 1))
            self.image.blit(self.font.render('Effect Description', True, '#EEE1C5'), (50, _effect[1].pos[1] - self.pos[1]))

        screen.blit(self.image, (self.pos[0] + right, self.pos[1] + scroll[1]))

        for _effect in self.effectsList:
            _effect[0].draw(screen, right, scroll)
            
            _effect[1].draw(screen, right, scroll)

            _effect[2].draw(screen, right, scroll)
            _effect[3].draw(screen, right, scroll)
            _effect[4].draw(screen, right, scroll)

        for _component in self.components:
            _component.draw(screen, right, scroll)

    def hover(self):
        for _effect in self.effectsList:
            for _comp in _effect:
                _comp.noHover()
                if _comp.rect.collidepoint(pygame.mouse.get_pos()):
                    _comp.hover()

    def onClick(self):
        print(self.lastClickEffect)
        for _effect in self.effectsList:
            for _comp in _effect:
                if hasattr(_comp, 'active'): 
                    _comp.active = False
                    _comp.exitField()
                    
                if _comp.rect.collidepoint(pygame.mouse.get_pos()):
                    self.lastClickEffect = _effect
                    _comp.onClick()

    def changeName(self):
        self.parent.name = self.components[0].text

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
        if _lastClickEffect[1].currentFormat == 1:
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
        if _lastClickEffect[1].currentFormat == 2:
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
        if _lastClickEffect[1].currentFormat == 3:
            _lastClickEffect[4].on = True
        else:
            _lastClickEffect[4].on = False

    def changeEffects(self):
        _newDict: dict[str, str] = {}
        for _effect in self.effectsList:
            _newDict[_effect[0].text] = _effect[1].text

        self.parent.effects = _newDict