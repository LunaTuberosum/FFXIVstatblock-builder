import re
import pygame

from editor.statcard import StatCard
from singletons.eventBus import event_bus

from uiComponents.button import Button
from uiComponents.textBox import TextBox

from ui.uiElement import UIElement
from uiComponents.toggleButtons import ToggleButtons


ELEMENT_SIZE: tuple[int, int] = (500, 395)
W_HALF: int = 250
H_HALF: int = 197

class AddCardElement(UIElement):
    def __init__(self) -> None:
        screen = pygame.display.get_surface()
        
        super().__init__(
            name='New Card',
            title='New Card',
            size=ELEMENT_SIZE,
            pos=(
                (screen.size[0] / 2) - W_HALF,
                (screen.size[1] / 2) - H_HALF,
            )
        )
        
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
                default='Standard'
            )
        )
        
        self.add_component(
            'Card_Width_Text',
            TextBox(
                pos=(288, 140),
                size=(90, 1),
            )
        )
        
        self.get_component('Card_Width_Text').change_text('1')
        self.get_component('Card_Width_Text').add_tabbing(self.tab)
        self.get_component('Card_Width_Text').add_command(self.check_numeric)
        
        self.add_component(
            'Card_Width_Plus',
            Button(
                pos=(378, 138),
                size=(32, 34),
                image='.\\assets\\icons\\AddButton.png',
                image_hover='.\\assets\\icons\\AddButton_hover.png',
                command=self.add_width
            )
        )
        self.add_component(
            'Card_Width_Minus',
            Button(
                pos=(408, 138),
                size=(32, 34),
                image='.\\assets\\icons\\MinusButton.png',
                image_hover='.\\assets\\icons\\MinusButton_hover.png',
                command=self.minus_width
            )
        )
        
        self.add_component(
            'Card_Height_Text',
            TextBox(
                pos=(288, 175),
                size=(90, 1),
            )
        )
        
        self.get_component('Card_Height_Text').change_text('1')
        self.get_component('Card_Height_Text').add_tabbing(self.tab)
        self.get_component('Card_Height_Text').add_command(self.check_numeric)
        
        self.add_component(
            'Card_Height_Plus',
            Button(
                pos=(378, 173),
                size=(32, 34),
                image='.\\assets\\icons\\AddButton.png',
                image_hover='.\\assets\\icons\\AddButton_hover.png',
                command=self.add_height
            )
        )
        self.add_component(
            'Card_Height_Minus',
            Button(
                pos=(408, 173),
                size=(32, 34),
                image='.\\assets\\icons\\MinusButton.png',
                image_hover='.\\assets\\icons\\MinusButton_hover.png',
                command=self.minus_height
            )
        )
        
        self.add_component(
            'Card_Trait_Text',
            TextBox(
                pos=(288, 235),
                size=(90, 1),
            )
        )
        
        self.get_component('Card_Trait_Text').change_text('0')
        self.get_component('Card_Trait_Text').add_tabbing(self.tab)
        self.get_component('Card_Trait_Text').add_command(self.check_numeric)
        
        self.add_component(
            'Card_Trait_Plus',
            Button(
                pos=(378, 233),
                size=(32, 34),
                image='.\\assets\\icons\\AddButton.png',
                image_hover='.\\assets\\icons\\AddButton_hover.png',
                command=self.add_trait
            )
        )
        self.add_component(
            'Card_Trait_Minus',
            Button(
                pos=(408, 233),
                size=(32, 34),
                image='.\\assets\\icons\\MinusButton.png',
                image_hover='.\\assets\\icons\\MinusButton_hover.png',
                command=self.minus_trait
            )
        )
        
        self.add_component(
            'Card_Ability_Text',
            TextBox(
                pos=(288, 285),
                size=(90, 1),
            )
        )
        
        self.get_component('Card_Ability_Text').change_text('0')
        self.get_component('Card_Ability_Text').add_tabbing(self.tab)
        self.get_component('Card_Ability_Text').add_command(self.check_numeric)
        
        self.add_component(
            'Card_Ability_Plus',
            Button(
                pos=(378, 283),
                size=(32, 34),
                image='.\\assets\\icons\\AddButton.png',
                image_hover='.\\assets\\icons\\AddButton_hover.png',
                command=self.add_ability
            )
        )
        self.add_component(
            'Card_Ability_Minus',
            Button(
                pos=(408, 283),
                size=(32, 34),
                image='.\\assets\\icons\\MinusButton.png',
                image_hover='.\\assets\\icons\\MinusButton_hover.png',
                command=self.minus_ability
            )
        )
        
        self.add_component(
            'Create',
            Button(
                pos=(28, 330),
                size=(198, 38),
                image='.\\assets\\icons\\button.png',
                image_hover='.\\assets\\icons\\button_hover.png',
                command=self.create,
                text='Create'
            )
        )
        
        self.add_component(
            'Close',
            Button(
                pos=(272, 330),
                size=(198, 38),
                image='.\\assets\\icons\\button.png',
                image_hover='.\\assets\\icons\\button_hover.png',
                command=self.close,
                text='Close'
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
        
    def create(self) -> None:
        card: StatCard = StatCard(
            int(self.get_component('Card_Width_Text').text),
            int(self.get_component('Card_Height_Text').text)
        )
        
        from editor.cardComponents.nameComponent import NameComponent
        card.add_component(
            'Name_Component',
            NameComponent(card)
        )
        
        from editor.cardComponents.topStatComponent import TopStatComponent
        card.add_component(
            'Top_Stat_Component',
            TopStatComponent(
                card,
                is_token=True if self.get_component('Type_Toggle').button_selected.text == 'Token' else False
            )
        )
        
        from editor.cardComponents.sectionNameComponent import SectionNameComponent
        
        trait_text: TextBox = self.get_component('Card_Trait_Text')
        if trait_text.text != '0':
            card.add_component(
                'Traits_Title',
                SectionNameComponent(card, 'Traits')
            )
            
            from editor.cardComponents.traitComponent import TraitComponent
            
            for trait in range(int(trait_text.text)):
                card.add_component(
                    f'Trait_{trait}',
                    TraitComponent(card)
                )
                
        ability_text: TextBox = self.get_component('Card_Ability_Text')
        if ability_text.text != '0':
            card.add_component(
                'Abilities_Title',
                SectionNameComponent(card, 'Abilities')
            )
            
            from editor.cardComponents.abilityComponent import AbilityComponent
            
            for ability in range(int(ability_text.text)):
                card.add_component(
                    f'Ability_{ability}',
                    AbilityComponent(card)
                )
    
        event_bus.sign('add_card', card)
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

        self.render_text('Card Size', '#C2C2C2', (25, 115))

        self.render_text('Width', '#EEE1C5', (50, 140))

        self.render_text('Height', '#EEE1C5', (50, 175))

        self.render_text('Traits', '#C2C2C2', (25, 210))

        self.render_text('Number of Traits', '#EEE1C5', (50, 235))

        self.render_text('Abilities', '#C2C2C2', (25, 260))

        self.render_text('Number of Abilities', '#EEE1C5', (50, 285))