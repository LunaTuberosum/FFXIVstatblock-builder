from os import listdir
import sys
import pygame

from menu.menu import Menu

from singletons.eventBus import event_bus
from singletons import resourceHandler

from src.display import Display
from src.gameProcess import GameProcess


DEFAULT_SCREEN_WIDTH = 1440
DEFAULT_SCREEN_HEIGHT = 810

class GameLoop():
    def __init__(self) -> None:
        pygame.font.init()
        
        self.clock = pygame.Clock()
        self.display: Display = None 
        self.load_setting_save()
        
        pygame.display.set_caption('FFXIV TTRPG Stat Card Builder V0.93')
        pygame.display.set_icon(resourceHandler.load_image('.\\assets\\icon.ico'))
        
        pygame.key.set_repeat(200, 100)
        
        self.current_process: GameProcess = Menu(self)
        self.run: bool = True
        
        event_bus.register('quit', self.quit)
        
    def quit(self) -> None:
        pygame.quit()
        self.run = False
        
    def load_setting_save(self) -> None:
        setting_save: dict[str] = resourceHandler.load_pickle('.//settings.pkl')

        if not setting_save:
            setting_save = {
                'windowSize': (DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT),
                'displayOption': 1,
                'framerate': 0,
                'vsync': False
            }

            resourceHandler.save_pickle('.//settings.pkl', setting_save)

        self.display = Display(setting_save['windowSize'][0], setting_save['windowSize'][1])
        self.display.set_fullscreen(setting_save['displayOption'])
        self.display.set_framerate(setting_save['framerate'])
        self.display.set_vsync(setting_save['vsync'])
        
        self.display.create_screen()
    
    def get_screen(self) -> pygame.Surface:
        return self.display.screen
    
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