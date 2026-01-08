import pygame

from editor.cardComponents.abilityComponent import AbilityComponent

from editor.ui.statCardElement import StatCardElement

from uiComponents.textBox import TextBox
from uiComponents.toggleButtons import ToggleButtons


ELEMENT_SIZE: tuple[int, int] = (580, 590)

class AbilityElement(StatCardElement[AbilityComponent]):
    def __init__(self, component) -> None:
        super().__init__(
            name='Ability',
            title='Ability',
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
                size=(300, 1)
            )
        ).change_text(self.component.name)
        
        self.add_component(
            'INVK_Toggle',
            ToggleButtons(
                pos=(380, 145),
                size=(200, 25),
                options={
                    'Off': None,
                    'On': None
                },
                default='On' if self.component.invk else 'Off'
            )
        )
        
        self.add_component(
            'Type_Text',
            TextBox(
                pos=(220, 200),
                size=(300, 2)
            )
        ).change_text(self.component.types)
        self.get_component('Type_Text').set_can_format(False)
        
        self.add_component(
            'Extra_Text',
            TextBox(
                pos=(40, 420),
                size=(480, 3)
            )
        ).change_text(self.component.extra_text)
        self.get_component('Extra_Text').set_can_format(False)
        
    def draw(self, screen: pygame.Surface) -> None:
        super().draw(screen)
            
        self.image.blit(self.text_face)
        
        screen.blit(self.image, self.pos)
        
        for comp in self.components.values():
            comp.draw(screen, self.pos)
            
    def _render_text_face(self):
        super()._render_text_face()
        
        self.render_text('Name', '#C2C2C2', (25, 55))
        self.render_text('Ability Name', '#EEE1C5', (50, 80))

        self.render_text('Invoked', '#C2C2C2', (25, 115))
        self.render_text('Is Invoked', '#EEE1C5', (50, 140))
        
        self.render_text('Types', '#C2C2C2', (25, 175))
        self.render_text('Ability Types', '#EEE1C5', (50, 200))
        
        self.render_text('Effects', '#C2C2C2', (25, 275))
        self.render_text('Edit Effects', '#EEE1C5', (50, 300))
        
        self.render_text('Marker', '#C2C2C2', (25, 335))
        self.render_text('Edit Marker', '#EEE1C5', (50, 360))
        
        self.render_text('Extra Text', '#C2C2C2', (25, 395))