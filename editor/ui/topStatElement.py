import re
from typing import Callable
import pygame

from editor.cardComponents.topStatComponent import TopStatComponent

from editor.ui.statCardElement import StatCardElement
from uiComponents.button import Button
from uiComponents.textBox import TextBox

WIDTH: int = 730
HEIGHT: int = 410
HEIGHT_TOKEN: int = 310

class TopStatElement(StatCardElement[TopStatComponent]):
    def __init__(self, component) -> None:
        super().__init__(
            name='TopStat',
            title='Attributes',
            size=(WIDTH, HEIGHT_TOKEN if component.is_token else HEIGHT),
            pos=(
                pygame.display.get_surface().size[0] - WIDTH, 
                30
            ),
            component=component
        )
        
        self.add_component(
            'Size_Text',
            TextBox(
                [130, 80], 
                [140, 1]
            )
        ).change_text(self.component.creature_size)
        
        self.add_component(
            'Species_Text',
            TextBox(
                [490, 80], 
                [180, 1]
            )
        ).change_text(self.component.species)
        
        self.__add_textbox(
            name='Defence',
            text=self.component.defense,
            pos=(140, 120),
            box_size=70, 
            plus_callback=self.add_defence,
            minus_callback=self.minus_defence
        )
        
        self.__add_textbox(
            name='Magic_Defence',
            text=self.component.magic_defense,
            pos=(540, 120),
            box_size=70, 
            plus_callback=self.add_magic_defence,
            minus_callback=self.minus_magic_defence
        )
        
        self.__add_textbox(
            name='HP',
            text=self.component.max_HP,
            pos=(140, 160),
            box_size=70, 
            plus_callback=self.add_HP,
            minus_callback=self.minus_HP
        )
    
        self.__add_textbox(
            name='Speed',
            text=self.component.speed,
            pos=(540, 160),
            box_size=70, 
            plus_callback=self.add_speed,
            minus_callback=self.minus_speed
        )
        
        self.__add_textbox(
            name='Vigilance',
            text=self.component.vigilance,
            pos=(140, 200),
            box_size=70, 
            plus_callback=self.add_vigilance,
            minus_callback=self.minus_vigilance
        )

        
        if self.component.is_token:
            return
        
        self.__add_textbox(
            name='STR',
            text=self.component.str,
            pos=(40, 300),
            box_size=50, 
            plus_callback=self.add_STR,
            minus_callback=self.minus_STR
        ).add_command(self.check_numeric)
        
        self.__add_textbox(
            name='DEX',
            text=self.component.dex,
            pos=(170, 300),
            box_size=50, 
            plus_callback=self.add_DEX,
            minus_callback=self.minus_DEX
        ).add_command(self.check_numeric)
        
        self.__add_textbox(
            name='VIT',
            text=self.component.vit,
            pos=(300, 300),
            box_size=50, 
            plus_callback=self.add_VIT,
            minus_callback=self.minus_VIT
        ).add_command(self.check_numeric)
        
        self.__add_textbox(
            name='INT',
            text=self.component.int,
            pos=(430, 300),
            box_size=50, 
            plus_callback=self.add_INT,
            minus_callback=self.minus_INT
        ).add_command(self.check_numeric)
        
        self.__add_textbox(
            name='MND',
            text=self.component.mnd,
            pos=(560, 300),
            box_size=50, 
            plus_callback=self.add_MND,
            minus_callback=self.minus_MND
        ).add_command(self.check_numeric)
        
    def draw(self, screen: pygame.Surface) -> None:
        super().draw(screen)
        
        self.image.blit(self.text_face)
        
        screen.blit(self.image, self.pos)
        
        for comp in self.components.values():
            comp.draw(screen, self.pos)
            
    def apply(self) -> None:
        self.component.creature_size = self.get_component('Size_Text').text
        self.component.species = self.get_component('Species_Text').text
        
        self.component.defense = self.get_component('Defence_Text').text
        self.component.magic_defense = self.get_component('Magic_Defence_Text').text
        
        self.component.max_HP = self.get_component('HP_Text').text
        self.component.speed = self.get_component('Speed_Text').text
        
        self.component.vigilance = self.get_component('Vigilance_Text').text
        
        self.component.str = self.get_component('STR_Text').text
        self.component.dex = self.get_component('DEX_Text').text
        self.component.vit = self.get_component('VIT_Text').text
        self.component.int = self.get_component('INT_Text').text
        self.component.mnd = self.get_component('MND_Text').text
        
        self.component.refresh()
        
    def add_defence(self) -> None:
        self.__change_value('Defence_Text', 1)
    
    def minus_defence(self) -> None:
        self.__change_value('Defence_Text', -1)
        
    def add_magic_defence(self) -> None:
        self.__change_value('Magic_Defence_Text', 1)
    
    def minus_magic_defence(self) -> None:
        self.__change_value('Magic_Defence_Text', -1)
        
    def add_HP(self) -> None:
        self.__change_value('HP_Text', 5)
    
    def minus_HP(self) -> None:
        self.__change_value('HP_Text', -5)
        
    def add_speed(self) -> None:
        self.__change_value('Speed_Text', 1)
    
    def minus_speed(self) -> None:
        self.__change_value('Speed_Text', -1)
        
    def add_vigilance(self) -> None:
        self.__change_value('Vigilance_Text', 1)
    
    def minus_vigilance(self) -> None:
        self.__change_value('Vigilance_Text', -1)
        
    def add_STR(self) -> None:
        self.__change_value('STR_Text', 1)
    
    def minus_STR(self) -> None:
        self.__change_value('STR_Text', -1)
        
    def add_DEX(self) -> None:
        self.__change_value('DEX_Text', 1)
    
    def minus_DEX(self) -> None:
        self.__change_value('DEX_Text', -1)
        
    def add_VIT(self) -> None:
        self.__change_value('VIT_Text', 1)
    
    def minus_VIT(self) -> None:
        self.__change_value('VIT_Text', -1)
        
    def add_INT(self) -> None:
        self.__change_value('INT_Text', 1)
    
    def minus_INT(self) -> None:
        self.__change_value('INT_Text', -1)
        
    def add_MND(self) -> None:
        self.__change_value('MND_Text', 1)
    
    def minus_MND(self) -> None:
        self.__change_value('MND_Text', -1)
            
    def check_numeric(self, textbox: TextBox) -> None:
        if textbox.text.isnumeric():
            return
        
        textbox.change_text(re.sub('[^-?0-9]', '', textbox.text))
        
        if not textbox.text:
            textbox.change_text('0')
            
    def __change_value(self, element_name: str, value: int) -> None:
        if not (textbox := self.get_component(element_name)).text.isnumeric():
            return
        
        textbox.change_text(str(int(textbox.text) + value))     
    
    def __add_textbox(self, name: str, text: str,  pos: tuple[int, int], box_size: int, plus_callback: Callable[[None], None], minus_callback: Callable[[None], None]) -> TextBox:
        self.add_component(
            f'{name}_Text',
            TextBox(
                pos=pos, 
                size=(box_size, 1)
            )
        ).change_text(text)
        
        self.add_component(
            f'{name}_Plus',
            Button(
                pos=(pos[0] + box_size, pos[1]),
                size=(30, 32),
                image='.\\assets\\icons\\AddButton.png',
                image_hover='.\\assets\\icons\\AddButton_hover.png',
                command=plus_callback
            )
        )
        self.add_component(
            f'{name}_Minus',
            Button(
                pos=(pos[0] + box_size + 30, pos[1]),
                size=(30, 32),
                image='.\\assets\\icons\\MinusButton.png',
                image_hover='.\\assets\\icons\\MinusButton_hover.png',
                command=minus_callback
            )
        )
        
        return self.get_component(f'{name}_Text')
            
    def _render_text_face(self):
        super()._render_text_face()
    
        self.render_text('Secondary Attributes', '#C2C2C2', (25, 55))

        self.render_text('Size', '#EEE1C5', (50, 80))

        self.render_text('Species', '#EEE1C5', (350, 80))

        self.render_text('Defense', '#EEE1C5', (50, 120))

        self.render_text('Magic Defense', '#EEE1C5', (350, 120))

        self.render_text('Max HP', '#EEE1C5', (50, 160))

        self.render_text('Speed', '#EEE1C5', (350, 160))

        self.render_text('Vigilance', '#EEE1C5', (50, 200))

        ## Skip if token

        if not self.component.is_token:

            self.render_text('Primary Attributes', '#C2C2C2', (25, 245))

            self.render_text('STR', '#EEE1C5', (105 - (self.font.size('STR')[0] / 2), 270))

            self.render_text('DEX', '#EEE1C5', (235 - (self.font.size('DEX')[0] / 2), 270))

            self.render_text('VIT', '#EEE1C5', (365 - (self.font.size('VIT')[0] / 2), 270))

            self.render_text('INT', '#EEE1C5', (495 - (self.font.size('INT')[0] / 2), 270))

            self.render_text('MND', '#EEE1C5', (625 - (self.font.size('MND')[0] / 2), 270))