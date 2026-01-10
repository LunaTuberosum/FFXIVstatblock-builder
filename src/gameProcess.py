from typing import Callable
import pygame

from singletons.eventBus import event_bus
from singletons.keyBus import key_bus

from src.contextMenu import ContextMenu
from src.keyHandler import KeyHandler
from src.mouseHandler import MouseHandler

from ui.confirmElement import ConfirmElement
from ui.escapeMenu import EscapeMenu
from ui.uiElement import UIElement


class GameProcess():
    def __init__(self, main: object) -> None:
        from src.gameLoop import GameLoop
        self.main: GameLoop = main
        
        self.key_handler: KeyHandler = KeyHandler()
        self.mouse_handler: MouseHandler = MouseHandler()
        
        self.ui_window: UIElement = None
        self.hold_window: list[UIElement] = []
        self.context_menu: ContextMenu = None
        
        self.hover_object: object = None
        
        self.events: list[pygame.Event] = []
        
        self.setup_bus_calls()
        
    def setup_bus_calls(self) -> None:
        event_bus.register('context_menu', self.create_context_menu)
        event_bus.register('ui_window', self.create_ui_window)
        
        key_bus.register('esc_down', self.escape_menu)
        
    def deregister(self) -> None:
        event_bus.deregister('context_menu', self.create_context_menu)
        event_bus.deregister('ui_window', self.create_ui_window)
        
        key_bus.deregister('esc_down', self.escape_menu)
        
    def is_event(self, event_id: int) -> pygame.Event:
        for event in self.events:
            if event.type == event_id:
                return event
    
    def create_context_menu(self, context_options: dict[str, Callable[[None], None]], addative: bool = False) -> None:
        if not context_options:
            if self.context_menu:
                self.context_menu.deregister()
                
            self.context_menu = None
            return
        
        if addative and self.context_menu:
            self.context_menu.add_options(context_options)
            return
        
        if self.context_menu:
            self.context_menu.deregister()
        
        self.context_menu = ContextMenu(self.mouse_handler.mouse_pos, 186, context_options)
        
    def create_ui_window(self, window: UIElement, hold_window: bool = False) -> None:
        event_bus.sign('context_menu', {})
        
        if self.ui_window and not hold_window:
            self.ui_window.deregister()
            
        if hold_window:
            self.hold_window.append(self.ui_window)
        
        if not window:
            self.ui_window = None
            
            if self.hold_window:
                self.ui_window = self.hold_window.pop()
                
            return
            
        window.hover()
        self.ui_window = window
        
    def update(self) -> None:
        self.hover_object = None
        
        self.main.clock.tick(self.main.display.get_framerate())
        self.events = pygame.event.get()
        
        self.key_handler.handle_keys()
        if self.key_handler.textbox:
            if down := self.is_event(pygame.KEYDOWN):
                self.key_handler.textbox.typing(down.unicode)
                
                if pygame.key.get_mods() & pygame.KMOD_CTRL and down.key == pygame.K_v:
                    key_bus.sign('paste')
                    
                if pygame.key.get_mods() & pygame.KMOD_CTRL and down.key == pygame.K_c:
                    key_bus.sign('copy')
                    
                if pygame.key.get_mods() & pygame.KMOD_CTRL and down.key == pygame.K_b:
                    key_bus.sign('toggle_bold')
                    
                if pygame.key.get_mods() & pygame.KMOD_CTRL and down.key == pygame.K_i:
                    key_bus.sign('toggle_italic')
                
                if down.key == pygame.K_LEFT:
                    key_bus.sign('left_arrow_down')
                    
                if down.key == pygame.K_UP:
                    key_bus.sign('up_arrow_down')
                    
                if down.key == pygame.K_DOWN:
                    key_bus.sign('down_arrow_down')
                
                if down.key == pygame.K_RIGHT:
                    key_bus.sign('right_arrow_down')
            
        self.mouse_handler.handle_mouse(self.events)
        
        if self.ui_window:
            self.ui_window.no_hover()
            
            for comp in self.ui_window.components.values():
                comp.no_hover()
                
                if comp.is_hover(self.mouse_handler.mouse_pos):
                    self.hover_object = comp
                    self.ui_window.hover()
            
            if self.ui_window.rect.collidepoint(self.mouse_handler.mouse_pos) and not self.hover_object:
                self.hover_object = self.ui_window
                
        if self.context_menu:
            self.context_menu.no_hover()
            
            for option in self.context_menu.options:
                option.no_hover()
                
                if option.rect.collidepoint(self.mouse_handler.mouse_pos) and not self.hover_object:
                    self.hover_object = option
                    self.context_menu.hover()
            
            if self.context_menu.rect.collidepoint(self.mouse_handler.mouse_pos) and not self.hover_object:
                self.hover_object = self.context_menu
                
        if self.is_event(pygame.QUIT):
            self.quit()
            
    def quit(self) -> None:
        def confirm():
            event_bus.sign('quit')
                    
        event_bus.sign('ui_window', 
            ConfirmElement(
                'Are you sure you want to exit?',
                confirm,
                confirm_text='Exit',
                cancel_text='Stay'
            )
        )
        
    def escape_menu(self) -> None:
        if isinstance(self.ui_window, EscapeMenu):
            event_bus.sign('ui_window', None)
            return
        
        event_bus.sign('ui_window', 
            EscapeMenu(
                self.menu_options()
            )
        )
        
    def menu_options(self) -> dict[str, Callable[[None], None]]:
        return {}
    
    def draw(self) -> None:
        if self.context_menu:
            self.context_menu.draw(self.main.get_screen())
            
        if self.ui_window:
            self.ui_window.draw(self.main.get_screen())
        
        self.main.display.draw()