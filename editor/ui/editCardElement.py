import re
import pygame

from editor.cardComponents.abilityComponent import AbilityComponent
from editor.cardComponents.cardComponent import CardComponent
from editor.cardComponents.nameComponent import LEVEL_NUM, LEVEL_TIER
from editor.cardComponents.sectionNameComponent import SectionNameComponent
from editor.cardComponents.traitComponent import TraitComponent
from singletons.eventBus import event_bus

from uiComponents.button import Button
from uiComponents.textBox import TextBox

from ui.uiElement import UIElement
from uiComponents.toggleButtons import ToggleButtons


ELEMENT_SIZE: tuple[int, int] = (500, 450)
W_HALF: int = 250
H_HALF: int = 225

class EditCardElement(UIElement):
    def __init__(self, card: object) -> None:
        screen = pygame.display.get_surface()
        
        super().__init__(
            name='Edit Card',
            title='Edit Card',
            size=ELEMENT_SIZE,
            pos=(
                (screen.size[0] / 2) - W_HALF,
                (screen.size[1] / 2) - H_HALF,
            )
        )
        
        from editor.statcard import StatCard
        self.card: StatCard = card
        
        self.text_face: pygame.Surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self._render_text_face()
        
        self.add_component(
            'Type_Toggle',
            ToggleButtons(
                pos=(220, 85),
                size=(230, 25),
                options={
                    'Standard': self.change_type,
                    'Token': self.change_type
                },
                default='Standard' if card.get_component('Top_Stat_Component').is_token == False else 'Token'
            )
        )
        
        self.add_component(
            'Level_Toggle',
            ToggleButtons(
                pos=(245, 145),
                size=(200, 25),
                options={
                    'Tier': self.change_level,
                    'Number': self.change_level
                },
                default='Tier' if card.get_component('Name_Component').level_type == LEVEL_TIER else 'Number'
            )
        )
        
        self.add_component(
            'Card_Width_Text',
            TextBox(
                pos=(288, 195),
                size=(90, 1),
            )
        )
        
        self.get_component('Card_Width_Text').change_text(str(self.card.width // 3))
        self.get_component('Card_Width_Text').add_tabbing(self.tab)
        self.get_component('Card_Width_Text').add_command(self.check_numeric)
        
        self.add_component(
            'Card_Width_Plus',
            Button(
                pos=(378, 193),
                size=(32, 34),
                image='.\\assets\\icons\\AddButton.png',
                image_hover='.\\assets\\icons\\AddButton_hover.png',
                command=self.add_width
            )
        )
        self.add_component(
            'Card_Width_Minus',
            Button(
                pos=(408, 193),
                size=(32, 34),
                image='.\\assets\\icons\\MinusButton.png',
                image_hover='.\\assets\\icons\\MinusButton_hover.png',
                command=self.minus_width
            )
        )
        
        self.add_component(
            'Card_Height_Text',
            TextBox(
                pos=(288, 230),
                size=(90, 1),
            )
        )
        
        self.get_component('Card_Height_Text').change_text(str(self.card.height))
        self.get_component('Card_Height_Text').add_tabbing(self.tab)
        self.get_component('Card_Height_Text').add_command(self.check_numeric)
        
        self.add_component(
            'Card_Height_Plus',
            Button(
                pos=(378, 228),
                size=(32, 34),
                image='.\\assets\\icons\\AddButton.png',
                image_hover='.\\assets\\icons\\AddButton_hover.png',
                command=self.add_height
            )
        )
        self.add_component(
            'Card_Height_Minus',
            Button(
                pos=(408, 228),
                size=(32, 34),
                image='.\\assets\\icons\\MinusButton.png',
                image_hover='.\\assets\\icons\\MinusButton_hover.png',
                command=self.minus_height
            )
        )
        
        self.add_component(
            'Card_Trait_Text',
            TextBox(
                pos=(288, 290),
                size=(90, 1),
            )
        )
        
        trait_count: int = 0
        for componet in self.card.components.keys():
            if not componet.startswith('Trait') or componet.startswith('Traits'):
                continue
            
            trait_count += 1
        
        self.get_component('Card_Trait_Text').change_text(str(trait_count))
        self.get_component('Card_Trait_Text').add_tabbing(self.tab)
        self.get_component('Card_Trait_Text').add_command(self.check_numeric)
        
        self.add_component(
            'Card_Trait_Plus',
            Button(
                pos=(378, 288),
                size=(32, 34),
                image='.\\assets\\icons\\AddButton.png',
                image_hover='.\\assets\\icons\\AddButton_hover.png',
                command=self.add_trait
            )
        )
        self.add_component(
            'Card_Trait_Minus',
            Button(
                pos=(408, 288),
                size=(32, 34),
                image='.\\assets\\icons\\MinusButton.png',
                image_hover='.\\assets\\icons\\MinusButton_hover.png',
                command=self.minus_trait
            )
        )
        
        self.add_component(
            'Card_Ability_Text',
            TextBox(
                pos=(288, 340),
                size=(90, 1),
            )
        )
        
        ability_count: int = 0
        for componet in self.card.components.keys():
            if not componet.startswith('Ability'):
                continue
            
            ability_count += 1
        
        self.get_component('Card_Ability_Text').change_text(str(ability_count))
        self.get_component('Card_Ability_Text').add_tabbing(self.tab)
        self.get_component('Card_Ability_Text').add_command(self.check_numeric)
        
        self.add_component(
            'Card_Ability_Plus',
            Button(
                pos=(378, 338),
                size=(32, 34),
                image='.\\assets\\icons\\AddButton.png',
                image_hover='.\\assets\\icons\\AddButton_hover.png',
                command=self.add_ability
            )
        )
        self.add_component(
            'Card_Ability_Minus',
            Button(
                pos=(408, 338),
                size=(32, 34),
                image='.\\assets\\icons\\MinusButton.png',
                image_hover='.\\assets\\icons\\MinusButton_hover.png',
                command=self.minus_ability
            )
        )
        
        self.add_component(
            'Confrim',
            Button(
                pos=(28, 385),
                size=(198, 38),
                image='.\\assets\\icons\\button.png',
                image_hover='.\\assets\\icons\\button_hover.png',
                command=self.edit,
                text='Confrim'
            )
        )
        
        self.add_component(
            'Cancel',
            Button(
                pos=(272, 385),
                size=(198, 38),
                image='.\\assets\\icons\\button.png',
                image_hover='.\\assets\\icons\\button_hover.png',
                command=self.close,
                text='Cancel'
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
            
        self.image.blit(self.text_face)
            
        screen.blit(self.image, self.pos)
        
        for comp in self.components.values():
            comp.draw(screen, self.pos)
            
    def change_type(self, selection: str) -> None:
        self.get_component('Type_Toggle').set_option(selection)
    
    def change_level(self, selection: str) -> None:
        self.get_component('Level_Toggle').set_option(selection)
            
    def check_numeric(self, textbox: TextBox) -> None:
        if textbox.text.isnumeric():
            return
        
        textbox.change_text(re.sub('[^-?0-9]', '', textbox.text))
        
        if not textbox.text:
            textbox.change_text('0')
            
    def add_width(self) -> None:
        self.__change_value('Card_Width_Text', 1)
    
    def minus_width(self) -> None:
        self.__change_value('Card_Width_Text', -1)
        
    def add_height(self) -> None:
        self.__change_value('Card_Height_Text', 1)
    
    def minus_height(self) -> None:
        self.__change_value('Card_Height_Text', -1)
        
    def add_trait(self) -> None:
        self.__change_value('Card_Trait_Text', 1)
    
    def minus_trait(self) -> None:
        self.__change_value('Card_Trait_Text', -1, min=0)
        
    def add_ability(self) -> None:
        self.__change_value('Card_Ability_Text', 1)
    
    def minus_ability(self) -> None:
        self.__change_value('Card_Ability_Text', -1, min=0)
        
    def __change_value(self, element_name: str, value: int, min: int = 1) -> None:
        if not (textbox := self.get_component(element_name)).text.isnumeric():
            return
        
        new_value: int = max(int(textbox.text) + value, min)
        textbox.change_text(str(new_value)) 
        
    def edit(self) -> None:
        is_tier: bool = self.get_component('Level_Toggle').button_selected.text == 'Tier'
        if is_tier and self.card.get_component('Name_Component').level_type != LEVEL_TIER:
            self.card.get_component('Name_Component').level = 'Mob'
        elif not is_tier and self.card.get_component('Name_Component').level_type == LEVEL_TIER:
            self.card.get_component('Name_Component').level = '00'
            
        self.card.get_component('Name_Component').level_type = LEVEL_TIER if is_tier else LEVEL_NUM
        self.card.get_component('Name_Component').refresh()
        
        self.card.get_component('Top_Stat_Component').is_token = True if self.get_component('Type_Toggle').button_selected.text == 'Token' else False
        self.card.get_component('Top_Stat_Component').refresh()
        
        traits: list[SectionNameComponent | TraitComponent] = []
        trait_num: int = int(self.get_component('Card_Trait_Text').text)
        
        count: int = 0
        for component in self.card.components.values():
            if isinstance(component, SectionNameComponent):
                component.deregister()
                continue
            
            if not isinstance(component, TraitComponent):
                continue
            
            if count >= trait_num:
                component.deregister()
                continue
            
            traits.append(component)
            count += 1
            
        if trait_num > 0:
            traits.insert(0, SectionNameComponent(self.card, 'Traits'))
            
        if count < trait_num:
            for i in range(trait_num - count):
                t = TraitComponent(self.card)
                t.name = f'Trait {trait_num + i + 1}'
                t.refresh()
                traits.append(t)
                
        abilities: list[SectionNameComponent | AbilityComponent] = []
        ability_num: int = int(self.get_component('Card_Ability_Text').text)
        
        count = 0
        for component in self.card.components.values():
            if isinstance(component, SectionNameComponent):
                component.deregister()
                continue
            
            if not isinstance(component, AbilityComponent):
                continue
            
            if count >= ability_num:
                component.deregister()
                continue
            
            abilities.append(component)
            count += 1
            
        if ability_num > 0:
            abilities.insert(0, SectionNameComponent(self.card, 'Abilities'))
            
        if count < ability_num:
            for i in range(ability_num - count):
                a = AbilityComponent(self.card)
                a.name = f'Ability {ability_num + i + 1}'
                a.refresh()
                abilities.append(a)
                
        new_components: dict[str, CardComponent] = {
            'Name_Component': self.card.get_component('Name_Component'),
            'Top_Stat_Component': self.card.get_component('Top_Stat_Component')
        }
        
        for index, trait in enumerate(traits):
            if isinstance(trait, SectionNameComponent):
                new_components['Traits_Title'] = trait
                continue
            
            new_components[f'Trait_{index}'] = trait
            
        for index, ability in enumerate(abilities):
            if isinstance(ability, SectionNameComponent):
                new_components['Abilities_Title'] = ability
                continue
            
            new_components[f'Ability_{index}'] = ability
            
        self.card.components = new_components
        
        self.card.width = int(self.get_component('Card_Width_Text').text) * 3
        self.card.height = int(self.get_component('Card_Height_Text').text)
        self.card.refresh()

        event_bus.sign('ui_window', None)
    
    def close(self) -> None:
        event_bus.sign('ui_window', None)
        
    def render_text(self, text: str, color: str, pos: tuple[int, int]) -> None:
        self.text_face.blit(self.font.render(text, True, '#000000'), (pos[0], pos[1] + 1))
        self.text_face.blit(self.font.render(text, True, color), (pos[0], pos[1]))
            
    def _render_text_face(self) -> None:
        self.text_face.fill((0,0,0,0))
        
        self.render_text('Card Type', '#C2C2C2', (25, 55))

        self.render_text('Type', '#EEE1C5', (50, 80))
        
        self.render_text('Level Type', '#C2C2C2', (25, 115))

        self.render_text('Type', '#EEE1C5', (50, 140))

        self.render_text('Card Size', '#C2C2C2', (25, 175))

        self.render_text('Width', '#EEE1C5', (50, 200))

        self.render_text('Height', '#EEE1C5', (50, 225))

        self.render_text('Traits', '#C2C2C2', (25, 260))

        self.render_text('Number of Traits', '#EEE1C5', (50, 285))

        self.render_text('Abilities', '#C2C2C2', (25, 320))

        self.render_text('Number of Abilities', '#EEE1C5', (50, 345))