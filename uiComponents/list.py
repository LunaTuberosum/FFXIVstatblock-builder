import pygame

from singletons import resourceHandler
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
                command=self.change_effect
            ))
        
        self.background: pygame.Surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.__draw_background()
        
        self.font_title: pygame.Font = resourceHandler.load_font('.\\assets\\fonts\\Deutschlander.otf', 30)
        
        self.text_face: pygame.Surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.__draw_text_face()
        
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
                command=None
            )
            ,
            'Effect_Minus': Button(
                pos=(self.size[0] - 42, 9),
                size=(32, 34),
                image='.\\assets\\icons\\MinusButton.png',
                image_hover='.\\assets\\icons\\MinusButton_hover.png',
                command=None
            )
        }
        
        self.get_component('Effect_Text').change_text(str(len(self.element.effects)))
        
    def deregister(self):
        super().deregister()
        
        for componet in self.components.values():
            componet.deregister()
            
        for item in self.list_items:
            item.deregister()
        
    def get_component(self, comp_name: str) -> Component:
        return self.components.get(comp_name)
    
    def set_effects(self) -> None:
        for item in self.list_items:
            item.deregister()
            
        self.list_items = []
        
        for name, data in self.element.effects.items():
            self.list_items.append(ListItem(
                size=(self.size[0] - 21, 30),
                effect_name=name,
                effect_data=data,
                command=self.change_effect
            ))
        
    def draw(self, screen: pygame.Surface, parent_pos: tuple[int, int]) -> None:
        super().draw(screen, parent_pos)
        
        self.image.blit(self.background)
        self.image.blit(self.text_face)
        
        screen.blit(self.image, self.rect.topleft)
        
        for component in self.components.values():
            component.no_hover()
            if component.is_hover(pygame.mouse.get_pos()):
                component.hover()
            
            component.draw(screen, self.rect.topleft)
            
        y: int = 49
        for item in self.list_items:
            item.no_hover()
            if not item.active:
                return
            
            if item.is_hover(pygame.mouse.get_pos()):
                item.hover()
                
            item.current = False
            if item.effect_name == self.element.current_effect[0]:
                item.current = True
            
            item.draw(screen, (5 + self.rect.x, y + self.rect.y))
            y += 32
        
    def change_effect(self, list_item: ListItem) -> None:
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
        