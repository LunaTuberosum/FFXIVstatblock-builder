from typing import Callable
import pygame

from singletons.eventBus import event_bus
from singletons.keyBus import key_bus
from singletons.dataBus import data_bus

from src.contextMenu import ContextMenu
from src.display import Display, ScreenOptions
from src.keyHandler import KeyHandler
from src.mouseHandler import MouseHandler
from src.soundEffectHandler import SoundeEffectHandler

from ui.confirmElement import ConfirmElement
from ui.escapeMenu import EscapeMenu
from ui.uiElement import UIElement
from uiComponents.dropdown import Dropdown


class GameProcess():
    def __init__(self, main: object) -> None:
        from src.gameLoop import GameLoop
        self.main: GameLoop = main
        
        self.key_handler: KeyHandler = KeyHandler()
        self.mouse_handler: MouseHandler = MouseHandler()
        
        self.sound_handler: SoundeEffectHandler = SoundeEffectHandler()
        self.sound_handler.set_volume(self.main.display.get_volume())
        
        self.ui_window: UIElement = None
        self.hold_window: list[UIElement] = []
        self.context_menu: ContextMenu = None
        
        self.hover_object: object = None
        
        self.events: list[pygame.Event] = []
        
        self.setup_bus_calls()
        
    def setup_bus_calls(self) -> None:
        event_bus.register('play_se', self.play_se)
        
        event_bus.register('set_master', self.set_master)
        event_bus.register('mute_master', self.mute_master)
        
        event_bus.register('set_resolution', self.set_resolution)
        
        event_bus.register('context_menu', self.create_context_menu)
        event_bus.register('ui_window', self.create_ui_window)
        
        key_bus.register('esc_down', self.escape_menu)
        
        data_bus.register('get_display', self.get_display)
        
        data_bus.register('get_resolution', self.get_resolution)
        data_bus.register('get_fullscreen', self.get_fullscreen)
        data_bus.register('get_fps', self.get_fps)
        data_bus.register('get_monitor', self.get_monitor)
        
    def deregister(self) -> None:
        event_bus.deregister('play_se', self.play_se)
        
        event_bus.deregister('set_master', self.set_master)
        event_bus.deregister('mute_master', self.mute_master)
        
        event_bus.register('set_resolution', self.set_resolution)
        
        event_bus.deregister('context_menu', self.create_context_menu)
        event_bus.deregister('ui_window', self.create_ui_window)
        
        key_bus.deregister('esc_down', self.escape_menu)
        
        data_bus.deregister('get_display', self.get_display)
        
        data_bus.deregister('get_resolution', self.get_resolution)
        data_bus.deregister('get_fullscreen', self.get_fullscreen)
        data_bus.deregister('get_fps', self.get_fps)
        data_bus.deregister('get_monitor', self.get_monitor)
        
    def is_event(self, event_id: int) -> pygame.Event:
        for event in self.events:
            if event.type == event_id:
                return event
    
    def play_se(self, sound_name: str) -> None:
        self.sound_handler.play_se(sound_name)
    
    def set_master(self, volume: float) -> None:
        self.main.display.set_volume(volume)
        self.sound_handler.set_volume(volume)        
        
    def mute_master(self) -> None:
        self.main.display.set_volume(0)
        self.sound_handler.set_volume(0)    
        
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
        
    def create_ui_window(self, window: UIElement, hold_window: bool = False, force: bool = False) -> None:
        event_bus.sign('context_menu', {})
        
        if self.ui_window and not hold_window:
            self.ui_window.deregister()
            
        if hold_window:
            self.hold_window.append(self.ui_window)
            
        if force:
            self.hold_window = []

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
                
        if self.context_menu:
            self.context_menu.no_hover()
            
            for option in self.context_menu.options:
                
                if option.rect.collidepoint(self.mouse_handler.mouse_pos) and not self.hover_object:
                    self.hover_object = option
                    self.context_menu.hover()
                    
                else:
                    option.no_hover()
            
            if self.context_menu.rect.collidepoint(self.mouse_handler.mouse_pos) and not self.hover_object:
                self.hover_object = self.context_menu
                
        if self.ui_window:
            self.ui_window.no_hover()
            
            for comp in self.ui_window.components.values():
                
                if comp.is_hover(self.mouse_handler.mouse_pos):
                    if isinstance(comp, Dropdown):
                        self.hover_object = comp
                        self.ui_window.hover()
                        continue
                    
                    if self.hover_object:
                        comp.no_hover()
                        continue
                    
                    self.hover_object = comp
                    self.ui_window.hover()
                    
                else: 
                    comp.no_hover()
            
            if self.ui_window.is_hover(self.mouse_handler.mouse_pos) and not self.hover_object:
                self.hover_object = self.ui_window
                
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
            ),
            False,
            True
        )
        
    def escape_menu(self) -> None:
        if isinstance(self.ui_window, EscapeMenu):
            event_bus.sign('ui_window', None)
            return
        
        event_bus.sign('ui_window', 
            EscapeMenu(
                self.menu_options()
            ),
            False,
            True
        )
        
    def menu_options(self) -> dict[str, Callable[[None], None]]:
        return {}
    
    def draw(self) -> None:            
        if self.ui_window:
            self.ui_window.draw(self.main.get_screen())
            
        if self.context_menu:
            self.context_menu.draw(self.main.get_screen())
        
        self.main.display.draw()
        
    def set_resolution(self, resolution: tuple[int, int]) -> None:
        self.main.display.set_resolution(resolution[0], resolution[1])
        
    def get_display(self) -> Display:
        return self.main.display
        
    def get_resolution(self) -> tuple[int, int]:
        return self.main.display.get_resolution()
    
    def get_fullscreen(self) -> ScreenOptions:
        return self.main.display.get_fullscreen()
        
    def get_fps(self) -> int:
        return round(self.main.clock.get_fps())
    
    def get_monitor(self) -> int:
        return self.main.display.get_monitor()