import pygame

from ui.uiElement import UIElement

from uiComponents.button import Button
from uiComponents.textBox import TextBox


class StatCardElement[T](UIElement):
    def __init__(self, name: str, title: str, size: tuple[int, int], pos: tuple[int, int], component: T, write_config: bool = True):
        super().__init__(name, title, size, pos, write_config)
        
        self.component: T = component
        
        self.text_face: pygame.Surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self._render_text_face()
        
        self.add_component(
            'Apply',
            Button(
                pos=(30, self.size[1] - 65),
                size=(198, 38),
                image='.\\assets\\icons\\button.png',
                image_hover='.\\assets\\icons\\button_hover.png',
                command=self.apply,
                text='Apply'
            )
        )
        
        self.add_component(
            'Confirm',
            Button(
                pos=(self.size[0] - 228, self.size[1] - 65),
                size=(198, 38),
                image='.\\assets\\icons\\button.png',
                image_hover='.\\assets\\icons\\button_hover.png',
                command=self.confirm,
                text='Confirm'
            )
        )
        
    def check_off_click(self) -> None:
        pass
        
    def draw(self, screen: pygame.Surface) -> None:
        super().draw(screen)
        
        if self.pos[0] != screen.size[0] - self.size[0]:
                    
            self.pos = (
                pygame.display.get_surface().size[0] - self.size[0], 
                30
            )
        
    def apply(self) -> None:
        pass
    
    def confirm(self) -> None:
        self.apply()
        
        self.close()
        
    def tab(self, textbox: TextBox) -> None:
        current_box: TextBox = None
        next_box: TextBox = None
        for component in self.components.values():
            if not isinstance(component, TextBox):
                continue
            
            if component == textbox:
                current_box = component
                continue
            
            if current_box:
                next_box = component
                break
                
        if not next_box:
            current_box.end_field()
            return
                
        current_box.end_field()
        next_box.activate()
    
    def render_text(self, text: str, color: str, pos: tuple[int, int]) -> None:
        self.text_face.blit(self.font.render(text, True, '#000000'), (pos[0], pos[1] + 1))
        self.text_face.blit(self.font.render(text, True, color), (pos[0], pos[1]))
    
    def _render_text_face(self) -> None:
        self.text_face.fill((0,0,0,0))