import pygame

from editor.cardComponents.abilityComponent import AbilityComponent, EffectData

from editor.ui.statCardElement import StatCardElement

from singletons.eventBus import event_bus

from uiComponents.textBox import TextBox
from uiComponents.toggleButtons import ToggleButtons
from uiComponents.list import List


ELEMENT_SIZE: tuple[int, int] = (790, 490)
W_HALF: int = 395
H_HALF: int = 245

class EffectElement(StatCardElement[AbilityComponent]):
    def __init__(self, component, ability_window) -> None:
        screen = pygame.display.get_surface()
        
        super().__init__(
            name='Effect',
            title='Effect',
            size=ELEMENT_SIZE,
            pos=(
                (screen.size[0] / 2) - W_HALF,
                (screen.size[1] / 2) - H_HALF,
            ),
            component=component
        )
        
        self.effects = self.component.effects.copy()
        self.current_effect = None
        if self.effects:
            self.current_effect = list(self.effects.items())[0]
        
        from editor.ui.abilityElement import AbilityElement
        self.ability_window: AbilityElement = ability_window
        
        apply = self.get_component('Apply')
        apply.pos = (self.size[0] - 436, apply.pos[1])
        
        self.add_component(
            'Name_Text',
            TextBox(
                pos=(460, 115),
                size=(270, 1)
            )
        )
        
        self.add_component(
            'Desc_Text',
            TextBox(
                pos=(280, 175),
                size=(450, 6)
            )
        )
        
        self.add_component(
            'Inline_Toggle',
            ToggleButtons(
                pos=(590, 390),
                size=(200, 25),
                options={
                    'Off': self.change_inline,
                    'On': self.change_inline
                },
                default='Off'
            )
        )
        
        self.add_component(
            'Effect_List',
            List(
                element=self,
                pos=(25, 55),
                size=(220, 385),
                list_name='Effects'
            )
        )
        
        if self.current_effect:
            self.update_effect()
        
    def apply(self):
        new_effects: list[str, EffectData] = {}
        
        for name, data in self.effects.items():
            if self.current_effect and self.current_effect[0] == name:
                
                desc_text: TextBox = self.get_component('Desc_Text')
                    
                new_effects[self.get_component('Name_Text').text] = EffectData(
                    desc_text.text,
                    desc_text.formating,
                    self.get_component('Inline_Toggle').button_selected.text == 'On'
                )
                
                self.current_effect = (self.get_component('Name_Text').text, new_effects[self.get_component('Name_Text').text])
                continue
            
            new_effects[name] = data
            
        self.component.effects = new_effects
        self.component.refresh()
        self.effects = new_effects
        self.get_component('Effect_List').set_effects()
                        
        self.component.refresh()
        
    def draw(self, screen: pygame.Surface) -> None:
        super().draw(screen)
        
        if self.pos[0] != (screen.size[0] / 2) - W_HALF \
        or self.pos[1] != (screen.size[1] / 2) - H_HALF:
                    
            self.pos = (
                (screen.size[0] / 2) - W_HALF,
                (screen.size[1] / 2) - H_HALF
            )
            
        self.image.blit(self.text_face)
            
        screen.blit(self.image, self.pos)
        
        for comp in self.components.values():
            comp.draw(screen, self.pos)
            
    def update_effect(self) -> None:
        self.get_component('Name_Text').change_text(self.current_effect[0])
        self.get_component('Desc_Text').change_text(self.current_effect[1].desc, self.current_effect[1].format_data)
        self.get_component('Inline_Toggle').set_option('On' if self.current_effect[1].in_line else 'Off')
            
    def change_inline(self, selection: str) -> None:
        self.get_component('Inline_Toggle').set_option(selection)
            
    def _render_text_face(self):
        super()._render_text_face()
        
        self.render_text('Presets', '#C2C2C2', (265, 55))
        
        self.render_text('Name', '#C2C2C2', (265, 90))
        self.render_text('Effect Name', '#EEE1C5', (290, 115))
        
        self.render_text('Description', '#C2C2C2', (265, 150))
        
        self.render_text('Inline', '#C2C2C2', (265, 360))
        self.render_text('Is Inline', '#EEE1C5', (290, 385))
        