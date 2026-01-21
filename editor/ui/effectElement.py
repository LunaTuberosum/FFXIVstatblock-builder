from typing import Callable
import pygame

from editor.cardComponents.abilityComponent import AbilityComponent, EffectData

from editor.ui.statCardElement import StatCardElement

from singletons.eventBus import event_bus

from ui.confirmElement import ConfirmElement
from uiComponents.dropdown import Dropdown
from uiComponents.textBox import TextBox
from uiComponents.textFormat import Format, FormatData
from uiComponents.toggleButtons import ToggleButtons
from uiComponents.list import List


ELEMENT_SIZE: tuple[int, int] = (790, 490)
W_HALF: int = 395
H_HALF: int = 245

class EffectElement(StatCardElement[AbilityComponent]):
    def __init__(self, component) -> None:
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
                size=(220, 375),
                list_name='Effects'
            )
        )
        
        self.add_component(
            'Preset_Dropdown',
            Dropdown(
                pos=(403, 52),
                options={
                    'Target (Single)':  self.target_single,
                    'Target (Area)':  self.target_area,
                    'Origin':  self.origin,
                    'Range  (Single)':  self.range_single,
                    'Range  (Single Ranged)':  self.range_single_ranged,
                    'Range  (Area)':  self.range_area,
                    'Range  (Area Ranged)':  self.range_area_ranged,
                    'Check':  self.check,
                    'CR':  self.cr,
                    'Base Effect':  self.base_effect,
                    'Direct Hit':  self.direct_hit,
                    'Marker Area':  self.marker_area,
                    'Marker Trigger':  self.marker_trigger,
                    'Marker Effect':  self.marker_effect,
                    'Limitation':  self.limitation
                },
                default='Please Select a Preset...'
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
         
    def __is_modified(self, modify_text: Callable[[None], None]) -> bool:
        name_text: TextBox = self.get_component('Name_Text')
        desc_text: TextBox = self.get_component('Desc_Text')
         
        def confirm():
            event_bus.sign('ui_window', None)
            modify_text()
            
        if not name_text.text.startswith('Effect') or desc_text.text != '':
            event_bus.sign('ui_window', ConfirmElement(
                text='This effect has been modified.\nAre you sure you want to override it?',
                confrim_command=confirm
            ), True)
            return True
        
        return False
         
    def target_single(self) -> None:
        def modify_text():
            self.get_component('Name_Text').change_text('Target')
            self.get_component('Desc_Text').change_text('Single', {})
            self.get_component('Inline_Toggle').button_selected = self.get_component('Inline_Toggle').options['Off']
        
        if self.__is_modified(modify_text):
            return
        
        modify_text()
        
    def target_area(self) -> None:
        def modify_text():
            self.get_component('Name_Text').change_text('Target')
            self.get_component('Desc_Text').change_text('All enemies within range', {})
            self.get_component('Inline_Toggle').button_selected = self.get_component('Inline_Toggle').options['Off']
        
        if self.__is_modified(modify_text):
            return
        
        modify_text()
        
    def origin(self) -> None:
        def modify_text():
            self.get_component('Name_Text').change_text('Origin')
            self.get_component('Desc_Text').change_text('1 square occupied by this character', {})
            self.get_component('Inline_Toggle').button_selected = self.get_component('Inline_Toggle').options['Off']
        
        if self.__is_modified(modify_text):
            return
        
        modify_text()
        
    def range_single(self) -> None:
        def modify_text():
            self.get_component('Name_Text').change_text('Range')
            self.get_component('Desc_Text').change_text('1 squares', {})
            self.get_component('Inline_Toggle').button_selected = self.get_component('Inline_Toggle').options['Off']
        
        if self.__is_modified(modify_text):
            return
        
        modify_text()
    
    def range_single_ranged(self) -> None:
        def modify_text():
            self.get_component('Name_Text').change_text('Range')
            self.get_component('Desc_Text').change_text('X squares', {})
            self.get_component('Inline_Toggle').button_selected = self.get_component('Inline_Toggle').options['Off']
        
        if self.__is_modified(modify_text):
            return
        
        modify_text()
        
    def range_area(self) -> None:
        def modify_text():
            self.get_component('Name_Text').change_text('Range')
            self.get_component('Desc_Text').change_text('A #x# area centered on this character', {})
            self.get_component('Inline_Toggle').button_selected = self.get_component('Inline_Toggle').options['Off']
        
        if self.__is_modified(modify_text):
            return
        
        modify_text()
        
    def range_area_ranged(self) -> None:
        def modify_text():
            self.get_component('Name_Text').change_text('Range')
            self.get_component('Desc_Text').change_text('A #x# area within X squares of this character', {})
            self.get_component('Inline_Toggle').button_selected = self.get_component('Inline_Toggle').options['Off']
        
        if self.__is_modified(modify_text):
            return
        
        modify_text()
        
    def check(self) -> None:
        def modify_text():
            self.get_component('Name_Text').change_text('Check')
            self.get_component('Desc_Text').change_text('MOD (d20 + X)', {0: FormatData(Format.COLOR, '#2D638E'), 3: FormatData(Format.COLOR_OFF, '')})
            self.get_component('Inline_Toggle').button_selected = self.get_component('Inline_Toggle').options['Off']
        
        if self.__is_modified(modify_text):
            return
        
        modify_text()
        
    def cr(self) -> None:
        def modify_text():
            self.get_component('Name_Text').change_text('CR')
            self.get_component('Desc_Text').change_text('Target\'s Magic Defense/Defense ', {9: FormatData(Format.COLOR, '#2D638E'), 30: FormatData(Format.COLOR_OFF, '')})
            self.get_component('Inline_Toggle').button_selected = self.get_component('Inline_Toggle').options['On']
        
        if self.__is_modified(modify_text):
            return
        
        modify_text()
        
    def base_effect(self) -> None:
        def modify_text():
            self.get_component('Name_Text').change_text('Base Effect')
            self.get_component('Desc_Text').change_text('Deals X/XdY damage to [the target]/[all targets].', {})
            self.get_component('Inline_Toggle').button_selected = self.get_component('Inline_Toggle').options['Off']
        
        if self.__is_modified(modify_text):
            return
        
        modify_text()
        
    def direct_hit(self) -> None:
        def modify_text():
            self.get_component('Name_Text').change_text('Direct Hit')
            self.get_component('Desc_Text').change_text('Deals an an additonal X/XdY damage.', {})
            self.get_component('Inline_Toggle').button_selected = self.get_component('Inline_Toggle').options['Off']
        
        if self.__is_modified(modify_text):
            return
        
        modify_text()
        
    def marker_area(self) -> None:
        def modify_text():
            self.get_component('Name_Text').change_text('Marker Area')
            self.get_component('Desc_Text').change_text('A #x# area centered on the origin', {})
            self.get_component('Inline_Toggle').button_selected = self.get_component('Inline_Toggle').options['Off']
        
        if self.__is_modified(modify_text):
            return
        
        modify_text()
        
    def marker_trigger(self) -> None:
        def modify_text():
            self.get_component('Name_Text').change_text('Marker Trigger')
            self.get_component('Desc_Text').change_text('At the start of this character\'s next turn.', {})
            self.get_component('Inline_Toggle').button_selected = self.get_component('Inline_Toggle').options['Off']
        
        if self.__is_modified(modify_text):
            return
        
        modify_text()
        
    def marker_effect(self) -> None:
        def modify_text():
            self.get_component('Name_Text').change_text('Marker Effect')
            self.get_component('Desc_Text').change_text('Deals X/XdY damage to all targets', {})
            self.get_component('Inline_Toggle').button_selected = self.get_component('Inline_Toggle').options['Off']
        
        if self.__is_modified(modify_text):
            return
        
        modify_text()
        
    def limitation(self) -> None:
        def modify_text():
            self.get_component('Name_Text').change_text('Limitation')
            self.get_component('Desc_Text').change_text('Once/Twice per phase.', {})
            self.get_component('Inline_Toggle').button_selected = self.get_component('Inline_Toggle').options['Off']
        
        if self.__is_modified(modify_text):
            return
        
        modify_text()
            
    def _render_text_face(self):
        super()._render_text_face()
        
        self.render_text('Presets', '#C2C2C2', (265, 55))
        
        self.render_text('Name', '#C2C2C2', (265, 90))
        self.render_text('Effect Name', '#EEE1C5', (290, 115))
        
        self.render_text('Description', '#C2C2C2', (265, 150))
        
        self.render_text('Inline', '#C2C2C2', (265, 360))
        self.render_text('Is Inline', '#EEE1C5', (290, 385))
        