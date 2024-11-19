from settings import *

from ui.switchButton import SwitchButton
from ui.background import Background
from ui.textBox import TextBox


class TraitUI(Background):
    def __init__(self, pos: list[int], parent: object):
        super().__init__(
            'TraitUI',
            'Trait',
            [580, 330],
            pos
        )

        self.parent: object = parent

        self.components.append(
            TextBox([(self.size[0] - 360), 80 + self.pos[1]], [300, 1], self.changeName)
        )
        self.components[0].text = parent.name

        self.components.append(
            TextBox([40, 140 + self.pos[1]], [450, 5], self.changeDesc, True)
        )
        self.components[1].text = parent.desc

        self.components.append(
            SwitchButton(
                [490, 140 + self.pos[1]], 
                [30, 31], 
                'assets/icons/BoldButton.png', 
                'assets/icons/BoldButton_hover.png', 
                self.addBold, 
                self.removeBold,
                self.updateBold
                )
        )

        self.components.append(
            SwitchButton(
                [490, 171 + self.pos[1]], 
                [30, 31], 
                'assets/icons/ItalicButton.png', 
                'assets/icons/ItalicButton_hover.png', 
                self.addItalic, 
                self.removeItalic,
                self.updateItalic
                )
        )

        self.components.append(
            SwitchButton(
                [490, 202 + self.pos[1]], 
                [30, 31], 
                'assets/icons/AbilityButton.png', 
                'assets/icons/AbilityButton_hover.png', 
                self.addAbility, 
                self.removeAbility,
                self.updateAbility
                )
        )

    def draw(self, screen: pygame.Surface, right: int, scroll: list[int]):
        for _component in self.components:
            if hasattr(_component, 'commandUpdate'):
                _component.update()
        super().draw(screen, right, scroll)

        self.image.blit(self.font.render('Name', True, '#000000'), (25, 56))
        self.image.blit(self.font.render('Name', True, '#C2C2C2'), (25, 55))

        self.image.blit(self.font.render('Trait Name', True, '#000000'), (50, 81))
        self.image.blit(self.font.render('Trait Name', True, '#EEE1C5'), (50, 80))

        self.image.blit(self.font.render('Description', True, '#000000'), (25, 116))
        self.image.blit(self.font.render('Description', True, '#C2C2C2'), (25, 115))

        screen.blit(self.image, (self.pos[0] + right, self.pos[1] + scroll[1]))

        for _component in self.components:
            _component.draw(screen, right, scroll)

    def changeName(self):
        self.parent.name = self.components[0].text

    def changeDesc(self):
        self.parent.desc = self.components[1].text

    def addBold(self):
        self.components[1].text += ' {b} '
        self.components[1].active = True

    def removeBold(self):
        self.components[1].text += ' {/b} '
        self.components[1].active = True

    def updateBold(self):
        if self.components[1].currentFormat['bold']:
            self.components[2].on = True
        else:
            self.components[2].on = False

    def addItalic(self):
        self.components[1].text += ' {i} '
        self.components[1].active = True

    def removeItalic(self):
        self.components[1].text += ' {/i} '
        self.components[1].active = True

    def updateItalic(self):
        if self.components[1].currentFormat['italic']:
            self.components[3].on = True
        else:
            self.components[3].on = False

    def addAbility(self):
        self.components[1].text += ' {a} '
        self.components[1].active = True

    def removeAbility(self):
        self.components[1].text += ' {/a} '
        self.components[1].active = True

    def updateAbility(self):
        if self.components[1].currentFormat['red']:
            self.components[4].on = True
        else:
            self.components[4].on = False

