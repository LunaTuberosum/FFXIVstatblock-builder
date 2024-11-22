import json
import os
from contextMenu import ContextMenu
from save import Save
from saveAdd import SaveAdd
from settings import *

from editor import Editor

class Menu():
    
    def __init__(self, screen: pygame.Surface, clock: pygame.Clock):
        self.screen: pygame.Surface = screen
        self.clock: pygame.Clock = clock
        self.saves: list[str] = os.listdir('.//saves')

        self.saveFiles: list[Save] = [Save(_save, self) for _save in self.saves]
        self.newSave: SaveAdd = SaveAdd(self)

        self.contextMenu: ContextMenu = None
        self.contextMenuPos: list[int] = []

    def leftClick(self):
        if self.contextMenu:
            if not self.contextMenu.rect.collidepoint(pygame.mouse.get_pos()):
                self.contextMenu = None
                return

            for _option in self.contextMenu.options:
                _option.clicked = False

                if _option.rect.collidepoint(pygame.mouse.get_pos()):
                    _option.onClick()
                    self.contextMenu = None
                    return
                
        if self.newSave.rect.collidepoint(pygame.mouse.get_pos()):
            self.createNewSave()
                
        for _save in self.saveFiles:
            if _save.rect.collidepoint(pygame.mouse.get_pos()):
                _saveFileNum = _save.onClick()
                _saveDict = Editor(self.screen, self.clock, _saveFileNum).main()
                _save.reload(_saveDict)
                return
                
    def delete(self, save: Save):
        os.remove(f'.//saves//{save.saveJson}')
        self.saveFiles.remove(save)

    def createNewSave(self):
        _i: int = 0
        for _save in self.saves:
            _name: str = _save.split('.')[0]
            _num: str = _name[9:]
            if _i <= int(_num):
                _i = int(_num)
        _i += 1

        with open(f'.//saves//statsheet{_i}.json', 'w') as _:
            _.write(json.dumps({}, indent=4))

        self.saves.append(f'statSheet{_i}.json')
        self.saveFiles.append(Save(f'statSheet{_i}.json', self))

    def main(self) -> None:

        while True:
            self.clock.tick(30)
            self.screen.fill('#B7B7B7')

            self.screen.blit(JUPITER_FONT.render('FFXIV TTRPG Stat Card Builder', True, '#000000'), (10, 20))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.leftClick()
                    
                    elif event.button == 3:
                        for _save in self.saveFiles: 
                            if _save.rect.collidepoint(pygame.mouse.get_pos()):
                                self.contextMenu = _save.contextMenu()
                                self.contextMenuPos = pygame.mouse.get_pos()
                                break

            _x: int = 15
            _y: int = 70
            for _save in self.saveFiles:
                _save.noHover()
                if _save.rect.collidepoint(pygame.mouse.get_pos()):
                    _save.hover()

                _save.draw(self.screen, _x, _y)
                _x += 260
                if _x >= 1835:
                    _x = 15
                    _y += 260

            self.newSave.noHover()
            if self.newSave.rect.collidepoint(pygame.mouse.get_pos()):
                self.newSave.hover()

            self.newSave.draw(self.screen, _x, _y)

            if self.contextMenu:

                for _option in self.contextMenu.options:
                    _option.noHover()

                    if _option.rect.collidepoint(pygame.mouse.get_pos()):
                        if not _option.hovering:
                            _option.hover()

            if self.contextMenu:
                self.contextMenu.draw(self.screen, self.contextMenuPos)

            pygame.display.flip()