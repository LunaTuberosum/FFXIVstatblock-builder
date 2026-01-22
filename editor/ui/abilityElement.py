import pygame

from editor.cardComponents.abilityComponent import AbilityComponent

from editor.ui.effectElement import EffectElement
from editor.ui.markerElement import MarkerElement
from editor.ui.statCardElement import StatCardElement

from singletons.eventBus import event_bus

from uiComponents.button import Button
from uiComponents.textBox import TextBox
from uiComponents.toggleButtons import ToggleButtons


ELEMENT_SIZE: tuple[int, int] = (580, 590)

INVK_ON: bool = True
INVK_OFF: bool = False

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
        )
        
        self.get_component('Name_Text').change_text(self.component.name)
        self.get_component('Name_Text').add_tabbing(self.tab)
        
        self.add_component(
            'INVK_Toggle',
            ToggleButtons(
                pos=(380, 145),
                size=(200, 25),
                options={
                    'Off': self.change_invk,
                    'On': self.change_invk
                },
                default='On' if self.component.invk == INVK_ON else 'Off'
            )
        )
        
        self.add_component(
            'Types_Text',
            TextBox(
                pos=(220, 200),
                size=(300, 2)
            )
        )
        
        self.get_component('Types_Text').change_text(self.component.types)
        self.get_component('Types_Text').add_tabbing(self.tab)
        self.get_component('Types_Text').set_can_format(False)
        
        self.add_component(
            'Effect_Edit',
            Button(
                pos=(322, 290),
                size=(198, 38),
                image='.\\assets\\icons\\button.png',
                image_hover='.\\assets\\icons\\button_hover.png',
                command=self.effect_edit,
                text='Effect Builder'
            )
        )
        
        self.add_component(
            'Marker_Edit',
            Button(
                pos=(322, 350),
                size=(198, 38),
                image='.\\assets\\icons\\button.png',
                image_hover='.\\assets\\icons\\button_hover.png',
                command=self.marker_edit,
                text='Marker Builder'
            )
        )
        
        self.add_component(
            'Extra_Text',
            TextBox(
                pos=(40, 420),
                size=(480, 3)
            )
        )
        
        self.get_component('Extra_Text').change_text(self.component.extra_text)
        self.get_component('Extra_Text').add_tabbing(self.tab)
        self.get_component('Extra_Text').set_can_format(False)
        
    def draw(self, screen: pygame.Surface) -> None:
        super().draw(screen)
            
        self.image.blit(self.text_face)
        
        screen.blit(self.image, self.pos)
        
        for comp in self.components.values():
            comp.draw(screen, self.pos)
            
    def apply(self) -> None:
        self.component.name = self.get_component('Name_Text').text
        
        invk_toggle: ToggleButtons = self.get_component('INVK_Toggle')
        if invk_toggle.button_selected.text == 'On':
            self.component.invk = INVK_ON
        elif invk_toggle.button_selected.text == 'Off':
            self.component.invk = INVK_OFF
            
        self.component.types = self.get_component('Types_Text').text
        
        self.component.extra_text = self.get_component('Extra_Text').text
            
        self.component.refresh()
           
    def change_invk(self, selection: str) -> None:
        self.get_component('INVK_Toggle').set_option(selection)
         
    def effect_edit(self) -> None:
        event_bus.sign('ui_window', EffectElement(self.component), True)
        
    def marker_edit(self) -> None:
        if not self.component.marker:
            from editor.cardComponents.markerComponnet import MarkerComponent
            self.component.marker = MarkerComponent(5, 5, self.component)
            self.component.refresh()
        
        event_bus.sign('ui_window', MarkerElement(self.component), True)
         
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