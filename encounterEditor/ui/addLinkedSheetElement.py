import pygame

from singletons.eventBus import event_bus
from singletons.dataBus import data_bus

from ui.uiElement import UIElement
from uiComponents.button import Button
from uiComponents.fileExplorer import FileExplorer


ELEMENT_SIZE: tuple[int, int] = (460, 500)

class AddLinkedSheetElement(UIElement):
    def __init__(self,  alert: bool = False) -> None:
        self.alert: bool = alert
        
        super().__init__(
            name='AddLinkedSheet',
            title='Add Linked Sheet(s)',
            size=ELEMENT_SIZE,
            pos=(
                (pygame.display.get_surface().size[0] / 2) - (ELEMENT_SIZE[0] / 2), 
                (pygame.display.get_surface().size[1] / 2) - (ELEMENT_SIZE[1] / 2)
            ),
            write_config=False
        )
        
        self.add_component(
            'Explorer',
            FileExplorer(
                pos=(50, 85)
            )
        )
        
        self.add_component(
            'Cancel',
            Button(
                pos=(30, self.size[1] - 65),
                size=(198, 38),
                image=f'.\\assets\\ui\\{data_bus.sign('get_theme')}\\icons\\button.png',
                image_hover=f'.\\assets\\ui\\{data_bus.sign('get_theme')}\\icons\\button_hover.png',
                command=self.cancel,
                text='Cancel'
            )
        )
        
        self.add_component(
            'Confirm',
            Button(
                pos=(self.size[0] - 228, self.size[1] - 65),
                size=(198, 38),
                image=f'.\\assets\\ui\\{data_bus.sign('get_theme')}\\icons\\button.png',
                image_hover=f'.\\assets\\ui\\{data_bus.sign('get_theme')}\\icons\\button_hover.png',
                command=self.confirm,
                text='Confirm'
            )
        )
        
        
        self.text_face: pygame.Surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self._render_text_face()
        
    def check_off_click(self) -> None:
        pass
        
    def play_open(self):
        if self.alert:
            event_bus.sign('play_se', 'notification')
        else:
            event_bus.sign('play_se', 'open_window')
        
    def draw(self, screen: pygame.Surface) -> None:
        super().draw(screen)
            
        self.image.blit(self.text_face)
        
        screen.blit(self.image, self.pos)
        
        for comp in self.components.values():
            comp.draw(screen, self.pos)
            
    def confirm(self) -> None:
        pass
    
    def cancel(self) -> None:
        event_bus.sign('ui_window', None)
        
    def render_text(self, text: str, color: str, pos: tuple[int, int]) -> None:
        self.text_face.blit(self.font.render(text, True, '#000000'), (pos[0], pos[1] + 1))
        self.text_face.blit(self.font.render(text, True, color), (pos[0], pos[1]))
    
    def _render_text_face(self) -> None:
        self.text_face.fill((0,0,0,0))
        
        self.render_text('File Explorer', '#C2C2C2', (25, 55))