from enum import Enum
import re
import sys
from typing import Callable

import pygame

import pyperclip

from src.timer import Timer

from singletons import resourceHandler

from singletons.keyBus import key_bus
from singletons.eventBus import event_bus

from uiComponents.componet import Component


class Formating(Enum):
    BOLD: int = 0
    BOLD_OFF: int = 1
    
    ITALIC: int = 2
    ITALIC_OFF: int = 3
    
    ABILITY: int = 4
    ABILITY_OFF: int = 5
    
    ATTRIBUTE: int = 6
    ATTRIBUTE_OFF: int = 7
    
    NEW_LINE: int = 8
    
BACKGROUND_TILE_SIZE: int = 10
BACKGROUND_TILE_SIZE_X2: int = 20
    
TEXT_WIDTH: int = 14
LINE_CHAR: int = 32

CURSOR_END: int = -1
CURSOR_OFFSET: tuple[int, int] = (5, 2)
CURSOR_MOUSE_POS_DEFUALT: tuple[int, int] = (1000, 1000)

class TextBox(Component):
    def __init__(self, pos: tuple[int, int], size: tuple[int, int]) -> None:
        super().__init__(
            pos,
            (size[0], size[1] * 30)
        )
        self.box_size: tuple[int, int] = size
            
        self.background: pygame.Surface = self.__draw_background('.\\assets\\backgrounds\\UITextBoxBackground.png')
        self.background_selected: pygame.Surface = self.__draw_background('.\\assets\\backgrounds\\UITextBoxBackground_selected.png') 
        
        self.font: pygame.Font = resourceHandler.load_font('.\\assets\\fonts\\noto-sans.regular.ttf', 18)
        
        self.text: str = ''
        
        # TODO: MAKE THIS ITS OWN OBJECT
        self.cursor: pygame.Surface = self.font.render('|', True, '#ffffff')
        self.cursor_pos: tuple[int] = (0, 0)
        self.cursor_mouse_pos: tuple[int] = CURSOR_MOUSE_POS_DEFUALT
        self.cursor_index: int = CURSOR_END
        self.cursor_active: bool = False
        self.cursor_timer: Timer = Timer(400)
        
        self.cursor_selection: bool = False
        self.cursor_selection_start: tuple[int, int] = ()
        self.cursor_selection_end: tuple[int, int] = ()
        self.cursor_selection_indexs: tuple[int, int] = (sys.maxsize, 0)
        self.highlighted_text: str = ''
        
        self.text_face: pygame.Surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.__draw_text()
        
        self.active: bool = False
        
        self.command: Callable[[TextBox], None] = None
        
        key_bus.register('mouse_left_down', self.on_click)
        key_bus.register('mouse_left_down', self.check_off_click)
        
        key_bus.register('mouse_left_up', self.on_release)
        
        key_bus.register('paste', self.paste)
        key_bus.register('copy', self.copy)
        
        key_bus.register('left_arrow_down', self.left_shift)
        key_bus.register('up_arrow_down', self.up_shift)
        key_bus.register('down_arrow_down', self.down_shift)
        key_bus.register('right_arrow_down', self.right_shift)
        
    def deregister(self) -> None:
        super().deregister()
        
        key_bus.deregister('mouse_left_down', self.on_click)
        key_bus.deregister('mouse_left_down', self.check_off_click)
        
        key_bus.deregister('mouse_left_up', self.on_release)
        
        key_bus.deregister('paste', self.paste)
        key_bus.deregister('copy', self.copy)
        
        key_bus.deregister('left_arrow_down', self.left_shift)
        key_bus.deregister('up_arrow_down', self.up_shift)
        key_bus.deregister('down_arrow_down', self.down_shift)
        key_bus.deregister('right_arrow_down', self.right_shift)
        
    def add_command(self, command: Callable[['TextBox'], None]) -> None:
        self.command = command
        
    def change_text(self, new_text: str) -> None:
        self.text = new_text
        
        self.__draw_text()
        
    def render_text(self, text: str, color: str, pos: tuple[int, int], highlight: bool = False) -> None:
        if highlight:
            self.highlighted_text += text
            self.text_face.blit(self.font.render(text, True, '#000000', '#2355ba'), (pos[0], pos[1] + 1))
            self.text_face.blit(self.font.render(text, True, color), (pos[0], pos[1]))
            
        self.text_face.blit(self.font.render(text, True, '#000000'), (pos[0], pos[1] + 1))
        self.text_face.blit(self.font.render(text, True, color), (pos[0], pos[1]))
        
    def left_shift(self) -> None:
        if not self.active:
            return
            
        self.cursor_active = True
        self.__reset_selection()

        
        if self.cursor_index == CURSOR_END:
            self.cursor_index = max(len(self.text) - 1, 0)
            self.__draw_text()
            return
        
        self.cursor_index = max(self.cursor_index - 1, 0)
        self.__draw_text()
        
    def up_shift(self) -> None:
        if not self.active:
            return
            
        self.cursor_active = True
        self.__reset_selection()

        
        if self.box_size[1] == 1:
            self.cursor_index = 0
            self.__draw_text()
            return
        
    def down_shift(self) -> None:
        if not self.active:
            return
            
        self.cursor_active = True
        self.__reset_selection()

        
        if self.box_size[1] == 1:
            self.cursor_index = CURSOR_END
            self.__draw_text()
            return
    
    def right_shift(self) -> None:
        if not self.active:
            return
            
        if self.cursor_index == CURSOR_END:
            return
        self.cursor_active = True
        self.__reset_selection()

        
        self.cursor_index += 1
        
        if self.cursor_index == len(self.text):
            self.cursor_index = CURSOR_END
            
        self.__draw_text()
        
    def draw(self, screen: pygame.Surface, parent_pos: tuple[int, int]) -> None:
        super().draw(screen, parent_pos)
        
        if self.hovering or self.active:
            self.image.blit(self.background_selected, (0, 0))
        else:
            self.image.blit(self.background, (0, 0))        
            
        self.image.blit(self.text_face, (0, 0))
        
        if self.cursor_selection:
            mouse = pygame.mouse.get_pos()
            self.cursor_selection_end = (mouse[0] - self.rect.x, mouse[1] - self.rect.y)
            self.cursor_mouse_pos = (mouse[0] - self.rect.x, mouse[1] - self.rect.y)
            
            self.__draw_text()
        
        if self.cursor_timer.is_done():
            self.cursor_active = not self.cursor_active
            self.cursor_timer.start()
        
        if self.cursor_active:
            self.image.blit(self.cursor, self.cursor_pos)
            
        screen.blit(self.image, self.rect.topleft)
        
    def __add_char(self, char: str) -> None:
        if not self.text:
            self.change_text(char)
            return
        
        if self.cursor_index == CURSOR_END:
            self.change_text(self.text + char)
            return
        
        chars: list[str] = list(self.text)
        
        chars.insert(self.cursor_index, char)
        self.cursor_index += 1
        
        self.change_text(''.join(chars))
        
    def copy(self) -> None:
        pyperclip.copy(self.highlighted_text)
        
    def __reset_selection(self) -> None:
        self.cursor_selection = False
        self.cursor_selection_start = ()
        self.cursor_selection_end = ()
        self.cursor_selection_indexs = (sys.maxsize, 0)
        
    def __remove_highlighted_text(self) -> None:
        text: str = ''
        
        for index, char in enumerate(list(self.text)):
            if self.cursor_selection_indexs[0] <= index and index <= self.cursor_selection_indexs[1]:
                continue
            
            text += char
            
        self.__reset_selection()
        
        self.change_text(text)
            
        self.highlighted_text = ''
    
    def paste(self) -> None:
        if not self.active:
            return
        
        clip: str = pyperclip.paste()
        
        if self.highlighted_text:
            self.__remove_highlighted_text()
        
        for char in clip:
            self.__add_char(char)
        
    def __remove_char(self) -> None:
        if not self.text:
            return
        
        if self.cursor_index == 0:
            return
        
        chars: list[str] = list(self.text)
        
        if self.cursor_index == CURSOR_END:
            chars.pop(self.cursor_index)
        else:
            self.cursor_index = self.cursor_index - 1
            chars.pop(self.cursor_index)
            
        self.change_text(''.join(chars))
        
    def typing(self, unicode: str) -> None:
        if not self.active:
            event_bus.sign('typing_register', None)
            return 
        
        # print(repr(unicode))

        # User used BACKSPACE
        if unicode == '\b':
            if self.highlighted_text:
                self.__remove_highlighted_text()
                return
            
            self.__remove_char()
            return
        
        # User used ESCAPE
        if unicode == '\x1b':
            self.hovering = False
            self.check_off_click()
            return
            
        # User used RETURN/ENTER
        if unicode == '\r':
            self.hovering = False
            self.check_off_click()
            return
            
        # User used TAB
        if unicode == '\t':
            return
            
        if not re.match(r'[A-Za-z0-9()-_[\]<> "\'{}]', unicode) or re.match(r'[:;]', unicode):
            return
        
        self.__add_char(unicode)
        
    def check_off_click(self) -> None:
        if self.hovering or not self.active:
            return
        
        self.cursor_active = False
        self.cursor_timer.reset()
        
        self.__reset_selection()
        
        self.active = False
        
        if self.command:
            self.command(self)
        
    def on_click(self) -> None:
        if not self.hovering:
            return
        
        self.cursor_mouse_pos = CURSOR_MOUSE_POS_DEFUALT
        self.cursor_index = CURSOR_END
        
        if self.active:
            mouse = pygame.mouse.get_pos()
            self.cursor_mouse_pos = (mouse[0] - self.rect.x, mouse[1] - self.rect.y)
            
            self.__reset_selection()
            self.cursor_selection = True
            self.cursor_selection_start = (mouse[0] - self.rect.x, mouse[1] - self.rect.y)
            
        self.cursor_active = True
        self.cursor_timer.start()
        
        self.__draw_text()
        
        self.active = True
        event_bus.sign('typing_register', self)
        
    def on_release(self) -> None:
        self.cursor_selection = False
        
    def __set_cursor_pos(self, pos: tuple[int, int]) -> None:
        self.cursor_pos = (pos[0] - CURSOR_OFFSET[0], pos[1] - CURSOR_OFFSET[1])
        
    def __draw_text(self) -> None:
        if self.box_size[1] > 1:
            pass
            return
        
        self.text_face.fill((0, 0, 0, 0))
        
        text_size: tuple[int, int] = self.font.size(self.text)
        surf_size: tuple[int, int] = self.text_face.size
        pos: tuple[int, int] = (
            (surf_size[0] / 2) - (text_size[0] / 2),
            (surf_size[1] / 2) - (text_size[1] / 2)
        )
        
        # [(minX, maxX, minY, maxY, advance**), ...]
        text_metrics: list[tuple[int, ...]] = self.font.metrics(self.text)
        
        sel_low: tuple[int, int] = []
        sel_high: tuple[int, int] = []
        if self.cursor_selection_end:
            self.highlighted_text = ''
            if self.cursor_selection_start[0] < self.cursor_selection_end[0]:
                sel_low = self.cursor_selection_start
                sel_high = self.cursor_selection_end
            else:
                sel_low = self.cursor_selection_end
                sel_high = self.cursor_selection_start
        
        modded_cursor: bool = False
        for index, char in enumerate(self.text):
            if sel_low and sel_low[0] < pos[0] + (text_metrics[index][4] / 2) and pos[0] + (text_metrics[index][4] / 2) < sel_high[0]:
                self.cursor_selection_indexs = (
                    min(index, self.cursor_selection_indexs[0]),
                    max(index, self.cursor_selection_indexs[1])
                )
                self.render_text(char, '#ffffff', pos, highlight=True)
            else:
                self.render_text(char, '#ffffff', pos)

            if self.cursor_index == index:
                self.__set_cursor_pos(pos)
                modded_cursor = True
            
            pos = (pos[0] + text_metrics[index][4], pos[1])
            
            if self.cursor_mouse_pos[0] < pos[0] - (text_metrics[index][4] / 2):
                self.__set_cursor_pos((pos[0] - text_metrics[index][4], pos[1]))
                self.cursor_mouse_pos = CURSOR_MOUSE_POS_DEFUALT
                self.cursor_index = index
                
                modded_cursor = True
        
        if self.cursor_mouse_pos[0] > pos[0] and not modded_cursor:
            self.cursor_index = CURSOR_END
        
        if self.cursor_index == CURSOR_END:
            self.__set_cursor_pos(pos)
        
    def __draw_background(self, path: str) -> pygame.Surface:
        _background: dict[str, pygame.Surface] = TextBox.__split_background(path)
        
        temp: pygame.Surface = pygame.Surface(self.size, pygame.SRCALPHA)
        size: tuple[int, int] = temp.size

        temp.blit(
            _background['TopLeft'], 
            (
                0, 
                0
            )
        )
        temp.blit(
            _background['TopRight'], 
            (
                size[0] - BACKGROUND_TILE_SIZE, 
                0
            )
        )
        temp.blit(
            _background['BottomLeft'], 
            (
                0, 
                size[1] - BACKGROUND_TILE_SIZE
            )
        )
        temp.blit(
            _background['BottomRight'], 
            (
                size[0] - BACKGROUND_TILE_SIZE, 
                size[1] - BACKGROUND_TILE_SIZE
            )
        )

        temp.blit(
            pygame.transform.scale(
                _background['TopMiddle'], 
                (
                    size[0] - BACKGROUND_TILE_SIZE_X2, 
                    BACKGROUND_TILE_SIZE
                )
            ), 
            (
                BACKGROUND_TILE_SIZE, 
                0
            )
            )
        temp.blit(
            pygame.transform.scale(
                _background['Left'], 
                (
                    BACKGROUND_TILE_SIZE, 
                    size[1] - BACKGROUND_TILE_SIZE_X2
                )
            ), 
            (
                0, 
                BACKGROUND_TILE_SIZE
            )
        )
        temp.blit(
            pygame.transform.scale(
                _background['Right'], 
                (
                    BACKGROUND_TILE_SIZE, 
                    size[1] - BACKGROUND_TILE_SIZE_X2
                )
            ), 
            (
                size[0] - BACKGROUND_TILE_SIZE, 
                BACKGROUND_TILE_SIZE
            )
        )
        temp.blit(
            pygame.transform.scale(
                _background['BottomMiddle'], 
                (
                    size[0] - BACKGROUND_TILE_SIZE_X2, 
                    BACKGROUND_TILE_SIZE
                )
            ), 
            (
                BACKGROUND_TILE_SIZE, 
                size[1] - BACKGROUND_TILE_SIZE
            )
        )

        temp.blit(
            pygame.transform.scale(
                _background['Middle'], 
                (
                    size[0] - BACKGROUND_TILE_SIZE_X2, 
                    size[1] - BACKGROUND_TILE_SIZE_X2
                )
            ), 
            (
                BACKGROUND_TILE_SIZE, 
                BACKGROUND_TILE_SIZE
            )
        )
        
        return temp
        
    def __split_background(path: str) -> dict[str, pygame.Surface]:
        _img = resourceHandler.load_image(path)

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