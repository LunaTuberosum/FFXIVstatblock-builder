import pygame

from singletons.eventBus import event_bus

from ui.uiElement import UIElement

from uiComponents.button import Button
from uiComponents.textBox import TextBox


ELEMENT_SIZE: tuple[int, int] = (610, 200)
W_HALF: int = 305
H_HALF: int = 100

class RenameElement(UIElement):
    def __init__(self, m_file: object):
        screen = pygame.display.get_surface()
        
        super().__init__(
            name='Rename',
            title='Rename',
            size=ELEMENT_SIZE,
            pos=(
                (screen.size[0] / 2) - W_HALF,
                (screen.size[1] / 2) - H_HALF,
            )
        )
        
        from menu.menuObject import MenuObject
        self.m_file: MenuObject = m_file
        
        textbox: TextBox = self.addComponent(
            'Name_Text',
            TextBox(
                pos=(220, 80),
                size=(270+60, 1)
            )
        )
        textbox.change_text(self.m_file.name)
        
        self.addComponent(
            'Close',
            Button(
                pos=(30, 135),
                size=(198, 38),
                image='.\\assets\\icons\\button.png',
                image_hover='.\\assets\\icons\\button_hover.png',
                command=self.close,
                text='Close'
            )
        )
        
        self.addComponent(
            'Confirm',
            Button(
                pos=(382, 135),
                size=(198, 38),
                image='.\\assets\\icons\\button.png',
                image_hover='.\\assets\\icons\\button_hover.png',
                command=self.change_name,
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
        
        self.render_text('Name', '#C2C2C2', (25, 55))
        
        self.render_text(f'{self.m_file.__class__.__name__} Name', '#EEE1C5', (50, 80))
            
        screen.blit(self.image, self.pos)
        
        for comp in self.components.values():
            comp.draw(screen, self.pos)
            
    def change_name(self):
        self.m_file.rename(self.getComponent('Name_Text').text)
        self.close()