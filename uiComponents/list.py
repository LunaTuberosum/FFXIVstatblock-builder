import re
import pygame

from editor.cardComponents.abilityComponent import EffectData

from singletons import resourceHandler

from singletons.eventBus import event_bus
from singletons.keyBus import key_bus

from ui.confirmElement import ConfirmElement

from uiComponents.button import Button
from uiComponents.componet import Component
from uiComponents.listItem import ListItem
from uiComponents.textBox import TextBox


BACKGROUND_TILE_SIZE: int = 50
BACKGROUND_TILE_SIZE_X2: int = 100

class List(Component):
    def __init__(self, element, pos: tuple[int, int], size: tuple[int, int], list_name: str):
        super().__init__(
            pos,
            size
        )
        
        from editor.ui.effectElement import EffectElement
        self.element: EffectElement = element
        
        self.list_name: str = list_name
        self.list_items: list[ListItem] = []
        
        for name, data in self.element.effects.items():
            self.list_items.append(ListItem(
                size=(self.size[0] - 21, 30),
                effect_name=name,
                effect_data=data,
                command=self.change_effect,
                parent=self
            ))
        
        self.background: pygame.Surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.__draw_background()
        
        self.font_title: pygame.Font = resourceHandler.load_font('.\\assets\\fonts\\Deutschlander.otf', 30)
        
        self.text_face: pygame.Surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.__draw_text_face()
        
        self.dragged_list: ListItem = None
        
        self.offset: int = 0
        
        self.components: dict[str, Component] = {
            'Effect_Text': TextBox(
                pos=(self.size[0] - 114, 10),
                size=(40, 1)
            ),
            'Effect_Plus': Button(
                pos=(self.size[0] - 72, 9),
                size=(32, 34),
                image='.\\assets\\icons\\AddButton.png',
                image_hover='.\\assets\\icons\\AddButton_hover.png',
                command=self.add_effect_num
            )
            ,
            'Effect_Minus': Button(
                pos=(self.size[0] - 41, 9),
                size=(32, 34),
                image='.\\assets\\icons\\MinusButton.png',
                image_hover='.\\assets\\icons\\MinusButton_hover.png',
                command=self.minus_effect_num
            )
        }
        
        self.get_component('Effect_Text').change_text(str(len(self.element.effects)))
        self.get_component('Effect_Text').add_command(self.check_numeric)
        self.get_component('Effect_Text').add_char_limit(3)
        
        key_bus.register('mouse_scroll_down', self.mouse_scroll_down)
        key_bus.register('mouse_scroll_up', self.mouse_scroll_up)
        
        event_bus.register('swap_effects', self.swap_effects)
        
    def deregister(self):
        super().deregister()
        
        key_bus.deregister('mouse_scroll_down', self.mouse_scroll_down)
        key_bus.deregister('mouse_scroll_up', self.mouse_scroll_up)
        
        event_bus.deregister('swap_effects', self.swap_effects)
        
        for componet in self.components.values():
            componet.deregister()
            
        for item in self.list_items:
            item.deregister()
        
    def get_component(self, comp_name: str) -> Component:
        return self.components.get(comp_name)
    
    def set_effects(self) -> None:
        list_items = []
        
        index: int = 0
        for name, data in self.element.effects.items():
            if index >= len(self.list_items):
                list_items.append(ListItem(
                    size=(self.size[0] - 21, 30),
                    effect_name=name,
                    effect_data=data,
                    command=self.change_effect,
                    parent=self
                ))
                continue
            
            item: ListItem = self.list_items[index]
            item.effect_name = name
            item.effect_data = data
            item.refresh()
            
            list_items.append(item)
            index += 1
            
        self.list_items = list_items
        
    def swap_effects(self, effect: ListItem) -> None:
        if not self.dragged_list:
            return
        
        swap_to: ListItem = None
        all_effects: list[ListItem] = []
        for item in self.list_items:
            all_effects.append(item)
            
            if item.hovering and item != effect:
                swap_to = item
                
        mouse = pygame.mouse.get_pos()
        if not swap_to and mouse[1] < all_effects[0].rect.y:
            swap_to = all_effects[0]
            
        if not swap_to and mouse[1] > all_effects[-1].rect.y:
            swap_to = all_effects[-1]
            
        if not swap_to:
            return
        
        swapper_effect_name: str = effect.effect_name
        swapper_effect_data: str = effect.effect_data
        
        effect.effect_name = swap_to.effect_name
        effect.effect_data = swap_to.effect_data
        
        swap_to.effect_name = swapper_effect_name
        swap_to.effect_data = swapper_effect_data
        
        effect.refresh()
        swap_to.refresh()
        
        new_effects = {}
        for item in self.list_items:
            new_effects[item.effect_name] = item.effect_data
            
        self.element.effects = new_effects
        self.element.update_effect()
        
    def handle_effects(self) -> None:
        effect_text: TextBox = self.get_component('Effect_Text')
        if effect_text.active:
            return
        
        num_effects: int = int(effect_text.text)
        
        if num_effects == len(self.element.effects):
            return
        
        if num_effects > len(self.element.effects):
            count = 0
            for name in self.element.effects.keys():
                if name.startswith('Effect'):
                    count += 1
                    
            for new in range(num_effects - len(self.element.effects)):
                self.element.effects[f'Effect {count}'] = EffectData(
                    '',
                    {},
                    False
                )
                count += 1
                
            self.set_effects()
            
            if count == 1:
                self.__modify_effect(self.list_items[0])
                
        elif num_effects < len(self.element.effects):
            def lower_effects():
                new_effects: dict[str, EffectData] = {}
                
                index: int = 0
                for name, data in self.element.effects.items():
                    if index >= num_effects:
                        break
                    
                    new_effects[name] = data
                    index += 1
                    
                self.element.effects = new_effects
                effect_text.change_text(str(len(self.element.effects)))
                
                if self.element.current_effect and name == self.element.current_effect[0] and len(self.element.effects):
                    last_key: str = list(self.element.effects.keys())[-1]
                    self.element.current_effect = (last_key, self.element.effects[last_key])
                    self.element.update_effect()
                    
                self.set_effects()
                
            def confirm():                
                event_bus.sign('ui_window', None)  
                lower_effects()
                self.element.apply()
                
                if len(self.list_items) == 0:
                    self.element.clear()
                
            def cancel():
                event_bus.sign('ui_window', None)
                effect_text.change_text(str(len(self.element.effects)))
            
            last_key: str = list(self.element.effects.keys())[-1]
            
            if not last_key.startswith('Effect') or self.element.effects[last_key].desc or \
                (self.element.current_effect[0] == last_key and (not self.element.get_component('Name_Text').text.startswith('Effect') or self.element.get_component('Desc_Text').text)):
                    
                confirm_elemnet: ConfirmElement = ConfirmElement(
                    'This effect has been modified in some way.\nWould you like to delete it?',
                    confrim_command=confirm
                )
                confirm_elemnet.change_cancel_commnad(cancel)
                
                event_bus.sign('ui_window', confirm_elemnet, True)
                self.get_component('Effect_Minus').no_hover()
                
            else:
                lower_effects()
                if len(self.list_items) == 0:
                    self.element.clear()
                
        self.element.apply()
            
    def draw(self, screen: pygame.Surface, parent_pos: tuple[int, int]) -> None:
        super().draw(screen, parent_pos)
        
        self.image.blit(self.background)
        self.image.blit(self.text_face)
        
        screen.blit(self.image, self.rect.topleft)
        
        if len(self.list_items) > 10:
            segment_size: float = (self.size[1] - 52) / len(self.list_items)
            scroll_size: float = segment_size * 10
            scroll_offset: float = segment_size * self.offset
            
            pygame.draw.rect(screen, '#525552', (self.size[0] - 13 + self.rect.x, self.rect.y + 48 + scroll_offset, 8, scroll_size))
        
        for component in self.components.values():
            if component.is_hover(pygame.mouse.get_pos()):
                component.hover()
            else:
                component.no_hover()
            
            component.draw(screen, self.rect.topleft)
            
        self.handle_effects()
        
        y: int = 49
        self.dragged_list = None
        pos: tuple[int, int] = ()
        for index, item in enumerate(self.list_items):
            item.active = True
            
            if index <= self.offset - 1:
                item.active = False
                continue
            
            if index >= 10 + self.offset:
                item.active = False
                continue
            
            item.no_hover()
            if not item.active:
                return
            
            if item.is_hover(pygame.mouse.get_pos()):
                item.hover()
                
            item.current = False
            if self.element.current_effect and item.effect_name == self.element.current_effect[0]:
                item.current = True
            
            if item.drag:
                self.dragged_list = item
                pos = (5 + self.rect.x, y + self.rect.y)
            else:
                item.draw(screen, (5 + self.rect.x, y + self.rect.y))   
            y += 32
            
        if self.dragged_list:
            self.dragged_list.draw(screen, pos)
            
    def is_hover(self, mouse_pos: tuple[int, int]) -> bool:
        is_hover: bool = False
        for item in self.list_items:
            if item.is_hover(mouse_pos):
                is_hover = True
                
        for component in self.components.values():
            if component.is_hover(mouse_pos):
                is_hover = True

        return is_hover

    def mouse_scroll_down(self) -> None:
        if len(self.list_items) <= 10:
            return
        
        self.offset = min(self.offset + 1, len(self.list_items) - 10)
        
    def mouse_scroll_up(self) -> None:
        if len(self.list_items) <= 10:
            return
        
        self.offset = max(self.offset - 1, 0)
        
    def check_numeric(self, textbox: TextBox) -> None:
        if textbox.text.isnumeric():
            return
        
        textbox.change_text(re.sub('[^0-9]', '', textbox.text))
        
        if not textbox.text:
            textbox.change_text('0')
            
    def add_effect_num(self) -> None:
        self.__change_value('Effect_Text', 1)
    
    def minus_effect_num(self) -> None:
        self.__change_value('Effect_Text', -1)
            
    def __change_value(self, element_name: str, value: int) -> None:
        if not (textbox := self.get_component(element_name)).text.isnumeric():
            return
        
        new_value: int = max(int(textbox.text) + value, 0)
        textbox.change_text(str(new_value)) 
        
    def change_effect(self, list_item: ListItem) -> None:
        self.element.apply()
        self.__modify_effect(list_item)
        self.element.get_component('Preset_Dropdown').change_selection('Please Select a Preset...')
        
    def __modify_effect(self, list_item: ListItem) -> None:
        self.element.current_effect = (list_item.effect_name, list_item.effect_data)
        self.element.update_effect()
        
    def __draw_text_face(self) -> None:
        self.text_face.fill((0, 0, 0, 0))
        
        self.text_face.blit(self.font_title.render(self.list_name, True, '#000000'), (15, 11))
        self.text_face.blit(self.font_title.render(self.list_name, True, '#ffffff'), (15, 10))
        
    def __draw_background(self) -> None:
        _background: dict[str, pygame.Surface] = List.__split_background()

        self.background.blit(
            _background['TopLeft'], 
            (
                0, 
                0
            )
        )
        self.background.blit(
            _background['TopRight'], 
            (
                self.size[0] - BACKGROUND_TILE_SIZE, 
                0
            )
        )
        self.background.blit(
            _background['BottomLeft'], 
            (
                0, 
                self.size[1] - BACKGROUND_TILE_SIZE
            )
        )
        self.background.blit(
            _background['BottomRight'], 
            (
                self.size[0] - BACKGROUND_TILE_SIZE, 
                self.size[1] - BACKGROUND_TILE_SIZE
            )
        )

        self.background.blit(
            pygame.transform.scale(
                _background['TopMiddle'], 
                (
                    self.size[0] - BACKGROUND_TILE_SIZE_X2, 
                    BACKGROUND_TILE_SIZE
                )
            ), 
            (
                BACKGROUND_TILE_SIZE, 
                0
            )
            )
        self.background.blit(
            pygame.transform.scale(
                _background['Left'], 
                (
                    BACKGROUND_TILE_SIZE, 
                    self.size[1] - BACKGROUND_TILE_SIZE_X2
                )
            ), 
            (
                0, 
                BACKGROUND_TILE_SIZE
            )
        )
        self.background.blit(
            pygame.transform.scale(
                _background['Right'], 
                (
                    BACKGROUND_TILE_SIZE, 
                    self.size[1] - BACKGROUND_TILE_SIZE_X2
                )
            ), 
            (
                self.size[0] - BACKGROUND_TILE_SIZE, 
                BACKGROUND_TILE_SIZE
            )
        )
        self.background.blit(
            pygame.transform.scale(
                _background['BottomMiddle'], 
                (
                    self.size[0] - BACKGROUND_TILE_SIZE_X2, 
                    BACKGROUND_TILE_SIZE
                )
            ), 
            (
                BACKGROUND_TILE_SIZE, 
                self.size[1] - BACKGROUND_TILE_SIZE
            )
        )

        self.background.blit(
            pygame.transform.scale(
                _background['Middle'], 
                (
                    self.size[0] - BACKGROUND_TILE_SIZE_X2, 
                    self.size[1] - BACKGROUND_TILE_SIZE_X2
                )
            ), 
            (
                BACKGROUND_TILE_SIZE, 
                BACKGROUND_TILE_SIZE
            )
        )
               
    def __split_background() -> dict[str, pygame.Surface]:
        _img = resourceHandler.load_image('.\\assets\\backgrounds\\ListBackground.png')

        _temp: dict[str, pygame.Surface] = {
            'TopLeft': None,
            'TopMiddle': None,
            'TopRight': None,
            'Left': None,
            'Middle': None,
            'Right': None,
            'BottomLeft': None,
            'BottomMiddle': None,
            'BottomRight': None
        }

        _temp['TopLeft'] = pygame.surface.Surface((BACKGROUND_TILE_SIZE, BACKGROUND_TILE_SIZE), pygame.SRCALPHA)
        _temp['TopLeft'].blit(_img, (0, 0))
        _temp['TopMiddle'] = pygame.surface.Surface((BACKGROUND_TILE_SIZE, BACKGROUND_TILE_SIZE), pygame.SRCALPHA)
        _temp['TopMiddle'].blit(_img, (-BACKGROUND_TILE_SIZE, 0))
        _temp['TopRight'] = pygame.surface.Surface((BACKGROUND_TILE_SIZE, BACKGROUND_TILE_SIZE), pygame.SRCALPHA)
        _temp['TopRight'].blit(_img, (-BACKGROUND_TILE_SIZE_X2, 0))

        _temp['Left'] = pygame.surface.Surface((BACKGROUND_TILE_SIZE, BACKGROUND_TILE_SIZE), pygame.SRCALPHA)
        _temp['Left'].blit(_img, (0, -BACKGROUND_TILE_SIZE))
        _temp['Middle'] = pygame.surface.Surface((BACKGROUND_TILE_SIZE, BACKGROUND_TILE_SIZE), pygame.SRCALPHA)
        _temp['Middle'].blit(_img, (-BACKGROUND_TILE_SIZE, -BACKGROUND_TILE_SIZE))
        _temp['Right'] = pygame.surface.Surface((BACKGROUND_TILE_SIZE, BACKGROUND_TILE_SIZE), pygame.SRCALPHA)
        _temp['Right'].blit(_img, (-BACKGROUND_TILE_SIZE_X2, -BACKGROUND_TILE_SIZE))

        _temp['BottomLeft'] = pygame.surface.Surface((BACKGROUND_TILE_SIZE, BACKGROUND_TILE_SIZE), pygame.SRCALPHA)
        _temp['BottomLeft'].blit(_img, (0, -BACKGROUND_TILE_SIZE_X2))
        _temp['BottomMiddle'] = pygame.surface.Surface((BACKGROUND_TILE_SIZE, BACKGROUND_TILE_SIZE), pygame.SRCALPHA)
        _temp['BottomMiddle'].blit(_img, (-BACKGROUND_TILE_SIZE, -BACKGROUND_TILE_SIZE_X2))
        _temp['BottomRight'] = pygame.surface.Surface((BACKGROUND_TILE_SIZE, BACKGROUND_TILE_SIZE), pygame.SRCALPHA)
        _temp['BottomRight'].blit(_img, (-BACKGROUND_TILE_SIZE_X2, -BACKGROUND_TILE_SIZE_X2))

        return _temp
        