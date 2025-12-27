import re

from typing import Callable

import pygame

from singletons import resourceHandler
from singletons.eventBus import event_bus
from singletons.keyBus import key_bus

from menu.menuObject import MenuObject
from menu.sheet import Sheet
from src.timer import Timer


ENTRY_START_Y: int = 75
ENTRY_MAX_LINES: int = 5

Y_OFFSET: int = 45

SEPERATOR_SIZE: tuple[int, int] = (155, 3)
SEPERATOR_POS: tuple[int, int] = (33, 70)

RECT_POS: tuple[int, int] = (19, 35)
RECT_SIZE: tuple[int, int] = (212, 180)

def sort() -> Callable:
    convert = lambda text: int(text) if text.isdigit() else text 
    return lambda key: [ convert(c) for c in re.split('([0-9]+)', key.name.lower()) ] 

class Folder(MenuObject):
    def __init__(self, path: str, folder: str) -> None:
        super().__init__(
            folder,
            path, 
            'UIFolder'
        )        
        self.TILE_MAX_WIDTH = 157
        
        self.files: list[MenuObject] = []
        
        self.add_files()
        
        self.is_prev: bool = False
        
        self.click_timer: Timer = Timer(300)
        
        key_bus.register('mouse_left_down', self.on_click)
        event_bus.register('duplicate_sheet', self.duplicate_sheet)
        
    def deregister(self):
        super().deregister()
        
        key_bus.deregister('mouse_left_down', self.on_click)
        event_bus.deregister('duplicate_sheet', self.duplicate_sheet)
        
    def on_click(self) -> None:
        if not self.hovering:
            return
        
        if self.click_timer.time_left() > 0:
            event_bus.sign('change_folder', self)
        else:
            self.click_timer.start()
        
    def add_files(self) -> None:
        # '' -> 'folder' -> 'fodler//folder2'
        for m_file in resourceHandler.load_dir(f'.\\saves\\{self.path}\\{self.name}'):
            if m_file.endswith('.json'):  
                self.files.append(Sheet(f'{self.path}\\{self.name}', m_file))
                continue
            self.files.append(Folder(f'{self.path}\\{self.name}', m_file))
            
        self.files.sort(key=sort())
        
    def get_entry(self, entry) -> str:
        return super().get_entry(entry.name)
            
    def draw(self, screen: pygame.Surface, x: int, y: int) -> None:
        if self.is_prev:
            prev_name: str = self.name
            self.name = 'Go Back...'
            super().draw(x, y, Y_OFFSET)
            self.name = prev_name
        else:
            super().draw(x, y, Y_OFFSET)
        self.rect = pygame.Rect((x + RECT_POS[0], y + RECT_POS[1]), RECT_SIZE)
        
        self.image.blit(pygame.transform.scale(self.seperator, SEPERATOR_SIZE), SEPERATOR_POS)
        
        self.draw_entries(self.files, ENTRY_START_Y, ENTRY_MAX_LINES)

        if self.hovering:
            screen.blit(self.add_outline(self.image), (x - 2, y - 2))
        else:
            screen.blit(self.image, (x, y))
            
    def context_menu(self) -> None:
        if self.is_prev: return
        
        super().context_menu()
                        
    def create_folder(self) -> None:
        event_bus.sign('context_menu', {})
        
        new_name: str = 'New Folder'
        count: int = 0
        for m_file in self.files:
            if isinstance(m_file, Folder) and m_file.name.startswith(new_name):
                count += 1
        
        if count:
            new_name += f' {count}'

        resourceHandler.save_dir(f'.\\saves\\{self.path}\\{self.name}', new_name)
        
        self.files.append(Folder(f'{self.path}\\{self.name}', new_name))
        self.files.sort(key=sort())
    
    def create_sheet(self) -> None:
        event_bus.sign('context_menu', {})
        
        new_name: str = 'New Stat Sheet'
        count: int = 0
        for m_file in self.files:
            if isinstance(m_file, Sheet) and m_file.name.startswith(new_name):
                count += 1
        
        if count:
            new_name += f' {count}'

        resourceHandler.save_json(f'.\\saves\\{self.path}\\{self.name}\\{new_name}.json', {})
        
        self.files.append(Sheet(f'{self.path}\\{self.name}', f'{new_name}.json'))
        self.files.sort(key=sort())
        
    def duplicate_sheet(self, sheet: Sheet) -> None:
        if not any(m_file == sheet for m_file in self.files):
            return
        
        new_name: str = sheet.name + ' - Copy'
        count: int = 0
        for m_file in self.files:
            if isinstance(m_file, Sheet) and m_file.name.startswith(new_name):
                count += 1
                
        if count:
            new_name += f' ({count})'
            
        resourceHandler.save_json(f'.\\saves\\{self.path}\\{self.name}\\{new_name}.json', sheet.sheet_info)
        
        self.files.append(Sheet(f'{self.path}\\{self.name}', f'{new_name}.json'))
        self.files.sort(key=sort())
        
    def rename(self, text: str) -> None:
        if not text:
            text = 'New Folder Name'
        
        if not resourceHandler.rename_dir(f'.\\saves\\{self.path}\\{self.name}', f'.\\saves\\{self.path}\\{text}'):
            return
        
        for m_file in self.files:
            m_file.path = f'.\\saves\\{self.path}\\{text}'
            
        self.name = text