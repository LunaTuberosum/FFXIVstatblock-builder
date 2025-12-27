from typing import Callable
import pygame

from menu.ui.renameElement import RenameElement

from singletons import resourceHandler

from singletons.eventBus import event_bus
from singletons.keyBus import key_bus


ENTRY_START_X: int = 33
ENTRY_INDENT_X: int = 44
ENTRY_INCREASE: int = 25
ENTRY_X_BOUND: int = 215

class MenuObject():
    def __init__(self, name: str, path: str, background: str) -> None:
        self.TILE_MAX_WIDTH: int = 187
        
        self.name: str = name
        self.path: str = path
        
        self.seperator: pygame.Surface = resourceHandler.load_image('assets/backgrounds/UISeperator.png')
        self.background: pygame.Surface = resourceHandler.load_image(f'assets/backgrounds/{background}.png')
        
        self.size: tuple[int, int] = (250, 250)
        self.image: pygame.Surface = pygame.Surface(self.size, pygame.SRCALPHA)
        
        self.rect: pygame.Rect = self.image.get_rect()
        
        self.font: pygame.font.Font = resourceHandler.load_font('assets/fonts/noto-sans.regular.ttf', 18)
        self.fontTitle: pygame.font.Font = resourceHandler.load_font('assets/fonts/Deutschlander.otf', 25)
        
        self.hovering: bool = False
        
        key_bus.register('mouse_right_down', self.context_menu)
        
    def deregister(self) -> None:
        key_bus.deregister('mouse_right_down', self.context_menu)
        
    def add_outline(self, image: pygame.Surface) -> pygame.Surface:
        con_mask = pygame.mask.Mask((5, 5), fill=True)

        mask = pygame.mask.from_surface(image)

        surf_out = mask.convolve(con_mask).to_surface(setcolor="#1D1D1D", unsetcolor=(0, 0, 0, 0))

        surf_out.blit(image, (-1, -1))

        return surf_out
    
    def get_entry(self, entry) -> str:
        return f'- {entry}'.split(' ')
    
    def render_text(self, text: str, color: str, pos: tuple[int, int]) -> None:
        self.image.blit(self.font.render(text, True, '#000000'), (pos[0], pos[1] + 1))
        self.image.blit(self.font.render(text, True, color), pos)
    
    def draw_entries(self, entries: list, entry_start_y: int, entry_max_lines: int) -> None:
        _y = entry_start_y
        line_count: int = 1
        
        if not len(entries):
            self.render_text('EMPTY', '#EEE1C5' if not self.hovering else '#F7EDD9', (ENTRY_START_X, _y))
            return
        
        for _file in entries:
            _x = ENTRY_START_X
            for word in self.get_entry(_file):
                if _x + self.font.size(word)[0] > ENTRY_X_BOUND:
                    _x = ENTRY_INDENT_X
                    _y += ENTRY_INCREASE
                    line_count += 1
                    
                if line_count == entry_max_lines:
                    self.render_text('...', '#EEE1C5' if not self.hovering else '#F7EDD9', (ENTRY_START_X, _y))
                    return
                    
                self.render_text(word, '#EEE1C5' if not self.hovering else '#F7EDD9', (_x, _y))
                _x += self.font.size(word + ' ')[0]
            
            _y += ENTRY_INCREASE
            line_count += 1
    
    def draw(self, x: int, y: int, y_offset: int) -> None:
        self.rect = self.image.get_rect(topleft=(x, y))

        self.image.blit(self.background, (0, 0))
        
        if self.fontTitle.size(self.name)[0] >= self.TILE_MAX_WIDTH:
            name: list[str] = []
            for char in self.name:
                if self.fontTitle.size(''.join(name))[0] >= self.TILE_MAX_WIDTH:
                    break
                name += char
                
            name.pop()
            name.pop()
            name.pop()
            
            name = ''.join(name)
            name += '...'
            
            self.image.blit(self.fontTitle.render(name, True, '#000000'), (ENTRY_START_X, y_offset + 1))
            self.image.blit(self.fontTitle.render(name, True, '#CCCCCC' if not self.hovering else '#dedede'), (ENTRY_START_X, y_offset))
        
            return

        self.image.blit(self.fontTitle.render(self.name, True, '#000000'), (ENTRY_START_X, y_offset + 1))
        self.image.blit(self.fontTitle.render(self.name, True, '#CCCCCC' if not self.hovering else '#dedede'), (ENTRY_START_X, y_offset))
        
    def context_menu(self) -> None:
        if not self.hovering: 
            return
        
        event_bus.sign('context_menu', {
            '': None,
            'Change Name': self.change_name,
            'Delete': self.delete
        }, True)
    
    def change_name(self) -> None:
        event_bus.sign('context_menu', {})
        event_bus.sign('ui_window', RenameElement(self))

    def delete(self):
        event_bus.sign('delete_file', self)

    def no_hover(self):
        if not self.hovering:
            return
        self.hovering = False

    def hover(self):
        self.hovering = True
        
    def rename(self, text: str):
        pass
        