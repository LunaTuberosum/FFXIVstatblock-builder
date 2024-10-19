from settings import *

from ui.background import Background
from ui.button import Button
from ui.textBox import TextBox
from ui.toggleButtons import ToggleButtons


class TopStatsUI(Background):
    def __init__(self, pos: list[int], parent: object):
        super().__init__(
            'TopStatsUI',
            'Attributes',
            [730, 370],
            pos
        )

        self.parent: object = parent

        self.components.append(
            TextBox([130, 80 + self.pos[1]], [140, 1], 0, self.changeSize)
        )
        self.components[0].text = parent.creatureSize

        self.components.append(
            TextBox([520, 80 + self.pos[1]], [150, 1], 0, self.changeSpecies)
        )
        self.components[1].text = parent.species

        self.components.append(
            TextBox([140, 120 + self.pos[1]], [70, 1], 0, self.changeDefense)
        )
        self.components[2].text = parent.defense

        self.components.append(
            Button(
                [210, 120 + self.pos[1]],
                [30, 32],
                'assets/icons/AddButton.png',
                'assets/icons/AddButton_hover.png',
                self.addDefense
            )
        )
        self.components.append(
            Button(
                [240, 120 + self.pos[1]],
                [30, 32],
                'assets/icons/MinusButton.png',
                'assets/icons/MinusButton_hover.png',
                self.minusDefense
            )
        )

        self.components.append(
            TextBox([540, 120 + self.pos[1]], [70, 1], 0, self.changeMagicDefense)
        )
        self.components[5].text = parent.magicDefense

        self.components.append(
            Button(
                [610, 120 + self.pos[1]],
                [30, 32],
                'assets/icons/AddButton.png',
                'assets/icons/AddButton_hover.png',
                self.addMagicDefense
            )
        )
        self.components.append(
            Button(
                [640, 120 + self.pos[1]],
                [30, 32],
                'assets/icons/MinusButton.png',
                'assets/icons/MinusButton_hover.png',
                self.minusMagicDefense
            )
        )

        self.components.append(
            TextBox([130, 160 + self.pos[1]], [80, 1], 0, self.changeMaxHP)
        )
        self.components[8].text = parent.maxHP

        self.components.append(
            Button(
                [210, 160 + self.pos[1]],
                [30, 32],
                'assets/icons/AddButton.png',
                'assets/icons/AddButton_hover.png',
                self.addMaxHP
            )
        )
        self.components.append(
            Button(
                [240, 160 + self.pos[1]],
                [30, 32],
                'assets/icons/MinusButton.png',
                'assets/icons/MinusButton_hover.png',
                self.minusMaxHP
            )
        )

        self.components.append(
            TextBox([540, 160 + self.pos[1]], [70, 1], 0, self.changeSpeed)
        )
        self.components[11].text = parent.speed

        self.components.append(
            Button(
                [610, 160 + self.pos[1]],
                [30, 32],
                'assets/icons/AddButton.png',
                'assets/icons/AddButton_hover.png',
                self.addSpeed
            )
        )
        self.components.append(
            Button(
                [640, 160 + self.pos[1]],
                [30, 32],
                'assets/icons/MinusButton.png',
                'assets/icons/MinusButton_hover.png',
                self.minusSpeed
            )
        )

        self.components.append(
            TextBox([140, 200 + self.pos[1]], [70, 1], 0, self.changeVigilance)
        )
        self.components[14].text = parent.vigilance

        self.components.append(
            Button(
                [210, 200 + self.pos[1]],
                [30, 32],
                'assets/icons/AddButton.png',
                'assets/icons/AddButton_hover.png',
                self.addVigilance
            )
        )
        self.components.append(
            Button(
                [240, 200 + self.pos[1]],
                [30, 32],
                'assets/icons/MinusButton.png',
                'assets/icons/MinusButton_hover.png',
                self.minusVigilance
            )
        )

        ##

        self.components.append(
            TextBox([40, 300 + self.pos[1]], [50, 1], 0, self.changeSTR)
        )
        self.components[17].text = parent.str

        self.components.append(
            Button(
                [90, 300 + self.pos[1]],
                [30, 32],
                'assets/icons/AddButton.png',
                'assets/icons/AddButton_hover.png',
                self.addSTR
            )
        )
        self.components.append(
            Button(
                [120, 300 + self.pos[1]],
                [30, 32],
                'assets/icons/MinusButton.png',
                'assets/icons/MinusButton_hover.png',
                self.minusSTR
            )
        )

        self.components.append(
            TextBox([170, 300 + self.pos[1]], [50, 1], 0, self.changeDEX)
        )
        self.components[20].text = parent.dex

        self.components.append(
            Button(
                [220, 300 + self.pos[1]],
                [30, 32],
                'assets/icons/AddButton.png',
                'assets/icons/AddButton_hover.png',
                self.addDEX
            )
        )
        self.components.append(
            Button(
                [250, 300 + self.pos[1]],
                [30, 32],
                'assets/icons/MinusButton.png',
                'assets/icons/MinusButton_hover.png',
                self.minusDEX
            )
        )

        self.components.append(
            TextBox([300, 300 + self.pos[1]], [50, 1], 0, self.changeVIT)
        )
        self.components[23].text = parent.vit

        self.components.append(
            Button(
                [350, 300 + self.pos[1]],
                [30, 32],
                'assets/icons/AddButton.png',
                'assets/icons/AddButton_hover.png',
                self.addVIT
            )
        )
        self.components.append(
            Button(
                [380, 300 + self.pos[1]],
                [30, 32],
                'assets/icons/MinusButton.png',
                'assets/icons/MinusButton_hover.png',
                self.minusVIT
            )
        )

        self.components.append(
            TextBox([430, 300 + self.pos[1]], [50, 1], 0, self.changeINT)
        )
        self.components[26].text = parent.int

        self.components.append(
            Button(
                [480, 300 + self.pos[1]],
                [30, 32],
                'assets/icons/AddButton.png',
                'assets/icons/AddButton_hover.png',
                self.addINT
            )
        )
        self.components.append(
            Button(
                [510, 300 + self.pos[1]],
                [30, 32],
                'assets/icons/MinusButton.png',
                'assets/icons/MinusButton_hover.png',
                self.minusINT
            )
        )

        self.components.append(
            TextBox([560, 300 + self.pos[1]], [50, 1], 0, self.changeMND)
        )
        self.components[29].text = parent.mnd

        self.components.append(
            Button(
                [610, 300 + self.pos[1]],
                [30, 32],
                'assets/icons/AddButton.png',
                'assets/icons/AddButton_hover.png',
                self.addMND
            )
        )
        self.components.append(
            Button(
                [640, 300 + self.pos[1]],
                [30, 32],
                'assets/icons/MinusButton.png',
                'assets/icons/MinusButton_hover.png',
                self.minusMND
            )
        )


    def draw(self, screen: pygame.Surface, right: int):
        super().draw(screen, right)

        self.image.blit(self.font.render('Secondary Attributes', True, '#000000'), (25, 56))
        self.image.blit(self.font.render('Secondary Attributes', True, '#C2C2C2'), (25, 55))

        self.image.blit(self.font.render('Size', True, '#000000'), (50, 81))
        self.image.blit(self.font.render('Size', True, '#EEE1C5'), (50, 80))

        self.image.blit(self.font.render('Species', True, '#000000'), (350, 81))
        self.image.blit(self.font.render('Species', True, '#EEE1C5'), (350, 80))

        self.image.blit(self.font.render('Defense', True, '#000000'), (50, 121))
        self.image.blit(self.font.render('Defense', True, '#EEE1C5'), (50, 120))

        self.image.blit(self.font.render('Magic Defense', True, '#000000'), (350, 121))
        self.image.blit(self.font.render('Magic Defense', True, '#EEE1C5'), (350, 120))

        self.image.blit(self.font.render('Max HP', True, '#000000'), (50, 161))
        self.image.blit(self.font.render('Max HP', True, '#EEE1C5'), (50, 160))

        self.image.blit(self.font.render('Speed', True, '#000000'), (350, 161))
        self.image.blit(self.font.render('Speed', True, '#EEE1C5'), (350, 160))

        self.image.blit(self.font.render('Vigilance', True, '#000000'), (50, 201))
        self.image.blit(self.font.render('Vigilance', True, '#EEE1C5'), (50, 200))

        ##

        self.image.blit(self.font.render('Primary Attributes', True, '#000000'), (25, 246))
        self.image.blit(self.font.render('Primary Attributes', True, '#C2C2C2'), (25, 245))

        self.image.blit(self.font.render('STR', True, '#000000'), (105 - (self.font.size('STR')[0] / 2), 271))
        self.image.blit(self.font.render('STR', True, '#EEE1C5'), (105 - (self.font.size('STR')[0] / 2), 270))

        self.image.blit(self.font.render('DEX', True, '#000000'), (235 - (self.font.size('DEX')[0] / 2), 271))
        self.image.blit(self.font.render('DEX', True, '#EEE1C5'), (235 - (self.font.size('DEX')[0] / 2), 270))

        self.image.blit(self.font.render('VIT', True, '#000000'), (365 - (self.font.size('VIT')[0] / 2), 271))
        self.image.blit(self.font.render('VIT', True, '#EEE1C5'), (365 - (self.font.size('VIT')[0] / 2), 270))

        self.image.blit(self.font.render('INT', True, '#000000'), (495 - (self.font.size('INT')[0] / 2), 271))
        self.image.blit(self.font.render('INT', True, '#EEE1C5'), (495 - (self.font.size('INT')[0] / 2), 270))

        self.image.blit(self.font.render('MND', True, '#000000'), (625 - (self.font.size('MND')[0] / 2), 271))
        self.image.blit(self.font.render('MND', True, '#EEE1C5'), (625 - (self.font.size('MND')[0] / 2), 270))

        screen.blit(self.image, (self.pos[0] + right, self.pos[1]))

        for _component in self.components:
            _component.draw(screen, right)

    def changeSize(self):
        self.parent.creatureSize = self.components[0].text

    def changeSpecies(self):
        self.parent.species = self.components[1].text

    def changeDefense(self):
        self.parent.defense = self.components[2].text

    def addDefense(self):
        if not self.parent.defense.isnumeric():
            return
        self.parent.defense = str(int(self.parent.defense) + 1)
        self.components[2].text = self.parent.defense

    def minusDefense(self):
        if not self.parent.defense.isnumeric():
            return
        self.parent.defense = str(int(self.parent.defense) - 1) if int(self.parent.defense) - 1 > 1 else str(1)
        self.components[2].text = self.parent.defense

    def changeMagicDefense(self):
        self.parent.magicDefense = self.components[5].text

    def addMagicDefense(self):
        if not self.parent.magicDefense.isnumeric():
            return
        self.parent.magicDefense = str(int(self.parent.magicDefense) + 1)
        self.components[5].text = self.parent.magicDefense

    def minusMagicDefense(self):
        if not self.parent.magicDefense.isnumeric():
            return
        self.parent.magicDefense = str(int(self.parent.magicDefense) - 1) if int(self.parent.magicDefense) - 1 > 1 else str(1)
        self.components[5].text = self.parent.magicDefense

    def changeMaxHP(self):
        self.parent.maxHP = self.components[8].text

    def addMaxHP(self):
        if not self.parent.maxHP.isnumeric():
            return
        self.parent.maxHP = str(int(self.parent.maxHP) + 5)
        self.components[8].text = self.parent.maxHP

    def minusMaxHP(self):
        if not self.parent.maxHP.isnumeric():
            return
        self.parent.maxHP = str(int(self.parent.maxHP) - 5) if int(self.parent.maxHP) - 5> 5 else str(5)
        self.components[8].text = self.parent.maxHP

    def changeSpeed(self):
        self.parent.speed = self.components[11].text

    def addSpeed(self):
        if not self.parent.speed.isnumeric():
            return
        self.parent.speed = str(int(self.parent.speed) + 1)
        self.components[11].text = self.parent.speed

    def minusSpeed(self):
        if not self.parent.speed.isnumeric():
            return
        self.parent.speed = str(int(self.parent.speed) - 1) if int(self.parent.speed) - 1 > 0 else str(0)
        self.components[11].text = self.parent.speed

    def changeVigilance(self):
        self.parent.vigilance = self.components[14].text

    def addVigilance(self):
        if not self.parent.vigilance.isnumeric():
            return
        self.parent.vigilance = str(int(self.parent.vigilance) + 1)
        self.components[14].text = self.parent.vigilance

    def minusVigilance(self):
        if not self.parent.vigilance.isnumeric():
            return
        self.parent.vigilance = str(int(self.parent.vigilance) - 1) if int(self.parent.vigilance) - 1 > 0 else str(0)
        self.components[14].text = self.parent.vigilance

    ##

    def changeSTR(self):
        try:
            int(self.compoonents[17].text)
            self.parent.str = self.components[17].text
        except:
            self.components[17].text = self.parent.str
            return

    def addSTR(self):
        try:
            self.parent.str = str(int(self.parent.str) + 1)
            self.components[17].text = self.parent.str
        except:
            self.components[17].text = self.parent.str
            return

    def minusSTR(self):
        try:
            self.parent.str = str(int(self.parent.str) - 1)
            self.components[17].text = self.parent.str
        except:
            self.components[17].text = self.parent.str
            return

    def changeDEX(self):
        try:
            int(self.compoonents[20].text)
            self.parent.dex = self.components[20].text
        except:
            self.components[20].text = self.parent.dex
            return

    def addDEX(self):
        try:
            self.parent.dex = str(int(self.parent.dex) + 1)
            self.components[20].text = self.parent.dex
        except:
            self.components[20].text = self.parent.dex
            return

    def minusDEX(self):
        try:
            self.parent.dex = str(int(self.parent.dex) - 1)
            self.components[20].text = self.parent.dex
        except:
            self.components[20].text = self.parent.dex
            return

    def changeVIT(self):
        try:
            int(self.compoonents[23].text)
            self.parent.vit = self.components[23].text
        except:
            self.components[23].text = self.parent.vit
            return

    def addVIT(self):
        try:
            self.parent.vit = str(int(self.parent.vit) + 1)
            self.components[23].text = self.parent.vit
        except:
            self.components[23].text = self.parent.vit
            return

    def minusVIT(self):
        try:
            self.parent.vit = str(int(self.parent.vit) - 1)
            self.components[23].text = self.parent.vit
        except:
            self.components[23].text = self.parent.vit
            return

    def changeINT(self):
        try:
            int(self.compoonents[26].text)
            self.parent.int = self.components[26].text
        except:
            self.components[26].text = self.parent.int
            return

    def addINT(self):
        try:
            self.parent.int = str(int(self.parent.int) + 1)
            self.components[26].text = self.parent.int
        except:
            self.components[26].text = self.parent.int
            return

    def minusINT(self):
        try:
            self.parent.int = str(int(self.parent.int) - 1)
            self.components[26].text = self.parent.int
        except:
            self.components[26].text = self.parent.int
            return

    def changeMND(self):
        try:
            int(self.compoonents[29].text)
            self.parent.mnd = self.components[29].text
        except:
            self.components[29].text = self.parent.mnd
            return

    def addMND(self):
        try:
            self.parent.mnd = str(int(self.parent.mnd) + 1)
            self.components[29].text = self.parent.mnd
        except:
            self.components[29].text = self.parent.mnd
            return

    def minusMND(self):
        try:
            self.parent.mnd = str(int(self.parent.mnd) - 1)
            self.components[29].text = self.parent.mnd
        except:
            self.components[29].text = self.parent.mnd
            return
