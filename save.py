import json
from contextMenu import ContextMenu
from settings import *
from ui.background import Background


class Save(Background):
    def __init__(self, saveJson: str, menu: object):
        super().__init__(
            f'Save ({saveJson})',
            f'Stat Sheet {saveJson.split(".")[0][9:]}',
            [250, 250],
            [0, 0],
            False
        )

        self.menu: object = menu

        self.saveJson: str = saveJson
        self.saveInfo: dict = {}
        with open(f'.//saves//{saveJson}', 'r') as _saveFile:
            self.saveInfo = json.load(_saveFile)

        self.image: pygame.Surface = pygame.Surface((250, 250))

        self.rect: pygame.Rect = self.image.get_rect(topleft=(0, 0))


    def draw(self, screen: pygame.Surface, x: int, y: int):
        self.pos = [x, y]
        super().draw(screen, 0, [0, 0])

        _y: int = 55
        for _card in self.saveInfo.values():
            _name: list[str] = ('- ' + _card['components']['NameComponent [0]']['name']).split(' ')
            _x = 25
            for _word in _name:
                if _x + self.font.size(_word)[0] > 230:
                    _x = 25
                    _y += 25
                self.image.blit(self.font.render(_word, True, '#000000'), (_x, _y + 1))                    
                self.image.blit(self.font.render(_word, True, '#CCCCCC' if not self.hovering else '#dedede'), (_x, _y))
                _x += self.font.size(_word + ' ')[0]
            _y += 25
            if _y + 50 >= 250:
                self.image.blit(self.font.render('...', True, '#000000'), (10, _y + 1))                
                self.image.blit(self.font.render('...', True, '#CCCCCC' if not self.hovering else '#dedede'), (10, _y))
                break 

        if len(self.saveInfo.values()) == 0:
            self.image.blit(self.font.render('EMPTY', True, '#000000'), (25, 56))            
            self.image.blit(self.font.render('EMPTY', True, '#CCCCCC' if not self.hovering else '#dedede'), (25, 55))

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
        return self.saveJson.split('.')[0][9:]
