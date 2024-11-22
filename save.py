import json
from contextMenu import ContextMenu
from settings import *


class Save(pygame.sprite.Sprite):
    def __init__(self, saveJson: str, menu: object):
        super().__init__()

        self.menu: object = menu

        self.saveJson: str = saveJson
        self.saveInfo: dict = {}
        with open(f'.//saves//{saveJson}', 'r') as _saveFile:
            self.saveInfo = json.load(_saveFile)

        self.image: pygame.Surface = pygame.Surface((250, 250))

        self.rect: pygame.Rect = self.image.get_rect(topleft=(0, 0))
        self.font: pygame.font.Font = pygame.font.Font('assets/fonts/LibreBaskerville.ttf', 20)

        self.hovering: bool = False

    def draw(self, screen: pygame.Surface, x: int, y: int):
        self.image.fill('#efefef' if self.hovering else '#dedede')
        self.rect = self.image.get_rect(topleft=(x, y))

        _y: int = 10
        for _card in self.saveInfo.values():
            _name: list[str] = ('- ' + _card['components']['NameComponent [0]']['name']).split(' ')
            _x = 10
            for _word in _name:
                if _x + self.font.size(_word)[0] > 250:
                    _x = 10
                    _y += 25
                self.image.blit(self.font.render(_word, True, '#000000'), (_x, _y))
                _x += self.font.size(_word + ' ')[0]
            _y += 25
            if _y + 50 >= 250:
                self.image.blit(self.font.render('...', True, '#000000'), (10, _y))
                break 

        if len(self.saveInfo.values()) == 0:
            self.image.blit(self.font.render('EMPTY', True, '#000000'), (10, 10))

        screen.blit(self.image, (x, y))

    def reload(self, saveDict: dict):
        self.saveInfo = saveDict

    def contextMenu(self) -> ContextMenu:
        return ContextMenu(
            [186, 48],
            {
                'Delete': self.delete
            }
        )

    def delete(self):
        self.menu.delete(self)

    def noHover(self):
        if not self.hovering:
            return
        self.hovering = False

    def hover(self):
        self.hovering = True

    def onClick(self):
        return self.saveJson.split('.')[0].split('Sheet')[1]
