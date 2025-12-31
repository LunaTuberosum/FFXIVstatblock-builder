import pygame

from editor.cardComponents.traitComponent import TraitComponent

from editor.ui.statCardElement import StatCardElement

from uiComponents.textBox import TextBox


ELEMENT_SIZE: tuple[int, int] = (580, 370)

class TraitElement(StatCardElement[TraitComponent]):
    def __init__(self, component) -> None:
        super().__init__(
            name='Trait',
            title='Trait',
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
            'Desc_Text',
            TextBox(
                pos=(40, 140),
                size=(480, 5)
            )
        ).change_text(self.component.desc, self.component.formating)
        
    def draw(self, screen: pygame.Surface) -> None:
        super().draw(screen)
            
        self.image.blit(self.text_face)
        
        screen.blit(self.image, self.pos)
        
        for comp in self.components.values():
            comp.draw(screen, self.pos)
            
    def apply(self) -> None:
        self.component.name = self.get_component('Name_Text').text
        self.component.desc = self.get_component('Desc_Text').text
        self.component.formating = self.get_component('Desc_Text').formating
        
        self.component.refresh()
        
    def _render_text_face(self):
        super()._render_text_face()
        
        self.render_text('Name', '#C2C2C2', (25, 55))

        self.render_text('Trait Name', '#EEE1C5', (50, 80))

        self.render_text('Description', '#C2C2C2', (25, 115))