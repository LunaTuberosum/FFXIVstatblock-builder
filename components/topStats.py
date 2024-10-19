from settings import *

from components.component import Component
from ui.topStats import TopStatsUI


class TopStatsComponent(Component):
    def __init__(self):
        super().__init__(
            "TopStatsComponent",
            [526, 171],
            [5, 5],
            1
        )

        self.font: pygame.font.Font = pygame.font.SysFont('Noto Sans', 16, True)
        self.fontCap: pygame.font.Font = pygame.font.SysFont('Noto Sans', 18, True)

        self.largeFont: pygame.font.Font = pygame.font.SysFont('Noto Sans', 18, True)
        self.largeFontCap: pygame.font.Font = pygame.font.SysFont('Noto Sans', 20, True)

        self.topLine: pygame.Surface = pygame.image.load('assets/backgrounds/StatsTopLine.png').convert_alpha()

        _background: pygame.Surface = pygame.image.load('assets/backgrounds/StatsBackground.png').convert_alpha()
        self.backgroundMiddle: pygame.Surface = pygame.Surface((530, 45))
        self.backgroundMiddle.fill('#F3E1C6')
        self.backgroundMiddle.blit(_background, (0, 0))
        self.backgroundMiddle = pygame.transform.scale(self.backgroundMiddle, (530, self.height() - 60))

        self.backgroundBottom: pygame.Surface = pygame.Surface((530, 45))
        self.backgroundBottom.fill('#F3E1C6')
        self.backgroundBottom.blit(_background, (0, -45))

        self.seperator: pygame.Surface = pygame.image.load('assets/backgrounds/StatsSeperator.png').convert_alpha()

        self.creatureSize: str = 'Large (2x2)'
        self.species: str = 'Elder Primal'
        self.vigilance: str = '20'

        self.defense: str = '12'
        self.magicDefense: str = '12'
        self.maxHP: str = '120'
        self.speed: str = '0'

        self.str: str = '7'
        self.dex: str = '7'
        self.vit: str = '7'
        self.int: str = '7'
        self.mnd: str = '7'

    def draw(self, screen: pygame.Surface, parentPos: list[int]) -> None:
        super().draw(screen, parentPos)
        self.image.blit(self.backgroundMiddle, (3, 18))
        self.image.blit(self.backgroundBottom, (3, self.height() - self.backgroundBottom.get_height()))
        self.image.blit(self.topLine, (0, 0))

        self._renderLargeNumber(f'Size: {self.creatureSize} - {self.species}', 15, 4, self.font, self.fontCap, MIEDINGER)
        self._renderLargeNumber(f'Vigilance: {self.vigilance}', 516 - (self.fontCap.size('Vigilance: ')[0] + MIEDINGER.size(self.vigilance)[0]), 4, self.font, self.fontCap, MIEDINGER)


        self._renderLargeNumber(f'Defense: {self.defense}', 15, 40, self.largeFont, self.largeFontCap, MIEDINGER_MEDIUM)
        self._renderLargeNumber(f'Max HP: {self.maxHP}', 15, 70, self.largeFont, self.largeFontCap, MIEDINGER_MEDIUM)

        self._renderLargeNumber(f'Magic Defense: {self.magicDefense}', 263, 40, self.largeFont, self.largeFontCap, MIEDINGER_MEDIUM)
        self._renderLargeNumber(f'Speed:  {self.speed} squares', 263, 70, self.largeFont, self.largeFontCap, MIEDINGER_MEDIUM)

        self.image.blit(self.seperator, (12, 102))

        self.image.blit(MIEDINGER_MEDIUM.render('STR', True, '#ffffff'), (25, 112))
        self.image.blit(MIEDINGER_MEDIUM.render(('+' if int(self.str) >= 0 else '') + self.str, True, '#ffffff'), (
            25 + MIEDINGER_MEDIUM.size('STR')[0] / 2 - MIEDINGER_MEDIUM.size(('+' if int(self.str) >= 0 else '') + self.str)[0] / 2, 
            137
        ))

        self.image.blit(MIEDINGER_MEDIUM.render('DEX', True, '#ffffff'), (135, 112))
        self.image.blit(MIEDINGER_MEDIUM.render(('+' if int(self.dex) >= 0 else '') + self.dex, True, '#ffffff'), (
            135 + MIEDINGER_MEDIUM.size('DEX')[0] / 2 - MIEDINGER_MEDIUM.size(('+' if int(self.dex) >= 0 else '') + self.dex)[0] / 2, 
            137
        ))

        self.image.blit(MIEDINGER_MEDIUM.render('VIT', True, '#ffffff'), (244, 112))
        self.image.blit(MIEDINGER_MEDIUM.render(('+' if int(self.vit) >= 0 else '') + self.vit, True, '#ffffff'), (
            244 + MIEDINGER_MEDIUM.size('VIT')[0] / 2 - MIEDINGER_MEDIUM.size(('+' if int(self.vit) >= 0 else '') + self.vit)[0] / 2, 
            137
        ))

        self.image.blit(MIEDINGER_MEDIUM.render('INT', True, '#ffffff'), (335, 112))
        self.image.blit(MIEDINGER_MEDIUM.render(('+' if int(self.int) >= 0 else '') + self.int, True, '#ffffff'), (
            335 + MIEDINGER_MEDIUM.size('INT')[0] / 2 - MIEDINGER_MEDIUM.size(('+' if int(self.int) >= 0 else '') + self.int)[0] / 2, 
            137
        ))

        self.image.blit(MIEDINGER_MEDIUM.render('MND', True, '#ffffff'), (427, 112))
        self.image.blit(MIEDINGER_MEDIUM.render(('+' if int(self.mnd) >= 0 else '') + self.mnd, True, '#ffffff'), (
            427 + MIEDINGER_MEDIUM.size('MND')[0] / 2 - MIEDINGER_MEDIUM.size(('+' if int(self.mnd) >= 0 else '') + self.mnd)[0] / 2, 
            137
        ))

        screen.blit(self.image, [20 + self.x(), parentPos[1] + self.y()])

    def onClick(self):
        if self.window:
            self.window = None
            return
        self.window = TopStatsUI([-15, 90], self)



