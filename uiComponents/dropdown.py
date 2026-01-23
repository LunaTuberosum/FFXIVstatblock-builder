from typing import Callable
import pygame

from singletons import resourceHandler

from singletons.keyBus import key_bus
from singletons.eventBus import event_bus

from uiComponents.componet import Component


BACKGROUND_TILE_SIZE: int = 30
BACKGROUND_TILE_SIZE_X2: int = 60

class DropdownOption():
    def __init__(self, pos: tuple[int, int], command: Callable[[None], None]) -> None:
        self.pos: tuple[int, int] = pos
        self.command: Callable[[None], None] = command
        
        self.rect: pygame.Rect = pygame.Rect(self.pos, (330, 30))

class Dropdown(Component):
    def __init__(self, pos: tuple[int, int], options: dict[str, Callable[[None], None]], default: str, size: str = 'Large'):
        super().__init__(
            pos=pos,
            size=(330 if size == 'Large' else 270, 38)
        )
        
        if size == 'Large':
            self.image_open: dict[str, pygame.Surface] = {
                'no_hover': resourceHandler.load_image('.\\assets\\icons\\dropdown_open.png'),
                'hover': resourceHandler.load_image('.\\assets\\icons\\dropdown_open_hover.png'),
            }
            self.image_closed: dict[str, pygame.Surface] = {
                'no_hover': resourceHandler.load_image('.\\assets\\icons\\dropdown_closed.png'),
                'hover': resourceHandler.load_image('.\\assets\\icons\\dropdown_closed_hover.png'),
            }
        else:
            self.image_open: dict[str,
                                  pygame.Surface] = {
                'no_hover': resourceHandler.load_image('.\\assets\\icons\\dropdown_small_open.png'),
                'hover': resourceHandler.load_image('.\\assets\\icons\\dropdown_small_open_hover.png'),
            }
            self.image_closed: dict[str, pygame.Surface] = {
                'no_hover': resourceHandler.load_image('.\\assets\\icons\\dropdown_small_closed.png'),
                'hover': resourceHandler.load_image('.\\assets\\icons\\dropdown_small_closed_hover.png'),
            }
            
        self.font: pygame.Font = resourceHandler.load_font('.\\assets\\fonts\\noto-sans.regular.ttf', 20)
        
        self.options: dict[str, DropdownOption] = {}
        y: int = 5
        for option, command in options.items():
            self.options[option] = DropdownOption(
                pos=(18, y),
                command=command
            )
            
            y += 30
        
        self.selected_option: str = default
        self.active: bool = False
        
        self.option_hover: pygame.Surface = resourceHandler.load_image('.\\assets\\backgrounds\\DropDownHoverBackground.png')
        
        back_size = (294,  (len(self.options) * 30) + 10)
        self.background: pygame.Surface = pygame.Surface(back_size, pygame.SRCALPHA)
        self.__draw_background()
        
        self.background_text_face: pygame.Surface = pygame.Surface(back_size, pygame.SRCALPHA)
        
        self.text_face: pygame.Surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.__draw_text_face()
        
        key_bus.register('mouse_left_down', self.on_click)
        key_bus.register('mouse_left_down', self.check_off_click)
        
    def deregister(self):
        super().deregister()
        
        key_bus.deregister('mouse_left_down', self.on_click)
        key_bus.deregister('mouse_left_down', self.check_off_click)
        
    def draw(self, screen: pygame.Surface, parent_pos: tuple[int, int]):
        super().draw(screen, parent_pos)
        
        if self.active:
            screen.blit(self.background, (18 + self.rect.x, 35 + self.rect.y))
            
            self.background_text_face.fill((0, 0, 0, 0))
            for name, data in self.options.items():
                data.rect.topleft = (data.pos[0] + self.rect.x + 18, data.pos[1] + self.rect.y + 35)
                
                if name == self.selected_option or data.rect.collidepoint(pygame.mouse.get_pos()):
                    self.background_text_face.blit(self.option_hover, (data.pos[0] - 10, data.pos[1]))
                
                self.background_text_face.blit(self.font.render(name, True, '#000000'), (data.pos[0], data.pos[1] + 1))
                self.background_text_face.blit(self.font.render(name, True, '#ffffff'), data.pos)
                
            screen.blit(self.background_text_face, (18 + self.rect.x, 35 + self.rect.y))
            
            if self.hovering:
                self.image.blit(self.image_open['hover'])
            else:
                self.image.blit(self.image_open['no_hover'])
                
        else:
            if self.hovering:
                self.image.blit(self.image_closed['hover'])
            else:
                self.image.blit(self.image_closed['no_hover'])
                
        self.image.blit(self.text_face)
        
        screen.blit(self.image, self.rect.topleft)
        
    def on_click(self) -> None:
        if not self.hovering:
            return
        
        event_bus.sign('play_se', 'confirm')
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.active = not self.active
            return
        
        if not self.active:
            return
        
        selection: str = self.selected_option
        for name, data in self.options.items():
            if data.rect.collidepoint(pygame.mouse.get_pos()):
                selection = name
                break
            
        self.selected_option = selection
        self.__draw_text_face()
        self.active = False
        
        data.command()
        
    def check_off_click(self) -> None:
        if self.hovering or not self.active:
            return
        
        self.active = False
        
    def is_hover(self, mouse_pos: tuple[int, int]) -> bool:
        is_hover: bool = False
        if self.active and self.background.get_rect(topleft=(18 + self.rect.x, 35 + self.rect.y)).collidepoint(mouse_pos):
            is_hover = True
        
        return is_hover or self.rect.collidepoint(mouse_pos)    
    
    def __draw_text_face(self) -> None:
        self.text_face.fill((0, 0, 0, 0))
        
        self.text_face.blit(self.font.render(self.selected_option, True, '#000000'), (31, 5))
        self.text_face.blit(self.font.render(self.selected_option, True, '#ffffff'), (30, 4))
        
    def __draw_background(self) -> None:
        _background: dict[str, pygame.Surface] = Dropdown.__split_background()

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
                self.background.size[0] - BACKGROUND_TILE_SIZE, 
                0
            )
        )
        self.background.blit(
            _background['BottomLeft'], 
            (
                0, 
                self.background.size[1] - BACKGROUND_TILE_SIZE
            )
        )
        self.background.blit(
            _background['BottomRight'], 
            (
                self.background.size[0] - BACKGROUND_TILE_SIZE, 
                self.background.size[1] - BACKGROUND_TILE_SIZE
            )
        )

        self.background.blit(
            pygame.transform.scale(
                _background['TopMiddle'], 
                (
                    self.background.size[0] - BACKGROUND_TILE_SIZE_X2, 
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
                    self.background.size[1] - BACKGROUND_TILE_SIZE_X2
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
                    self.background.size[1] - BACKGROUND_TILE_SIZE_X2
                )
            ), 
            (
                self.background.size[0] - BACKGROUND_TILE_SIZE, 
                BACKGROUND_TILE_SIZE
            )
        )
        self.background.blit(
            pygame.transform.scale(
                _background['BottomMiddle'], 
                (
                    self.background.size[0] - BACKGROUND_TILE_SIZE_X2, 
                    BACKGROUND_TILE_SIZE
                )
            ), 
            (
                BACKGROUND_TILE_SIZE, 
                self.background.size[1] - BACKGROUND_TILE_SIZE
            )
        )

        self.background.blit(
            pygame.transform.scale(
                _background['Middle'], 
                (
                    self.background.size[0] - BACKGROUND_TILE_SIZE_X2, 
                    self.background.size[1] - BACKGROUND_TILE_SIZE_X2
                )
            ), 
            (
                BACKGROUND_TILE_SIZE, 
                BACKGROUND_TILE_SIZE
            )
        )
               
    def __split_background() -> dict[str, pygame.Surface]:
        _img = resourceHandler.load_image('.\\assets\\backgrounds\\DropDownBackground.png')

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