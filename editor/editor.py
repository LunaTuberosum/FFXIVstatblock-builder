from pprint import pprint
from typing import Callable
import pygame

from editor.cardComponents.cardComponent import CardComponent

from editor.statcard import StatCard

from menu.folder import Folder
from menu.sheet import Sheet

from singletons import resourceHandler

from singletons.dataBus import data_bus
from singletons.eventBus import event_bus
from singletons.keyBus import key_bus

from src.gameProcess import GameProcess

from ui.confirmElement import ConfirmElement
from ui.uiElement import UIElement


class Editor(GameProcess):
    def __init__(self, main: object, sheet: Sheet, current_folder: Folder, prev_folders: list[Folder]) -> None:
        super().__init__(main)
        
        self.sheet: Sheet = sheet
        self.current_folder: Folder = current_folder
        self.prev_folders: list[Folder] = prev_folders
        
        self.pan: tuple[int, int] = (0, 0)
        self.can_pan: dict[str, bool] = {
            'left_down': False,
            'space_down': False
        }
        
        self.text_colors: list[str] = []
        
        self.stat_cards: list[StatCard] = []
        self.load()
        
    def setup_bus_calls(self) -> None:
        super().setup_bus_calls()
        
        key_bus.register('mouse_left_down', self.on_click)
        key_bus.register('mouse_left_up', self.on_release)
        
        key_bus.register('mouse_right_down', self.editor_context_menu)
        
        key_bus.register('space_down', self.space_down)
        key_bus.register('space_up', self.space_up)
        
        data_bus.register('get_colors', self.get_colors)
        data_bus.register('add_color', self.add_color)
        
        event_bus.register('add_card', self.new_card)
        event_bus.register('delete_card', self.delete_card)
        
        event_bus.register('move_card', self.move_card)
        
    def deregister(self) -> None:
        super().deregister()
        
        key_bus.deregister('mouse_left_down', self.on_click)
        key_bus.deregister('mouse_left_up', self.on_release)
        
        key_bus.deregister('mouse_right_down', self.editor_context_menu)
        
        key_bus.deregister('space_down', self.space_down)
        key_bus.deregister('space_up', self.space_up)
        
        data_bus.deregister('get_colors', self.get_colors)
        data_bus.deregister('add_color', self.add_color)
        
        event_bus.deregister('add_card', self.new_card)
        event_bus.deregister('delete_card', self.delete_card)
        
        event_bus.deregister('move_card', self.move_card)
        
        for card in self.stat_cards:
            card.deregister()
        
    def editor_context_menu(self) -> None:
        if self.ui_window and self.ui_window.hovering:
            return
        
        event_bus.sign('context_menu', {
            'Add Card': self.add_card,
            'Save': self.save,
            'Export as PNG': self.export
        })
        
    def get_colors(self) -> list[str]:
        return self.text_colors
    
    def add_color(self, color: str) -> None:
        self.text_colors.append(color.strip('#'))
        
    def space_down(self) -> None:
        self.can_pan['space_down'] = True
        
    def space_up(self) -> None:
        self.can_pan['space_down'] = False
        
    def on_click(self) -> None:
        self.can_pan['left_down'] = True
        
    def on_release(self) -> None:
        self.can_pan['left_down'] = False
        
    def __update_cursor(self) -> None:
        if self.can_pan['space_down']:
            pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_SIZEALL))
            
        elif self.hover_object and isinstance(self.hover_object, CardComponent):
            pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))
            
        elif self.hover_object and not isinstance(self.hover_object, UIElement): 
            pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))
            
        else:
            pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))
    def update(self) -> None:
        super().update()
        
        if self.can_pan['left_down'] and self.can_pan['space_down'] and (event := self.is_event(pygame.MOUSEMOTION)):
            self.pan = (
                min(self.pan[0] + event.rel[0], 0), 
                min(self.pan[1] + event.rel[1], 0)
            )
            
        for card in self.stat_cards:
            card.no_hover()
            
            for component in card.components.values():
                component.no_hover()
                
                if component.rect.collidepoint(self.mouse_handler.mouse_pos) and not self.hover_object:
                    card.hover()
                    self.hover_object = component
                    
            if card.rect.collidepoint(self.mouse_handler.mouse_pos) and not self.hover_object:
                self.hover_object = card
        
        if self.hover_object:
            self.hover_object.hover()
            
        self.__update_cursor()
        
        self.draw()
        
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
        
    def draw(self) -> None:
        screen: pygame.Surface = self.main.get_screen()
        screen_rect: pygame.Rect = pygame.Rect((0, 0), screen.size)
        
        screen.fill('#313031')
        
        x: int = 40
        for card in self.stat_cards:
            card.update(self.pan, x)
            if screen_rect.colliderect(card.rect):
                card.draw(screen)
                
            x += card.size[0] + 20
        
        super().draw()
        
    def new_card(self, card: StatCard) -> None:
        self.stat_cards.append(card)
        
    def load(self) -> None:
        for card in self.sheet.sheet_info.values():
            if not isinstance(card, dict): 
                if isinstance(card, list):
                    self.text_colors = card
                continue
            
            s_card: StatCard = StatCard(card['width'], card['height'])
            
            s_card.load(card['components'])
            
            self.stat_cards.append(s_card)
            
    def add_card(self) -> None:
        from editor.ui.addCardElement import AddCardElement
        event_bus.sign('ui_window', AddCardElement())
        
    def save(self) -> None:
        save_dict: dict = {
            'version': '2.0',
            'colors': self.get_colors(),
        }
        for index, card in enumerate(self.stat_cards):
            save_dict[str(index)] = card.save()
            
        pprint(save_dict)    
        
        resourceHandler.save_json(f'.\\saves\\{self.sheet.path}\\{self.sheet.name}.json', save_dict)
        
    def export(self) -> None:
        event_bus.sign('context_menu', None)
        
        width: int = 40
        height: int = 40
        
        for card in self.stat_cards:
            width += card.size[0] + 20
            
            height = max(height, card.size[1] + 40)
            
        export_trans: pygame.Surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        export: pygame.Surface = pygame.Surface((width, height), pygame.SRCALPHA)
        export.fill('#313031')
        
        x: int = 40
        for card in self.stat_cards:
            for component in card.components.values():
                component.no_hover()
            
            card.update((0, 0), x)
            card.draw(export_trans)
            card.draw(export)
            
            x += card.size[0] + 20
            
        try:
            resourceHandler.save_image(export_trans, f'.\\exports\\{self.sheet.name}\\export_transparent.png')
            
            resourceHandler.save_image(export, f'.\\exports\\{self.sheet.name}\\export.png')
        except:
            resourceHandler.save_dir('.\\exports\\', self.sheet.name)
            
            resourceHandler.save_image(export_trans, f'.\\exports\\{self.sheet.name}\\export_transparent.png')
            
            resourceHandler.save_image(export, f'.\\exports\\{self.sheet.name}\\export.png')
            
        
    def delete_card(self, card: StatCard) -> None:
        card.deregister()
        
        self.stat_cards.remove(card)
        
    def move_card(self, card: StatCard, direction: str) -> None:
        card_index: int = self.stat_cards.index(card)
        
        if direction == 'left':
            self.stat_cards.remove(card)
            self.stat_cards.insert(card_index - 1, card)
            
        elif direction == 'right':
            self.stat_cards.remove(card)
            self.stat_cards.insert(card_index + 1, card)