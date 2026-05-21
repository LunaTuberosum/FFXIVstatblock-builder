from os import listdir
import sys
import pygame

from editor.editor import Editor
from menu.folder import Folder
from menu.menu import Menu

from singletons.eventBus import event_bus
from singletons.keyBus import key_bus 

from singletons import resourceHandler

from src.display import Display
from src.gameProcess import GameProcess


DEFAULT_SCREEN_WIDTH = 1440
DEFAULT_SCREEN_HEIGHT = 810

class GameLoop():
    def __init__(self) -> None:
        pygame.init()
        
        self.clock = pygame.Clock()
        self.display: Display = None 
        self.load_setting_save()
        
        pygame.mixer.set_num_channels(3)
        
        pygame.display.set_caption('FFXIV TTRPG Stat Card Builder V0.93.2')
        pygame.display.set_icon(resourceHandler.load_image('.\\assets\\icon.ico'))
        
        pygame.key.set_repeat(200, 100)
        
        self.current_process: GameProcess = Menu(self)
        self.run: bool = True
        
        self.set_up_bus_calls()
        
    def set_up_bus_calls(self) -> None:
        event_bus.register('quit', self.quit)
        event_bus.register('load_sheet', self.load_sheet)
        event_bus.register('return_menu', self.return_menu)
        
    def quit(self) -> None:
        pygame.quit()
        self.run = False
        
    def load_setting_save(self) -> None:
        setting_save: dict[str] = resourceHandler.load_pickle('.//settings.pkl')

        if not setting_save:
            setting_save = {
                'monitor': 1,
                
                'windowSize': (DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT),
                'displayOption': 1,
                'framerate': 0,
                'vsync': False,
                
                'volume': 1
            }

            resourceHandler.save_pickle('.//settings.pkl', setting_save)

        self.display = Display(setting_save['windowSize'][0], setting_save['windowSize'][1])
        self.display.set_monitor(setting_save['monitor'])
        self.display.set_fullscreen(setting_save['displayOption'])
        self.display.set_framerate(setting_save['framerate'])
        self.display.set_vsync(setting_save['vsync'])
        
        self.display.set_volume(setting_save['volume'])
        
        self.display.create_screen()
    
    def get_screen(self) -> pygame.Surface:
        return self.display.screen
    
    def load_sheet(self, sheet: object) -> None:
        event_bus.reset()
        key_bus.reset()
        self.set_up_bus_calls()
        
        self.current_process = Editor(self, sheet, self.current_process.current_folder, self.current_process.prev_folder)
                
    def search_for_folder(self, folder: Folder, look_folder: Folder) -> Folder:
        for m_file in folder.files:
            if not isinstance(m_file, Folder):
                continue
            
            if m_file.id == look_folder.id:
                return m_file
            
            if found := self.search_for_folder(m_file, look_folder):
                return found
                
    def return_menu(self, current_folder: Folder, prev_folders: list[Folder]) -> None:
        event_bus.reset()
        key_bus.reset()
        self.set_up_bus_calls()
            
        self.current_process = Menu(self)
        
        prev_fold: list[Folder] = []
        for folder in prev_folders:
            if folder.id == self.current_process.current_folder.id:
                self.current_process.current_folder.is_prev = True
                prev_fold.append(self.current_process.current_folder)
                continue
            
            m_file = self.search_for_folder(self.current_process.current_folder, folder)
            m_file.is_prev = True
            prev_fold.append(m_file)
            
        self.current_process.prev_folder = prev_fold
        
        if self.current_process.current_folder.id != current_folder.id:
            self.current_process.current_folder = self.search_for_folder(self.current_process.current_folder, current_folder)
            
    def update(self) -> None:
        while self.run:
            try:
                self.current_process.update()
                
            except KeyboardInterrupt:
                sys.exit(130)
                
            except Exception:
                if not self.run:
                    sys.exit(0)
                    return
                
                import traceback
                traceback.print_exc(file=sys.stdout)
                
                with open(f'.\\logs\\error_log_{len(listdir('.\\logs'))}.txt', 'w') as error_log:
                    error_log.write(traceback.format_exc())
                    
                sys.exit(0)