from settings import *

from components.component import Component


class SectionNameComponent(Component):
    def __init__(self, section: str, priority: int):
        super().__init__(
            "SectionNameComponent",
            [520, 42],
            [10, 10],
            priority
        )

        self.section: str = section

        self.divider: pygame.Surface = pygame.image.load('assets/backgrounds/StatCardDivider.png').convert_alpha()

        self.fontCap: pygame.font.Font = pygame.font.Font('assets/fonts/LibreBaskerville.ttf', 22)
        self.font: pygame.font.Font = pygame.font.Font('assets/fonts/LibreBaskerville.ttf', 18)

    def draw(self, screen: pygame.Surface, parentPos: list[int]) -> None:
        super().draw(screen, parentPos)
        self._renderSmallCase(self.section, 0)

        self.image.blit(self.divider, (2, self.height() - 3))

        screen.blit(self.image, (20 + self.x(), parentPos[1] + self.y()))



