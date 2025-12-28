import pygame

from editor.statcard import StatCard
from menu.sheet import Sheet

from singletons import resourceHandler

from singletons.eventBus import event_bus
from singletons.keyBus import key_bus

from src.gameProcess import GameProcess

from ui.confirmElement import ConfirmElement


pygame.font.init()
JUPITER_FONT: pygame.font.Font = resourceHandler.load_font('.\\assets\\fonts\\jupiter_pro_regular.otf', 40)
MIEDINGER: pygame.font.Font = resourceHandler.load_font('assets/fonts/miedinger_medium.ttf', 18)

class Editor( GameProcess):
    def __init__(self, main: object, sheet: Sheet) -> None:
        super().__init__(main)
        
        self.sheet: Sheet = sheet
        
        self.pan: tuple[int, int] = (0, 0)
        self.can_pan: dict[str, bool] = {
            'left_down': False,
            'space_down': False
        }
        
        self.temp = StatCard(3, 1)
        
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
            
        else:
            pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))
        
    def update(self) -> None:
        super().update()
        
        self.__update_cursor()
        
        if self.can_pan['left_down'] and self.can_pan['space_down'] and (event := self.is_event(pygame.MOUSEMOTION)):
            self.pan = (
                min(self.pan[0] + event.rel[0], 0), 
                min(self.pan[1] + event.rel[1], 0)
            )
        
        if self.hover_object:
            self.hover_object.hover()
        
        self.draw()
        
    def quit(self) -> None:
        def confirm():
            event_bus.sign('return_menu')
                    
        event_bus.sign('ui_window', 
            ConfirmElement(
                'Are you sure you want to exit?',
                confirm,
                confirm_text='Exit',
                cancel_text='Stay'
            )
        )
        
    def draw(self) -> None:
        screen: pygame.Surface = self.main.get_screen()
        
        screen.fill('#313031')
        
        self.temp.draw(screen, self.pan, 40)
        
        screen.blit(MIEDINGER.render(str(round(self.main.clock.get_fps(), 1)), True, '#00ff00'), (screen.size[0]- 100, 10))
        
        super().draw()
        