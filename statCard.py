from settings import *

from components.component import Component
from components.name import NameComponent
from components.topStats import TopStatsComponent
from components.sectionName import SectionNameComponent
from components.trait import TraitComponent
from components.ability import AbilityComponent


class StatCard():
    def __init__(self, statCardBackground: dict[str, pygame.Surface], width: int, height: int, components: list[Component] = []):
        self.image: pygame.Surface = None
        self.__statCardBackground: dict[str, pygame.Surface] = statCardBackground
        self.width: int = width
        self.totalWidth: int = 0
        self.height: int = height

        self.components: list[Component] = components
        self.components.append(NameComponent())
        self.components.append(TopStatsComponent())

        self.components.append(SectionNameComponent('Traits', 2))
        self.components.append(TraitComponent(
            'Elite Foe: Lord of the Corpse Hall',
            'This character cannot be {b} Stunned {/b} and markers they have generated cannot be removed. Be sure to inform players of this before beginning the encounter.'
        ))
        self.components.append(TraitComponent(
            'Survive and Receive Valhalla',
            'This creature summons 2 [Gungnir] 3 spaces from itself at the start of each round.'
        ))

        self.components.append(SectionNameComponent('Abilites', 2))

        self.components.append(AbilityComponent(
            'Shin-Zantetsiken',
            'Primary, Physical',
            {
                'Marker Area:': 'The entire encounter map',
                'Target:': 'All enemies within the marker area',
                'Marker Trigger:': 'The beginning of the 3rd round',
                'Marker Effect:': 'Deals 999 damage.'
            }
        ))

        self.components.append(AbilityComponent(
            'Gungnir',
            'Primary, Mobile Marker, Magic',
            {
                'Origin': 'Two squares occupied by two separate enemy characters without {b} Enmity {/b}',
                'Marker Area:': 'A mobile 5x5 area centered on the origins',
                'Target:': 'All enemies within the marker area',
                'Marker Trigger:': 'The beginning of this character\'s next turn',
                'Marker Effect:': 'Deals 3d6 damage and summons a [Gungnir] in an unoccupied adjacenet area to the center.'
            },
            [
                [0, 0, 0, 0, 0, 0, 0],
                [0, 1, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 0],
                [0, 1, 1, 2, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 0],
                [0, 0, 0, 0, 0, 0, 0]
            ]
        ))
        
        if self.height == 0:
            _height: int = 25

            for _c in self.components:
                _height += _c.height()

            _height += 5
            if _height < 363:
                _height = 363


            self.temp = _height
            self._makeStatCardBackgroundScale(self.width, _height)
        else:
            self._makeStatCardBackground(self.width, self.height)

    def draw(self, screen: pygame.Surface, scroll: list[float], x: int):
        screen.blit(self.image, [x + scroll[0], 20 + scroll[1]])

        _x: int = x
        _y: int = 20

        _last: Component = self.components[len(self.components) - 1]
        if hasattr(_last, 'last'):
            _last.last = True
        
        for _comp in self.components:
            _comp.draw(self.image, (_x, _y))

            _y += _comp.height()

    # TODO: do it later Mignt not need to?
    def sortComponenets(self) -> None:
        pass

    def _makeStatCardBackground(self, width: int, height: int) -> pygame.Surface:
        _img: pygame.Surface = pygame.surface.Surface(
            (((1 + ((width - 1) * 3)) + 2) * 194,
            (height + 2) * 194)
        )
        self.totalWidth = _img.get_width()
        
        _x: int = 0
        _y: int = 0
        _i: int = 0
        _list: list[str] = ['Top', '', 'Bottom']

        for _h in range(height + 2):
            if _h > 0:
                _y += 194
            _img.blit(self.__statCardBackground[_list[_i] + 'Left'], (_x, _y))

            for _w in range(1 + (3 * (width - 1))):
                _x += 194

                _img.blit(self.__statCardBackground[_list[_i] + 'Middle'], (_x, _y))

            _x += 194
            _img.blit(self.__statCardBackground[_list[_i] + 'Right'], (_x, _y))

            _x = 0
            if _h == 0:
                _i = 1
            elif _h == height:
                _i = 2

        self.image = _img

    def _makeStatCardBackgroundScale(self, width: int, height: int) -> pygame.Surface:
        _img: pygame.Surface = pygame.surface.Surface(
            (((1 + ((width - 1) * 3)) + 2) * 194,
            363 if height == 0 else height + 25)
        )
        height -= 363

        self.totalWidth = _img.get_width()

        _x: int = 0

        _img.blit(self.__statCardBackground['TopLeft'], (_x, 0))

        for _w in range(1 + (3 * (width - 1))):
            _x += 194

            _img.blit(self.__statCardBackground['TopMiddle'], (_x, 0))

        _x += 194
        _img.blit(self.__statCardBackground['TopRight'], (_x, 0))

        _left: pygame.Surface = pygame.transform.scale(self.__statCardBackground['Left'], (194, height))
        _middle: pygame.surface = pygame.transform.scale(self.__statCardBackground['Middle'], (_x - 194, height))
        _right: pygame.Surface = pygame.transform.scale(self.__statCardBackground['Right'], (194, height))

        _img.blit(_left, (0, 194))
        _img.blit(_middle, (194, 194))
        _img.blit(_right, (_x, 194))

        _x: int = 0

        _img.blit(self.__statCardBackground['BottomLeft'], (_x, height + 194))

        for _w in range(1 + (3 * (width - 1))):
            _x += 194

            _img.blit(self.__statCardBackground['BottomMiddle'], (_x, height + 194))

        _x += 194
        _img.blit(self.__statCardBackground['BottomRight'], (_x, height + 194))

        self.image = _img