from typing import Callable

import pygame

from singletons import resourceHandler
from singletons.eventBus import event_bus
from singletons.keyBus import key_bus

from src.contextMenuOption import ContextMenuOption


OPTION_HEIGHT: int = 24
OPTION_X: int = 22
OPTION_Y_START: int = 11
OPTION_Y_INCREASE: int = 25

BACKGROUND_TILE_SIZE: int = 14
BACKGROUND_TILE_SIZE_X2: int = 28

RECT_OFFSET: int = 3

class ContextMenu():
    def __init__(self, mouse_pos: tuple[int, int], width: int, options: dict[str, Callable[[None], None]]) -> None:
        self.options: list[ContextMenuOption] = []
        y: int = OPTION_Y_START
        for _option, _call in options.items():
            self.options.append(ContextMenuOption(mouse_pos, (OPTION_X, y), _option, _call))
            y += OPTION_Y_INCREASE
        
        self.mouse_pos: tuple[int, int] = mouse_pos
        self.size: tuple[int, int] = (width, OPTION_HEIGHT + (OPTION_HEIGHT * len(self.options)))
        
        self.background: pygame.Surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.__draw_background()
        
        self.image: pygame.Surface = pygame.Surface(self.size, pygame.SRCALPHA)
        
        self.rect: pygame.Rect = pygame.Rect(
            (
                self.mouse_pos[0] + RECT_OFFSET, 
                self.mouse_pos[1] + RECT_OFFSET
            ), 
            (
                self.size[0] - (RECT_OFFSET * 2), 
                self.size[1] - (RECT_OFFSET * 2)
            )
        )
        
        self.hovering: bool = False
        
        key_bus.register('mouse_left_down', self.check_off_click)
        
    def add_options(self, options: dict[str, Callable[[None], None]]) -> None:
        prev_len: int = len(self.options)
        
        y: int = self.options[-1].pos[1] + OPTION_Y_INCREASE
        for _option, _call in options.items():
            exists: bool = False
            for _c_option in self.options:
                if _c_option.text == _option: 
                    exists = True
                    continue
                
            if exists:
                continue
            
            self.options.append(ContextMenuOption(self.mouse_pos, (OPTION_X, y), _option, _call))
            y += OPTION_Y_INCREASE
            
        if prev_len == len(self.options):
            return
            
        self.size = (self.size[0], OPTION_HEIGHT + (OPTION_HEIGHT * len(self.options)))
        
        self.background = pygame.Surface(self.size, pygame.SRCALPHA)
        self.__draw_background()
        
        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        
        self.rect = pygame.Rect(
            (
                self.mouse_pos[0] + RECT_OFFSET, 
                self.mouse_pos[1] + RECT_OFFSET
            ), 
            (
                self.size[0] - (RECT_OFFSET * 2), 
                self.size[1] - (RECT_OFFSET * 2)
            )
        )
        
    def draw(self, screen: pygame.Surface) -> None:
        self.image.fill((0, 0, 0, 0))
        self.image.blit(self.background, (0, 0))
        
        for _option in self.options:
            _option.draw(self.image)
        
        screen.blit(self.image, self.mouse_pos)
                
    def deregister(self) -> None:
        key_bus.deregister('mouse_left_down', self.check_off_click)
        
        for option in self.options:
            option.deregister()
                
    def check_off_click(self) -> None:
        if self.hovering:
            return
        
        event_bus.sign('context_menu', {})
        
    def no_hover(self) -> None:
        if not self.hovering:
            return
        self.hovering = False

    def hover(self) -> None:
        self.hovering = True
        
    def __draw_background(self) -> None:
        _background: dict[str, pygame.Surface] = ContextMenu.__split_background()
        
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
        _img = resourceHandler.load_image('.\\assets\\backgrounds\\ContextMenuBackground.png')

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