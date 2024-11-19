from contextMenu import ContextMenu
from settings import *

from components.component import Component


class StatCard(pygame.sprite.Sprite):
    def __init__(self, statCardBackground: dict[str, pygame.Surface], width: int, height: int, editor: object):
        super().__init__()
        self.image: pygame.Surface = None
        self.__statCardBackground: dict[str, pygame.Surface] = statCardBackground
        self.width: int = width
        self.totalWidth: int = 0
        self.height: int = height
        self.editor: object = editor

        self.rect: pygame.Rect = pygame.Rect((0, 0), (
            ((1 + ((width - 1) * 3)) + 2) * 194, 
            (height + 2) * 194
        ))

        self.components: list[Component] = list()
        
        
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

    def addComponent(self, component: Component):
        self.components.append(component)

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
            _height: int = (self.height + 2) * 194
            
        self.rect = pygame.Rect((x + scroll[0], 40 + scroll[1]), self.image.get_size())

        _x: int = 0
        _y: int = 20

        for _comp in self.components:
            _comp.last = False

        _last: Component = self.components[len(self.components) - 1]
        if hasattr(_last, 'last'):
            _last.last = True
        
        if self.height == 0:
            for _comp in self.components:
                _comp.draw(self.image, (_x, _y))

                _y += _comp.height()

        else:
            for _i, _comp in enumerate(self.components):
                if _y + _comp.height() >= _height - 60:
                    _y = 20
                    self.components[_i - 1].last = True
                    _x += 550
                    if _x + _comp.width() >= self.totalWidth:
                        self.width += 1
                        self._makeStatCardBackground(self.width, self.height)
                _comp.draw(self.image, (_x, _y))

                _y += _comp.height()

        screen.blit(self.image, [x + scroll[0], 40 + scroll[1]])

    def save(self) -> dict:
        _dict: dict = {
            'width': self.width,
            'height': self.height,
            'components': {}
        }
        for _i, _comp in enumerate(self.components):
            _dict['components'][f'{_comp.id} [{_i}]'] = _comp.save()

        return _dict

    def contextMenu(self) -> ContextMenu:
        return ContextMenu([186, 96], {
            'Edit': self.edit,
            'Clear': self.clear,
            'Delete': self.delete
        })

    def edit(self):
        self.editor.edit(self)

    def clear(self):
        print('Clear')

    def delete(self):
        self.editor.statCards.remove(self)

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