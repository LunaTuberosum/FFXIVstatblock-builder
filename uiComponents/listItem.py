from typing import Callable
import pygame

from editor.cardComponents.abilityComponent import EffectData

from singletons import resourceHandler
from singletons.keyBus import key_bus

from src.timer import Timer


BACKGROUND_TILE_SIZE: int = 10
BACKGROUND_TILE_SIZE_X2: int = 20

class ListItem():
    def __init__(self, size: tuple[int, int], effect_name: str, effect_data: EffectData, command: Callable[['ListItem'], None]) -> None:
        self.size: tuple[int, int] = size
        self.effect_name: str = effect_name
        self.effect_data: EffectData = effect_data
        
        self.command: Callable[['ListItem'], None] = command
        
        self.background: pygame.Surface =pygame.Surface(self.size, pygame.SRCALPHA)
        self.__draw_background()
        
        self.image: pygame.Surface =pygame.Surface(self.size, pygame.SRCALPHA)
        self.rect: pygame.Rect = self.image.get_rect()
        
        self.font_bolded: pygame.Font = resourceHandler.load_font('.\\assets\\fonts\\noto-sans.regular.ttf', 15)
        self.font_bolded.bold = True
        
        self.cursor_timer: Timer = Timer(300)
        self.cursor_timer.start()
        self.cursor_pos: tuple = (self.size[0] - 30, 0)
        self.cursor_cycle: int = -1
        self.cursor: pygame.Surface = resourceHandler.load_image('.\\assets\\icons\\Cursor.png')
        
        self.text_face: pygame.Surface =pygame.Surface(self.size, pygame.SRCALPHA)
        self.__render_text_face()
        
        self.hovering: bool = False
        
        self.current: bool = False
        self.click_timer: Timer = Timer(300)
        
        self.active: bool = True
        
        key_bus.register('mouse_left_down', self.on_click)
        
    def deregister(self) -> None:
        key_bus.deregister('mouse_left_down', self.on_click)
        
    def draw(self, screen: pygame.Surface, pos: tuple[int, int]) -> None:
        self.image.fill((0, 0, 0, 0))
        self.rect.topleft = pos
        self.image.blit(self.background)
        self.image.blit(self.text_face)
        
        if self.cursor_timer.is_done():
            self.cursor_pos = (self.cursor_pos[0] + (5 * self.cursor_cycle), 0)
            self.cursor_cycle *= -1
            self.cursor_timer.start()
        
        if self.current:
            self.image.blit(self.cursor, self.cursor_pos)
        elif self.hovering:
            self.image.blit(self.cursor, (self.size[0] - 30, 0))
        
        screen.blit(self.image, self.rect.topleft)
        
    def on_click(self) -> None:
        if not self.hovering:
            return
        
        if self.click_timer.time_left() > 0:
            self.command(self)
        
        self.click_timer.start()
        
    def no_hover(self) -> None:
        if not self.hovering:
            return
        
        self.hovering = False
        
    def hover(self) -> None:
        self.hovering = True
        
    def is_hover(self, mouse_pos: tuple[int, int]) -> bool:
        return self.rect.collidepoint(mouse_pos)
    
    def __render_text_face(self) -> None:
        self.text_face.fill((0, 0, 0, 0))
        
        name: str = ''
        
        width: int = 0
        for char in self.effect_name:
            name += char
            
            if self.font_bolded.size(name)[0] >= self.size[0] - 12:
                name = name[:-4]
                name += '...'
                break
        
        self.text_face.blit(self.font_bolded.render(name, True, '#995745'), (6, 3))
    
    def __draw_background(self) -> None:
        _background: dict[str, pygame.Surface] = ListItem.__split_background()

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
        _img = resourceHandler.load_image('.\\assets\\backgrounds\\ListItemBackground.png')

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