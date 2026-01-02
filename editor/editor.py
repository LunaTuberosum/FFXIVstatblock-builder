from typing import Callable
import pygame

from editor.cardComponents.cardComponent import CardComponent

from editor.statcard import StatCard

from menu.sheet import Sheet

from singletons import resourceHandler

from singletons.eventBus import event_bus
from singletons.keyBus import key_bus

from src.gameProcess import GameProcess

from ui.confirmElement import ConfirmElement


pygame.font.init()
JUPITER_FONT: pygame.Font = resourceHandler.load_font('.\\assets\\fonts\\jupiter_pro_regular.otf', 40)
MIEDINGER: pygame.Font = resourceHandler.load_font('assets/fonts/miedinger_medium.ttf', 18)

class Editor( GameProcess):
    def __init__(self, main: object, sheet: Sheet) -> None:
        super().__init__(main)
        
        self.sheet: Sheet = sheet
        
        self.pan: tuple[int, int] = (0, 0)
        self.can_pan: dict[str, bool] = {
            'left_down': False,
            'space_down': False
        }
        
        self.stat_cards: list[StatCard] = []
        self.load()
        
    def setup_bus_calls(self) -> None:
        super().setup_bus_calls()
        
        key_bus.register('mouse_left_down', self.on_click)
        key_bus.register('mouse_left_up', self.on_release)
        
        key_bus.register('space_down', self.space_down)
        key_bus.register('space_up', self.space_up)
        
    def deregister(self) -> None:
        super().deregister()
        
        key_bus.deregister('mouse_left_down', self.on_click)
        key_bus.deregister('mouse_left_up', self.on_release)
        
        key_bus.deregister('space_down', self.space_down)
        key_bus.deregister('space_up', self.space_up)
        
        for card in self.stat_cards:
            card.deregister()
        
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
            for component in card.components.values():
                component.no_hover()
                
                if component.rect.collidepoint(self.mouse_handler.mouse_pos) and not self.hover_object:
                    self.hover_object = component
        
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
            )
        )
        
    def menu_return(self) -> None:
        def confirm():
            event_bus.sign('return_menu')
                    
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
            'Save': self.quit,
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
        
        screen.blit(MIEDINGER.render(str(round(self.main.clock.get_fps(), 1)), True, '#00ff00'), (screen.size[0]- 100, 10))
        
        super().draw()
        
    def load(self) -> None:
        for card in self.sheet.sheet_info.values():
            if card == '2.0': continue
            
            s_card: StatCard = StatCard(card['width'], card['height'])
            
            s_card.load(card['components'])
            
            self.stat_cards.append(s_card)