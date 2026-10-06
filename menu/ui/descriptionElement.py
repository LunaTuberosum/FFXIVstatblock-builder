import pygame

from singletons.dataBus import data_bus

from ui.uiElement import UIElement

from uiComponents.button import Button
from uiComponents.textBox import TextBox


ELEMENT_SIZE: tuple[int, int] = (560, 290)
W_HALF: int = 305
H_HALF: int = 100

class DescriptionElement(UIElement):
    def __init__(self, m_file: object):
        screen = pygame.display.get_surface()
        
        super().__init__(
            name='Description',
            title='Description',
            size=ELEMENT_SIZE,
            pos=(
                (screen.size[0] / 2) - W_HALF,
                (screen.size[1] / 2) - H_HALF,
            )
        )
        
        from menu.encounter import Encounter
        self.m_file: Encounter = m_file
        
        textbox: TextBox = self.add_component(
            'Desc_Text',
            TextBox(
                pos=(50, 80),
                size=(450, 4)
            )
        )
        
        textbox.change_text(self.m_file.encounter_info['desc'])
        textbox.set_can_format(False)
        
        self.add_component(
            'Close',
            Button(
                pos=(30, 225),
                size=(198, 38),
                image=f'.\\assets\\ui\\{data_bus.sign('get_theme')}\\icons\\button.png',
                image_hover=f'.\\assets\\ui\\{data_bus.sign('get_theme')}\\icons\\button_hover.png',
                command=self.close,
                text='Close'
            )
        )
        
        self.add_component(
            'Confirm',
            Button(
                pos=(332, 225),
                size=(198, 38),
                image=f'.\\assets\\ui\\{data_bus.sign('get_theme')}\\icons\\button.png',
                image_hover=f'.\\assets\\ui\\{data_bus.sign('get_theme')}\\icons\\button_hover.png',
                command=self.change_desc,
                text='Confirm'
            )
        )
        
    def draw(self, screen: pygame.Surface) -> None:
        super().draw(screen)
        
        if self.pos[0] != (screen.size[0] / 2) - W_HALF \
        or self.pos[1] != (screen.size[1] / 2) - H_HALF:
                    
            self.pos = (
                (screen.size[0] / 2) - W_HALF,
                (screen.size[1] / 2) - H_HALF
            )
        
        self.render_text('Description', '#C2C2C2', (25, 55))
        
        screen.blit(self.image, self.pos)
        
        for comp in self.components.values():
            comp.draw(screen, self.pos)
            
    def change_desc(self):
        self.m_file.redesc(self.get_component('Desc_Text').text)
        self.close()
        
    