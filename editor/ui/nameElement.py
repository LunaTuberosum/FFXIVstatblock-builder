import pygame

from ui.uiElement import UIElement
from uiComponents.button import Button
from uiComponents.textBox import TextBox


ELEMENT_SIZE: tuple[int, int] = (550, 278)

class NameElement(UIElement):
    def __init__(self, component: object) -> None:
        super().__init__(
            name='Name',
            title='Name',
            size=ELEMENT_SIZE,
            pos=(
                pygame.display.get_surface().size[0] - ELEMENT_SIZE[0], 
                30
            )
        )
        
        from editor.cardComponents.nameComponent import NameComponent
        self.component: NameComponent = component
        
        self.add_component(
            'Name_Text',
            TextBox(
                pos=(220, 80),
                size=(270, 1)
            )
        ).change_text(self.component.name)
        
        self.add_component(
            'Level_Text',
            TextBox(
                pos=(338, 140),
                size=(90, 1)
            )
        ).change_text(self.component.level)
        
        self.add_component(
            'Level_Plus',
            Button(
                pos=[430, 140],
                size=[30, 32],
                image='.\\assets\\icons\\AddButton.png',
                image_hover='.\\assets\\icons\\AddButton_hover.png',
                command=self.add_level
            )
        )
        self.add_component(
            'Level_Minus',
            Button(
                pos=[461, 140],
                size=[30, 32],
                image='.\\assets\\icons\\MinusButton.png',
                image_hover='.\\assets\\icons\\MinusButton_hover.png',
                command=self.minus_level
            )
        )
        
        
        self.add_component(
            'Close',
            Button(
                pos=(30, 215),
                size=(198, 38),
                image='.\\assets\\icons\\button.png',
                image_hover='.\\assets\\icons\\button_hover.png',
                command=self.close,
                text='Close'
            )
        )
        
        self.add_component(
            'Confirm',
            Button(
                pos=(322, 215),
                size=(198, 38),
                image='.\\assets\\icons\\button.png',
                image_hover='.\\assets\\icons\\button_hover.png',
                command=None,
                text='Confirm'
            )
        )
        
    def draw(self, screen: pygame.Surface) -> None:
        super().draw(screen)
        
        if self.pos[0] != screen.size[0] - ELEMENT_SIZE[0]:
                    
            self.pos = (
                pygame.display.get_surface().size[0] - ELEMENT_SIZE[0], 
                30
            )
            
        self.render_text('Name', '#C2C2C2', (25, 55))

        self.render_text('Character Name', '#EEE1C5', (50, 80))

        self.render_text('Level', '#C2C2C2', (25, 115))

        self.render_text('Character Level', '#EEE1C5', (50, 140))

        self.render_text('Level Position', '#EEE1C5', (50, 175))
        
        screen.blit(self.image, self.pos)
        
        for comp in self.components.values():
            comp.draw(screen, self.pos)
            
            
    def add_level(self) -> None:
        pass
    
    def minus_level(self) -> None:
        pass