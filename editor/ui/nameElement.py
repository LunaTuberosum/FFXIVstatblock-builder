import pygame

from editor.cardComponents.nameComponent import NameComponent

from editor.ui.statCardElement import StatCardElement

from uiComponents.button import Button
from uiComponents.textBox import TextBox
from uiComponents.toggleButtons import ToggleButtons


LEVEL_END = False
LEVEL_TOPRIGHT = True

ELEMENT_SIZE: tuple[int, int] = (550, 280)

class NameElement(StatCardElement[NameComponent]):
    def __init__(self, component) -> None:
        super().__init__(
            name='Name',
            title='Name',
            size=ELEMENT_SIZE,
            pos=(
                pygame.display.get_surface().size[0] - ELEMENT_SIZE[0], 
                30
            ),
            component=component
        )
        
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
                pos=[460, 140],
                size=[30, 32],
                image='.\\assets\\icons\\MinusButton.png',
                image_hover='.\\assets\\icons\\MinusButton_hover.png',
                command=self.minus_level
            )
        )
        
        self.add_component(
            'Level_Toggle',
            ToggleButtons(
                pos=(290, 180),
                size=(200, 25),
                options={
                    'End': self.change_level_position,
                    'Top Right': self.change_level_position
                },
                default='Top Right' if self.component.level_position == LEVEL_TOPRIGHT else 'End'
            )
        )
        
    def draw(self, screen: pygame.Surface) -> None:
        super().draw(screen)
            
        self.image.blit(self.text_face)
        
        screen.blit(self.image, self.pos)
        
        for comp in self.components.values():
            comp.draw(screen, self.pos)
            
    def apply(self) -> None:
        self.component.name = self.get_component('Name_Text').text
        self.component.level = self.get_component('Level_Text').text
        
        level_toggle: ToggleButtons = self.get_component('Level_Toggle')
        if level_toggle.button_selected.text == 'End':
            self.component.level_position = LEVEL_END
        elif level_toggle.button_selected.text == 'Top Right':
            self.component.level_position = LEVEL_TOPRIGHT
            
        self.component.refresh()
            
    def add_level(self) -> None:
        if not (textbox := self.get_component('Level_Text')).text.isnumeric():
            return
        
        textbox.change_text(str(int(textbox.text) + 10))
    
    def minus_level(self) -> None:
        if not (textbox := self.get_component('Level_Text')).text.isnumeric():
            return
        
        textbox.change_text(str(int(textbox.text) - 10))
        
    def change_level_position(self, text_pos: str) -> None:
        self.get_component('Level_Toggle').set_option(text_pos)
        
    def _render_text_face(self):
        super()._render_text_face()
        
        self.render_text('Name', '#C2C2C2', (25, 55))

        self.render_text('Character Name', '#EEE1C5', (50, 80))

        self.render_text('Level', '#C2C2C2', (25, 115))

        self.render_text('Character Level', '#EEE1C5', (50, 140))

        self.render_text('Level Position', '#EEE1C5', (50, 175))