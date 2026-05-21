import pygame

from singletons import resourceHandler

from singletons.eventBus import event_bus
from singletons.keyBus import key_bus
from uiComponents.button import Button
from uiComponents.componet import Component
from uiComponents.textBox import TextBox


BACKGROUND_TILE_SIZE: int = 50
BACKGROUND_TILE_SIZE_X2: int = 100

SEPERATOR_POS: tuple[int, int] = (25, 45)
SEPERATOR_SIZE: tuple[int, int] = (50, 3)

TITLE_POS: tuple[int, int] = (25, 20)
TITLE_POS_OFFSET: tuple[int, int] = (25, 21)

RECT_OFFSET: int = 8

class UIElement():
    def __init__(self, name: str, title: str, size: tuple[int, int], pos: tuple[int, int], write_config: bool = True) -> None:
        self.id: str = name
        self.title: str = title
        self.size: list[int] = size
        self.pos: list[int] = pos
        self.write_config: bool = write_config
        
        self.background: pygame.Surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.__draw_background()
        
        self.image: pygame.Surface = pygame.Surface(self.size, pygame.SRCALPHA)
        
        self.rect = pygame.Rect(
            (
                self.pos[0] + RECT_OFFSET, 
                self.pos[1] + RECT_OFFSET
            ), 
            (
                self.size[0] - (RECT_OFFSET * 2), 
                self.size[1] - (RECT_OFFSET * 2)
            )
        )
        
        self.components: dict[str, Component] = {}
        
        self.font: pygame.Font = resourceHandler.load_font('.\\assets\\fonts\\noto-sans.regular.ttf', 18)

        self.font_title: pygame.Font = resourceHandler.load_font('.\\assets\\fonts\\Deutschlander.otf', 25)
        self.seperator: pygame.Surface = resourceHandler.load_image('.\\assets\\backgrounds\\UISeperator.png')

        self.hovering: bool = False
        
        key_bus.register('mouse_left_down', self.check_off_click)
        
        self.add_component('Close_UI',Button(
            pos=(
                self.size[0] - 43,
                19
            ),
            size=(24, 24),
            image='.\\assets\\icons\\CloseButton.png',
            image_hover='.\\assets\\icons\\CloseButton_hover.png',
            command=self.close
        ))
        
        event_bus.sign('play_se', 'open_window')
        
    def deregister(self) -> None:
        key_bus.deregister('mouse_left_down', self.check_off_click)
        
        for comp in self.components.values():
            comp.deregister()
            
    def close(self) -> None:
        event_bus.sign('play_se', 'close_window')
        
        self.deregister()
            
        event_bus.sign('ui_window', None)
        
    def check_off_click(self) -> None:
        if self.hovering:
            return
        
        self.close()
        
    def no_hover(self) -> None:
        if not self.hovering:
            return
        self.hovering = False
            
    def hover(self) -> None:
        self.hovering = True
        
    def add_component(self, component_name: str, component: Component) -> Component:
        self.components[component_name] = component
        return component

    def get_component(self, component_name: str) -> Component:
        return self.components[component_name]
        
    def render_text(self, text: str, color: str, pos: tuple[int, int]) -> None:
        self.image.blit(self.font.render(text, True, '#000000'), (pos[0], pos[1] + 1))
        self.image.blit(self.font.render(text, True, color), (pos[0], pos[1]))
        
    def draw(self, screen: pygame.Surface) -> None:
        self.image.fill((0, 0, 0, 0))
        
        self.image.blit(self.background, (0, 0))

        self.image.blit(pygame.transform.scale(self.seperator, (self.size[0] - SEPERATOR_SIZE[0], SEPERATOR_SIZE[1])), SEPERATOR_POS)

        self.image.blit(self.font_title.render(f'{self.title}{" Configuration" if self.write_config else ""}', True, '#000000'), TITLE_POS_OFFSET)
        self.image.blit(self.font_title.render(f'{self.title}{" Configuration" if self.write_config else ""}', True, '#CCCCCC' if not self.hovering else '#dedede'), TITLE_POS)
      
    def is_hover(self, mouse_pos: tuple[int, int]) ->  bool:
        return self.rect.collidepoint(mouse_pos)
        
    def tab(self, textbox: TextBox) -> None:
        current_box: TextBox = None
        next_box: TextBox = None
        for component in self.components.values():
            if not isinstance(component, TextBox):
                continue
            
            if component == textbox:
                current_box = component
                continue
            
            if current_box:
                next_box = component
                break
                
        if not next_box:
            current_box.end_field()
            return
                
        current_box.end_field()
        next_box.activate()

    def __draw_background(self) -> None:
        _background: dict[str, pygame.Surface] = UIElement.__split_background()

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
        _img = resourceHandler.load_image('.\\assets\\backgrounds\\UIBackground.png')

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