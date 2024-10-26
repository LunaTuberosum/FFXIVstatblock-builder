from settings import *

from ui.background import Background
from ui.button import Button
from ui.textBox import TextBox
from ui.toggleButtons import ToggleButtons


class NameUI(Background):
    def __init__(self, pos: list[int], parent: object):
        super().__init__(
            'NameUI',
            'Name',
            [550, 240],
            pos
        )

        self.parent: object = parent

        self.components.append(
            TextBox([(self.size[0] - 330), 80 + self.pos[1]], [270, 1], self.changeName)
        )
        self.components[0].text = parent.name

        self.components.append(
            TextBox([(self.size[0] - 212), 140 + self.pos[1]], [90, 1], self.changeLevel)
        )
        self.components[1].text = parent.level

        self.components.append(
            Button(
                [self.size[0] - 120, 140 + self.pos[1]],
                [30, 32],
                'assets/icons/AddButton.png',
                'assets/icons/AddButton_hover.png',
                self.addLevel
            )
        )
        self.components.append(
            Button(
                [self.size[0] - 90, 140 + self.pos[1]],
                [30, 32],
                'assets/icons/MinusButton.png',
                'assets/icons/MinusButton_hover.png',
                self.minusLevel
            )
        )

        self.components.append(
            ToggleButtons([self.size[0] - 330, 175 + self.pos[1]], [270, 25], {
                'Top Right': self.changePostionTopRight,
                'End': self.changePostionEnd
            },
            'End')
        )

    def draw(self, screen: pygame.Surface, right: int, scroll: list[int]):
        super().draw(screen, right, scroll)

        self.image.blit(self.font.render('Name', True, '#000000'), (25, 56))
        self.image.blit(self.font.render('Name', True, '#C2C2C2'), (25, 55))

        self.image.blit(self.font.render('Character Name', True, '#000000'), (50, 81))
        self.image.blit(self.font.render('Character Name', True, '#EEE1C5'), (50, 80))

        self.image.blit(self.font.render('Level', True, '#000000'), (25, 116))
        self.image.blit(self.font.render('Level', True, '#C2C2C2'), (25, 115))

        self.image.blit(self.font.render('Character Level', True, '#000000'), (50, 141))
        self.image.blit(self.font.render('Character Level', True, '#EEE1C5'), (50, 140))

        self.image.blit(self.font.render('Level Position', True, '#000000'), (50, 176))
        self.image.blit(self.font.render('Level Position', True, '#EEE1C5'), (50, 175))

        screen.blit(self.image, (self.pos[0] + right, self.pos[1] + scroll[1]))

        for _component in self.components:
            _component.draw(screen, right, scroll)

    def changeName(self):
        self.parent.name = self.components[0].text

    def changeLevel(self):
        try:
            int(self.components[1].text)
            self.parent.level = self.components[1].text
        except:
            self.components[1].text = self.parent.level
            return

    def addLevel(self):
        try:
            self.parent.level = str(int(self.parent.level) + 10)
            self.components[1].text = self.parent.level
        except:
            self.components[1].text = self.parent.level
            return

    def minusLevel(self):
        try:
            self.parent.level = str(int(self.parent.level) - 10) if int(self.parent.level) - 10 > 10 else str(10)
            self.components[1].text = self.parent.level
        except:
            self.components[1].text = self.parent.level
            return

    def changePostionEnd(self):
        self.parent.levelPositon = False
    
    def changePostionTopRight(self):
        self.parent.levelPositon = True