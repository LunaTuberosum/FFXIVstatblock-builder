import json
import os
from contextMenu import ContextMenu
from save import Save
from saveAdd import SaveAdd
from settings import *

from editor import Editor
from ui.background import Background
from ui.confirm import ConfirmUI

class Menu():
    
    def __init__(self, screen: pygame.Surface, clock: pygame.Clock):
        self.screen: pygame.Surface = screen
        self.clock: pygame.Clock = clock
        self.saves: list[str] = os.listdir('.//saves')

        self.window: Background = None

        self.saveFiles: list[Save] = [Save(_save, self) for _save in self.saves]
        self.newSave: SaveAdd = SaveAdd(self)

        self.contextMenu: ContextMenu = None
        self.contextMenuPos: list[int] = []

    def leftClick(self):
        if self.window:
            if not self.window.rect.collidepoint(pygame.mouse.get_pos()):
                self.window = None
                return
            
            for _comp in self.window.components:
                if _comp.rect.collidepoint(pygame.mouse.get_pos()):
                    _comp.onClick()
                    return

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
                
    def quit(self):
        def quitConfirm():
            pygame.quit()
            os._exit(-1)

        self.window = ConfirmUI(self, 'Are you sure you want to exit?', quitConfirm, 'Exit', 'Stay')

    def delete(self, save: Save):
        def deleteConfirm():
            os.remove(f'.//saves//{save.saveJson}')
            self.saves.remove(save.saveJson)
            self.saveFiles.remove(save)
            self.window = False

        self.window = ConfirmUI(self, 'Are you sure you want to delete this save?', deleteConfirm)

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
            self.screen.fill('#313031')

            self.screen.blit(JUPITER_FONT.render('FFXIV TTRPG Stat Card Builder', True, '#000000'), (10, 21))
            self.screen.blit(JUPITER_FONT.render('FFXIV TTRPG Stat Card Builder', True, '#CCCCCC'), (10, 20))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    os._exit(-1)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.quit()
                
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

            if self.window:
                for _comp in self.window.components:
                    _comp.noHover()

                    if _comp.rect.collidepoint(pygame.mouse.get_pos()):
                        _comp.hover()

                self.window.draw(self.screen, 0, [0, 0])

            if self.contextMenu:

                for _option in self.contextMenu.options:
                    _option.noHover()

                    if _option.rect.collidepoint(pygame.mouse.get_pos()):
                        if not _option.hovering:
                            _option.hover()

            if self.contextMenu:
                self.contextMenu.draw(self.screen, self.contextMenuPos)

            pygame.display.flip()