import pygame

from statcardEditor.cardComponents.cardComponent import CardComponent

from statcardEditor.statcard import StatCard

from menu.folder import Folder
from menu.sheet import Sheet

from src.editorCore import Editor

from singletons import resourceHandler

from singletons.eventBus import event_bus

from ui.uiElement import UIElement


class StatcardEditor(Editor):
    def __init__(self, main: object, sheet: Sheet, current_folder: Folder, prev_folders: list[Folder]) -> None:
        self.sheet: Sheet = sheet
        self.stat_cards: list[StatCard] = []
        
        super().__init__(main, current_folder, prev_folders)
        
    def setup_bus_calls(self) -> None:
        super().setup_bus_calls()
        
        event_bus.register('add_card', self.new_card)
        event_bus.register('delete_card', self.delete_card)
        
        event_bus.register('move_card', self.move_card)
        
    def deregister(self) -> None:
        super().deregister()
        
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
        })
        
        super().editor_context_menu()
        
    def _update_cursor(self) -> bool:
        if super()._update_cursor():
            return True
            
        if self.hover_object and isinstance(self.hover_object, CardComponent):
            pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))
            return True
            
        if self.hover_object and not isinstance(self.hover_object, UIElement): 
            pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))
            return True
            
        pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))
        return False
            
    def update(self) -> None:
        super().update()
            
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
            
        self._update_cursor()
        
        self.draw()
        
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
        from statcardEditor.ui.addCardElement import AddCardElement
        event_bus.sign('ui_window', AddCardElement())
        
    def save(self) -> None:
        super().save()
        
        save_dict: dict = {
            'type': 'statsheet',
            'version': '2.2',
            'colors': self.get_colors(),
        }
        for index, card in enumerate(self.stat_cards):
            save_dict[str(index)] = card.save()
            
        resourceHandler.save_json(f'.\\saves\\{self.sheet.path}\\{self.sheet.name}.json', save_dict)
        
    def export(self) -> None:
        super().export()
        
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