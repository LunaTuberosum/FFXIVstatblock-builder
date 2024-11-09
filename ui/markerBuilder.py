from settings import *
from ui.background import Background
from ui.button import Button
from ui.marker import MarkerUI
from ui.switchButton import SwitchButton
from ui.textBox import TextBox
from ui.toggleButtons import ToggleButtons


class MarkerBuilderUI(Background):
    def __init__(self, pos: list[int], parent: object):
        super().__init__(
            'MarkerBuilderUI',
            'Marker',
            [650, 800],
            pos
        )
        self.parent: Background = parent

        self.components.append(
            TextBox([(self.size[0] - 227), 80 + self.pos[1]], [90, 1], self.changeWidth)
        )
        self.components[0].text = str(parent.parent.marker.gridSize[0])

        self.components.append(
            Button(
                [self.size[0] - 135, 80 + self.pos[1]],
                [30, 32],
                'assets/icons/AddButton.png',
                'assets/icons/AddButton_hover.png',
                self.addWidth
            )
        )
        self.components.append(
            Button(
                [self.size[0] - 105, 80 + self.pos[1]],
                [30, 32],
                'assets/icons/MinusButton.png',
                'assets/icons/MinusButton_hover.png',
                self.minusWidth
            )
        )

        self.components.append(
            TextBox([(self.size[0] - 227), 115 + self.pos[1]], [90, 1], self.changeHeight)
        )
        self.components[3].text = str(parent.parent.marker.gridSize[1])

        self.components.append(
            Button(
                [self.size[0] - 135, 115 + self.pos[1]],
                [30, 32],
                'assets/icons/AddButton.png',
                'assets/icons/AddButton_hover.png',
                self.addHeight
            )
        )
        self.components.append(
            Button(
                [self.size[0] - 105, 115 + self.pos[1]],
                [30, 32],
                'assets/icons/MinusButton.png',
                'assets/icons/MinusButton_hover.png',
                self.minusHeight
            )
        )

        self.components.append(
            ToggleButtons([15, 180 + self.pos[1]], [555, 25], {
                'Proximity': self.changeProximity,
                'Stack': self.changeStack,
                'Mobile': self.changeMobile,
                'Stationary': self.changeStationary
            },
            'Stationary')
        )
        _list: list = list(self.components[6].buttons.items())
        self.components[6].buttonSelected = _list[self.parent.parent.marker.type][0]

        self.components.append(
            SwitchButton(
                [20, 225 + self.pos[1]],
                [30, 32],
                'assets/icons/GridButton.png',
                'assets/icons/GridButton_hover.png',
                self.paintGrid,
                self.blank,
                self.blank
            )
        )
        self.components[7].on = True

        self.components.append(
            SwitchButton(
                [60, 225 + self.pos[1]],
                [30, 32],
                'assets/icons/MarkerButton.png',
                'assets/icons/MarkerButton_hover.png',
                self.paintMarker,
                self.blank,
                self.blank
            )
        )
        self.markerButtonImage: list[pygame.Surface] = [
            pygame.image.load('assets/icons/MarkerButton.png').convert_alpha(),
            pygame.image.load('assets/icons/MarkerButton_hover.png').convert_alpha()
        ]
        self.markerDisabledButtonImage: list[pygame.Surface] = [
            pygame.image.load('assets/icons/MarkerDisabledButton.png').convert_alpha(),
            pygame.image.load('assets/icons/MarkerDisabledButton_hover.png').convert_alpha()
        ]

        self.components.append(
            SwitchButton(
                [100, 225 + self.pos[1]],
                [30, 32],
                'assets/icons/OriginButton.png',
                'assets/icons/OriginButton_hover.png',
                self.paintOrigin,
                self.blank,
                self.blank
            )
        )
        self.orignButtonImage: list[pygame.Surface] = [
            pygame.image.load('assets/icons/OriginButton.png').convert_alpha(),
            pygame.image.load('assets/icons/OriginButton_hover.png').convert_alpha()
        ]
        self.orignOutlineButtonImage: list[pygame.Surface] = [
            pygame.image.load('assets/icons/OriginOutlineButton.png').convert_alpha(),
            pygame.image.load('assets/icons/OriginOutlineButton_hover.png').convert_alpha()
        ]
        self.orignOutlineStakeButtonImage: list[pygame.Surface] = [
            pygame.image.load('assets/icons/OriginOutlineStakeButton.png').convert_alpha(),
            pygame.image.load('assets/icons/OriginOutlineStakeButton_hover.png').convert_alpha()
        ]

        self.components.append(
            SwitchButton(
                [140, 225 + self.pos[1]],
                [30, 32],
                'assets/icons/TankButton.png',
                'assets/icons/TankButton_hover.png',
                self.paintTank,
                self.blank,
                self.blank
            )
        )

        self.components.append(
            SwitchButton(
                [180, 225 + self.pos[1]],
                [30, 32],
                'assets/icons/HealerButton.png',
                'assets/icons/HealerButton_hover.png',
                self.paintHealer,
                self.blank,
                self.blank
            )
        )

        self.components.append(
            SwitchButton(
                [220, 225 + self.pos[1]],
                [30, 32],
                'assets/icons/DPSButton.png',
                'assets/icons/DPSButton_hover.png',
                self.paintDPS,
                self.blank,
                self.blank
            )
        )

        self.components.append(
            MarkerUI(
                [20, 272 + self.pos[1]],
                self.parent.parent.marker
            )
        )

        if self.components[6].buttonSelected == 'Proximity':
            self.changeProximity()
        elif self.components[6].buttonSelected == 'Stack':
            self.changeStack()
        elif self.components[6].buttonSelected == 'Mobile':
            self.changeMobile()
        elif self.components[6].buttonSelected == 'Stationary':
            self.changeStationary()

        self.components.append(
            Button(
                [20, (self.size[1] - 65) + self.pos[1]],
                [198, 38],
                'assets/icons/button.png',
                'assets/icons/button_hover.png',
                self.close,
                'Close Window'
            )
        )

        self.components.append(
            Button(
                [self.size[1] - 426, (self.size[1] - 65) + self.pos[1]],
                [198, 38],
                'assets/icons/button.png',
                'assets/icons/button_hover.png',
                self.delete,
                'Delete Marker'
            )
        )

    def draw(self, screen: pygame.Surface, right: int, scroll: list[float]):
        super().draw(screen, right, scroll)

        self.image.blit(self.font.render('Size', True, '#000000'), (25, 56))
        self.image.blit(self.font.render('Size', True, '#C2C2C2'), (25, 55))

        self.image.blit(self.font.render('Width', True, '#000000'), (50, 81))
        self.image.blit(self.font.render('Width', True, '#EEE1C5'), (50, 80))

        self.image.blit(self.font.render('Height', True, '#000000'), (50, 116))
        self.image.blit(self.font.render('Height', True, '#EEE1C5'), (50, 115))

        self.image.blit(self.font.render('Type', True, '#000000'), (25, 151))
        self.image.blit(self.font.render('Type', True, '#C2C2C2'), (25, 150))

        screen.blit(self.image, (self.pos[0] + right, self.pos[1] + scroll[1]))

        for _component in self.components:
            _component.draw(screen, right, scroll)

    def onClick(self):
        for _comp in self.components:
            if hasattr(_comp, 'active'): 
                if _comp.active:
                    _comp.exitField()
                _comp.active = False
                
            if _comp.rect.collidepoint(pygame.mouse.get_pos()):
                _comp.onClick()

    def hover(self):
        for _comp in self.components:
            _comp.noHover()
            if _comp.rect.collidepoint(pygame.mouse.get_pos()):
                _comp.hover()

    def changeWidth(self):
        try:
            if self.parent.parent.marker.gridSize[0] < int(self.components[0].text):
                for _ in range(int(self.components[0].text) - self.parent.parent.marker.gridSize[0]):
                    self.addWidth()
            elif self.parent.parent.marker.gridSize[0] > int(self.components[0].text):
                for _ in range(self.parent.parent.marker.gridSize[0] - int(self.components[0].text)):
                    self.minusWidth()
        except:
            self.components[0].text = str(self.parent.parent.marker.gridSize[0])
    
    def addWidth(self):
        self.parent.parent.marker.gridSize[0] += 1
        self.components[0].text = str(self.parent.parent.marker.gridSize[0])
        for _row in self.parent.parent.marker.markerArea:
            _row.append(0)
        self.parent.parent.marker.createGrid()
        self.parent.parent.marker.adjustSize()

        self.components[13].createGrid()

    def minusWidth(self):
        self.parent.parent.marker.gridSize[0] -= 1
        self.components[0].text = str(self.parent.parent.marker.gridSize[0])
        _markerArea: list[list[int]]= []
        for _row in self.parent.parent.marker.markerArea:
            _markerArea.append(_row[:-1])

        self.parent.parent.marker.markerArea = _markerArea
        self.parent.parent.marker.createGrid()
        self.parent.parent.marker.adjustSize()

        self.components[13].markerArea = self.parent.parent.marker.markerArea
        self.components[13].createGrid()

    def changeHeight(self):
        try:
            if self.parent.parent.marker.gridSize[1] < int(self.components[3].text):
                for _ in range(int(self.components[3].text) - self.parent.parent.marker.gridSize[1]):
                    self.addHeight()
            elif self.parent.parent.marker.gridSize[1] > int(self.components[3].text):
                for _ in range(self.parent.parent.marker.gridSize[1] - int(self.components[3].text)):
                    self.minusHeight()
        except:
            self.components[3].text = str(self.parent.parent.marker.gridSize[1])

    def addHeight(self):
        self.parent.parent.marker.gridSize[1] += 1
        self.components[3].text = str(self.parent.parent.marker.gridSize[1])
        self.parent.parent.marker.markerArea.append([0 for _c in range(self.parent.parent.marker.gridSize[0])])
        self.parent.parent.marker.createGrid()
        self.parent.parent.marker.adjustSize()

        self.components[13].createGrid()

    def minusHeight(self):
        self.parent.parent.marker.gridSize[1] -= 1
        self.components[3].text = str(self.parent.parent.marker.gridSize[1])
        self.parent.parent.marker.markerArea = self.parent.parent.marker.markerArea[:-1]
        self.parent.parent.marker.createGrid()
        self.parent.parent.marker.adjustSize()

        self.components[13].markerArea = self.parent.parent.marker.markerArea
        self.components[13].createGrid()

    def changeStationary(self):
        self.parent.parent.marker.type = 3
        self.parent.parent.marker.markerImages()

        self.components[13].type = 3
        self.components[13].markerImages()

        self.components[8].image = self.markerButtonImage[0]
        self.components[8].imageHover = self.markerButtonImage[1]

        self.components[9].image = self.orignButtonImage[0]
        self.components[9].imageHover = self.orignButtonImage[1]

    def changeMobile(self):
        self.parent.parent.marker.type = 2
        self.parent.parent.marker.markerImages()

        self.components[13].type = 2
        self.components[13].markerImages()

        self.components[8].image = self.markerButtonImage[0]
        self.components[8].imageHover = self.markerButtonImage[1]

        self.components[9].image = self.orignOutlineStakeButtonImage[0]
        self.components[9].imageHover = self.orignOutlineStakeButtonImage[1]

    def changeStack(self):
        self.parent.parent.marker.type = 1
        self.parent.parent.marker.markerImages()

        self.components[13].type = 1
        self.components[13].markerImages()

        self.components[8].image = self.orignButtonImage[0]
        self.components[8].imageHover = self.orignButtonImage[1]

        self.components[9].image = self.markerButtonImage[0]
        self.components[9].imageHover = self.markerButtonImage[1]

    def changeProximity(self):
        self.parent.parent.marker.type = 0
        self.parent.parent.marker.markerImages()

        self.components[13].type = 0
        self.components[13].markerImages()

        self.components[8].image = self.markerDisabledButtonImage[0]
        self.components[8].imageHover = self.markerDisabledButtonImage[1]

        self.components[9].image = self.markerButtonImage[0]
        self.components[9].imageHover = self.markerButtonImage[1]

    def _turnOffAllPaints(self, exception: int):
        for _i in range(7, 13):
            if _i == exception:
                continue
            self.components[_i].on = False

    def paintGrid(self):
        self.components[13].paint = 0
        self._turnOffAllPaints(7)

    def paintMarker(self):
        self.components[13].paint = 1
        self._turnOffAllPaints(8)

    def paintOrigin(self):
        self.components[13].paint = 2
        self._turnOffAllPaints(9)

    def paintTank(self):
        self.components[13].paint = 3
        self._turnOffAllPaints(10)

    def paintHealer(self):
        self.components[13].paint = 4
        self._turnOffAllPaints(11)

    def paintDPS(self):
        self.components[13].paint = 5
        self._turnOffAllPaints(12)

    def close(self):
        self.parent.window = None

    def delete(self):
        self.parent.parent.marker = None
        self.parent.window = None

    def blank(self):
        pass
