import pygame

from editor.editor import Editor

from menu.encounter import Encounter
from menu.folder import Folder

from singletons import resourceHandler

from singletons.eventBus import event_bus

from ui.uiElement import UIElement


class EncounterEditor(Editor):
    def __init__(self, main: object, encounter: Encounter, current_folder: Folder, prev_folders: list[Folder]) -> None:
        self.encounter: Encounter = encounter
        print(self.encounter.encounter_info)
        
        super().__init__(main, current_folder, prev_folders)
        
    def setup_bus_calls(self) -> None:
        super().setup_bus_calls()
        
    def deregister(self) -> None:
        super().deregister()
        
    def editor_context_menu(self) -> None:
        if self.ui_window and self.ui_window.hovering:
            return
        
        event_bus.sign('context_menu', {
            'Add --': None,
        })
        
        super().editor_context_menu()
        
    def _update_cursor(self) -> bool:
        if super()._update_cursor():
            return True
            
        if self.hover_object and not isinstance(self.hover_object, UIElement): 
            pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))
            return True
            
        pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))
        return False
    
    def update(self) -> None:
        super().update()
        
        if self.hover_object:
            self.hover_object.hover()
            
        self._update_cursor()
        
        self.draw()
        
    def draw(self) -> None:
        screen: pygame.Surface = self.main.get_screen()
        screen_rect: pygame.Rect = pygame.Rect((0, 0), screen.size)
        
        screen.fill('#313031')
        
        super().draw()
        
    # def load(self) -> None:
    #     for card in self.sheet.sheet_info.values():
    #         if not isinstance(card, dict): 
    #             if isinstance(card, list):
    #                 self.text_colors = card
    #             continue
            
    #         s_card: StatCard = StatCard(card['width'], card['height'])
            
    #         s_card.load(card['components'])
            
    #         self.stat_cards.append(s_card)
            
    def save(self) -> None:
        super().save()
        
        save_dict: dict = {
            'type': 'encounter',
            'version': '1.0',
            'colors': self.get_colors(),
            'desc': self.encounter.encounter_info['desc']
        }
            
        resourceHandler.save_json(f'.\\saves\\{self.encounter.path}\\{self.encounter.name}.json', save_dict)
        