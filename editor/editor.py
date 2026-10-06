from typing import Callable
import pygame

from menu.folder import Folder

from singletons.dataBus import data_bus
from singletons.eventBus import event_bus
from singletons.keyBus import key_bus

from src.gameProcess import GameProcess

from ui.confirmElement import ConfirmElement


class Editor(GameProcess):
    def __init__(self, main: object, current_folder: Folder, prev_folders: list[Folder]) -> None:
        super().__init__(main)
        
        self.current_folder: Folder = current_folder
        self.prev_folders: list[Folder] = prev_folders
        
        self.pan: tuple[int, int] = (0, 0)
        self.can_pan: dict[str, bool] = {
            'left_down': False,
            'space_down': False
        }
        
        self.hori_scroll: bool = False
        
        self.text_colors: list[str] = []
        
        self.load()
        
    def setup_bus_calls(self) -> None:
        super().setup_bus_calls()
        
        key_bus.register('mouse_left_down', self.on_click)
        key_bus.register('mouse_left_up', self.on_release)
        
        key_bus.register('mouse_right_down', self.editor_context_menu)
        
        key_bus.register('space_down', self.space_down)
        key_bus.register('space_up', self.space_up)
        
        key_bus.register('shift_down', self.shift_down)
        key_bus.register('shift_up', self.shift_up)
        
        data_bus.register('get_colors', self.get_colors)
        data_bus.register('add_color', self.add_color)
        
    def deregister(self) -> None:
        super().deregister()
        
        key_bus.deregister('mouse_left_down', self.on_click)
        key_bus.deregister('mouse_left_up', self.on_release)
        
        key_bus.deregister('mouse_right_down', self.editor_context_menu)
        
        key_bus.deregister('space_down', self.space_down)
        key_bus.deregister('space_up', self.space_up)
        
        key_bus.deregister('shift_down', self.shift_down)
        key_bus.deregister('shift_up', self.shift_up)
        
        data_bus.deregister('get_colors', self.get_colors)
        data_bus.deregister('add_color', self.add_color)
        
    def editor_context_menu(self) -> None:
        event_bus.sign('context_menu', {
            '{}': None,
            'Save': self.save,
            'Export as PNG': self.export
        }, True)
        
    def get_colors(self) -> list[str]:
        return self.text_colors
    
    def add_color(self, color: str) -> None:
        self.text_colors.append(color.strip('#'))
        
    def space_down(self) -> None:
        self.can_pan['space_down'] = True
        
    def space_up(self) -> None:
        self.can_pan['space_down'] = False
        
    def shift_down(self) -> None:
        self.hori_scroll = True
        
    def shift_up(self) -> None:
        self.hori_scroll = False
        
    def on_click(self) -> None:
        self.can_pan['left_down'] = True
        
    def on_release(self) -> None:
        self.can_pan['left_down'] = False
        
    def _update_cursor(self) -> bool:
        if self.can_pan['space_down']:
            pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_SIZEALL))
            return True
            
        if self.hori_scroll:
            pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_SIZEWE))
            return True
            
        return False
        
    def update(self) -> None:
        super().update()
        
        if self.can_pan['left_down'] and self.can_pan['space_down'] and (event := self.is_event(pygame.MOUSEMOTION)):
            self.pan = (
                min(self.pan[0] + event.rel[0], 0), 
                min(self.pan[1] + event.rel[1], 0)
            )
        
        if event := self.is_event(pygame.MOUSEWHEEL):
                if self.hori_scroll:
                    self.pan = (
                        min(self.pan[0] + event.y * 40, 0),
                        self.pan[1]
                    )
                else:
                    self.pan = (
                        self.pan[0],
                        min(self.pan[1] + event.y * 40, 0)
                    )
                    
        if pygame.key.get_mods() & pygame.KMOD_CTRL and (key := self.is_event(pygame.KEYDOWN)) and key.key == pygame.K_SPACE:
            self.pan = (0, 0)
            
    def quit(self) -> None:
        def confirm():
            event_bus.sign('quit')
                    
        event_bus.sign('ui_window', 
            ConfirmElement(
                'Are you sure you want to exit?\nYou will loose any unsaved progress.',
                confirm,
                confirm_text='Exit',
                cancel_text='Stay'
            ),
            False,
            True
        )
        
    def menu_return(self) -> None:
        def confirm():
            event_bus.sign('return_menu', self.current_folder, self.prev_folders)
                    
        event_bus.sign('ui_window', 
            ConfirmElement(
                'Are you sure you want to return?\nYou will loose any unsaved progress.',
                confirm,
                confirm_text='Return',
                cancel_text='Stay'
            )
        )
        
    def menu_options(self) -> dict[str, Callable[[None], None]]:
        return {
            'Save': self.save,
            'Return to Menu': self.menu_return,
            'Exit Program': self.quit
        }
        
    def load(self) -> None:
        pass
    
    def save(self) -> None:
        event_bus.sign('context_menu', None)
        
    def export(self) -> None:
        event_bus.sign('context_menu', None)