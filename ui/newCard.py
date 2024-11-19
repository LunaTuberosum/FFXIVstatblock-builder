
from settings import *

from statCard import StatCard
from ui.background import Background
from ui.button import Button
from ui.switchButton import SwitchButton
from ui.textBox import TextBox
from ui.toggleButtons import ToggleButtons

from components.ability import AbilityComponent
from components.name import NameComponent
from components.sectionName import SectionNameComponent
from components.topStats import TopStatsComponent
from components.trait import TraitComponent


class NewCardUI(Background):
    def __init__(self, parent: object):
        super().__init__(
            'NewCardUI', 
            'New Card', 
            [500, 530], 
            [(SCREEN_WIDTH / 2) - 250, (SCREEN_HEIGHT / 2) - 200]
        )

        self.parent: object = parent

        self.tokenBool: bool = False

        self.components.append(
            ToggleButtons([self.size[0] - 315, 80 + self.pos[1]], [270, 25], {
                'Token': self.token,
                'Standered': self.standered
            },
            'Standered')
        )

        self.components.append(
            TextBox([(self.size[0] - 192), 140 + self.pos[1]], [90, 1], self.width)
        )
        self.components[1].text = '1'

        self.components.append(
            Button(
                [self.size[0] - 100, 140 + self.pos[1]],
                [30, 32],
                'assets/icons/AddButton.png',
                'assets/icons/AddButton_hover.png',
                self.widthAdd
            )
        )
        self.components.append(
            Button(
                [self.size[0] - 70, 140 + self.pos[1]],
                [30, 32],
                'assets/icons/MinusButton.png',
                'assets/icons/MinusButton_hover.png',
                self.widthMinus
            )
        )

        self.components.append(
            TextBox([(self.size[0] - 192), 175 + self.pos[1]], [90, 1], self.height)
        )
        self.components[4].text = '0'

        self.components.append(
            Button(
                [self.size[0] - 100, 175 + self.pos[1]],
                [30, 32],
                'assets/icons/AddButton.png',
                'assets/icons/AddButton_hover.png',
                self.heightAdd
            )
        )
        self.components.append(
            Button(
                [self.size[0] - 70, 175 + self.pos[1]],
                [30, 32],
                'assets/icons/MinusButton.png',
                'assets/icons/MinusButton_hover.png',
                self.heightMinus
            )
        )

        self.components.append(
            SwitchButton(
                [25, 212 + self.pos[1]],
                [20, 20],
                'assets/icons/ToggleButton.png',
                'assets/icons/ToggleButton_hover.png',
                self.blank,
                self.blank,
                self.blank,
                'assets/icons/ToggleButton_selected.png',
            )
        )

        self.components.append(
            TextBox([(self.size[0] - 192), 235 + self.pos[1]], [90, 1], self.trait)
        )
        self.components[8].text = '0'

        self.components.append(
            Button(
                [self.size[0] - 100, 235 + self.pos[1]],
                [30, 32],
                'assets/icons/AddButton.png',
                'assets/icons/AddButton_hover.png',
                self.traitAdd
            )
        )
        self.components.append(
            Button(
                [self.size[0] - 70, 235 + self.pos[1]],
                [30, 32],
                'assets/icons/MinusButton.png',
                'assets/icons/MinusButton_hover.png',
                self.traitMinus
            )
        )

        self.components.append(
            SwitchButton(
                [25, 262 + self.pos[1]],
                [20, 20],
                'assets/icons/ToggleButton.png',
                'assets/icons/ToggleButton_hover.png',
                self.blank,
                self.blank,
                self.blank,
                'assets/icons/ToggleButton_selected.png',
            )
        )

        self.components.append(
            TextBox([(self.size[0] - 192), 285 + self.pos[1]], [90, 1], self.ability)
        )
        self.components[12].text = '0'

        self.components.append(
            Button(
                [self.size[0] - 100, 285 + self.pos[1]],
                [30, 32],
                'assets/icons/AddButton.png',
                'assets/icons/AddButton_hover.png',
                self.abilityAdd
            )
        )
        self.components.append(
            Button(
                [self.size[0] - 70, 285 + self.pos[1]],
                [30, 32],
                'assets/icons/MinusButton.png',
                'assets/icons/MinusButton_hover.png',
                self.abilityMinus
            )
        )

        self.components.append(
            Button(
                [28, (self.size[1] - 70) + self.pos[1]],
                [198, 38],
                'assets/icons/button.png',
                'assets/icons/button_hover.png',
                self.create,
                'Create'
            )
        )

        self.components.append(
            Button(
                [self.size[0] - 228, (self.size[1] - 70) + self.pos[1]],
                [198, 38],
                'assets/icons/button.png',
                'assets/icons/button_hover.png',
                self.close,
                'Close'
            )
        )

    def draw(self, screen: pygame.Surface, right: int, scroll: list[int]):
        super().draw(screen, right, scroll)

        self.image.blit(self.font.render('Card Type', True, '#000000'), (25, 56))
        self.image.blit(self.font.render('Card Type', True, '#C2C2C2'), (25, 55))

        self.image.blit(self.font.render('Type', True, '#000000'), (50, 81))
        self.image.blit(self.font.render('Type', True, '#EEE1C5'), (50, 80))

        self.image.blit(self.font.render('Card Size', True, '#000000'), (25, 116))
        self.image.blit(self.font.render('Card Size', True, '#C2C2C2'), (25, 115))

        self.image.blit(self.font.render('Width', True, '#000000'), (50, 141))
        self.image.blit(self.font.render('Width', True, '#EEE1C5'), (50, 140))

        self.image.blit(self.font.render('Height', True, '#000000'), (50, 176))
        self.image.blit(self.font.render('Height', True, '#EEE1C5'), (50, 175))

        self.image.blit(self.font.render('Traits', True, '#000000'), (50, 211))
        self.image.blit(self.font.render('Traits', True, '#C2C2C2'), (50, 210))

        self.image.blit(self.font.render('Number of Traits', True, '#000000'), (75, 236))
        self.image.blit(self.font.render('Number of Traits', True, '#EEE1C5'), (75, 235))

        self.image.blit(self.font.render('Abilities', True, '#000000'), (50, 261))
        self.image.blit(self.font.render('Abilities', True, '#C2C2C2'), (50, 260))

        self.image.blit(self.font.render('Number of Abilities', True, '#000000'), (75, 286))
        self.image.blit(self.font.render('Number of Abilities', True, '#EEE1C5'), (75, 285))
    
        screen.blit(self.image, (self.pos[0] + right, self.pos[1] + scroll[1]))

        for _component in self.components:
            _component.draw(screen, self.rect.left, scroll)

    def token(self):
        self.tokenBool = True
    
    def standered(self):
        self.tokenBool = False

    def width(self):
        try:
            _i: int = int(self.components[1].text)
            if _i < 1: raise Exception

        except:
            self.components[1].text = '1'

    def widthAdd(self):
        try:
            _i: int = int(self.components[1].text) + 1
            self.components[1].text = str(_i)

        except:
            self.components[1].text = self.components[1].text

    def widthMinus(self):
        try:
            _i: int = int(self.components[1].text) - 1
            if _i < 1: 
                raise Exception
            self.components[1].text = str(_i)

        except:
            self.components[1].text = self.components[1].text

    def height(self):
        try:
            _i: int = int(self.components[4].text)
            if _i < 0: raise Exception

        except:
            self.components[4].text = '0'

    def heightAdd(self):
        try:
            _i: int = int(self.components[4].text) + 1
            self.components[4].text = str(_i)

        except:
            self.components[4].text = self.components[4].text

    def heightMinus(self):
        try:
            _i: int = int(self.components[4].text) - 1
            if _i < 0: 
                raise Exception
            self.components[4].text = str(_i)

        except:
            self.components[4].text = self.components[4].text

    def trait(self):
        try:
            _i: int = int(self.components[8].text)
            if _i < 0: raise Exception

        except:
            self.components[8].text = '0'

    def traitAdd(self):
        try:
            _i: int = int(self.components[8].text) + 1
            self.components[8].text = str(_i)

        except:
            self.components[8].text = self.components[8].text

    def traitMinus(self):
        try:
            _i: int = int(self.components[8].text) - 1
            if _i < 0: 
                raise Exception
            self.components[8].text = str(_i)

        except:
            self.components[8].text = self.components[8].text

    def ability(self):
        try:
            _i: int = int(self.components[12].text)
            if _i < 0: raise Exception

        except:
            self.components[12].text = '0'

    def abilityAdd(self):
        try:
            _i: int = int(self.components[12].text) + 1
            self.components[12].text = str(_i)

        except:
            self.components[12].text = self.components[12].text

    def abilityMinus(self):
        try:
            _i: int = int(self.components[12].text) - 1
            if _i < 0: 
                raise Exception
            self.components[12].text = str(_i)

        except:
            self.components[12].text = self.components[12].text

    def create(self):
        _card: StatCard = StatCard(self.parent.statCardBackground, int(self.components[1].text), int(self.components[4].text), self.parent)
        _card.addComponent(NameComponent(_card))

        _card.addComponent(TopStatsComponent(_card, self.tokenBool))

        if self.components[7].on:
            _card.addComponent(SectionNameComponent('Traits', 2, _card))

            for _trait in range(int(self.components[8].text)):
                _card.addComponent(TraitComponent(f'Trait {_trait + 1}', '', _card))

        if self.components[11].on:
            _card.addComponent(SectionNameComponent('Abilities', 2, _card))

            for _ability in range(int(self.components[12].text)):
                _card.addComponent(AbilityComponent(f'Ability {_ability + 1}', '', {}, _card))

        self.parent.statCards.add(
            _card
        )

        self.parent.window = None

    def close(self):
        self.parent.window = None

    def blank(self):
        pass