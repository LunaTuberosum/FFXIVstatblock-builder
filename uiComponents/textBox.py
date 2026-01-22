import math
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
from uiComponents.textFormat import Format, FormatData
from uiComponents.textFormatBox import TextFormatBox


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
        
        self.font_bolded: pygame.Font = resourceHandler.load_font('.\\assets\\fonts\\noto-sans.regular.ttf', 18)
        self.font_bolded.bold = True
        
        self.font_italic: pygame.Font = resourceHandler.load_font('.\\assets\\fonts\\noto-sans.regular.ttf', 18)
        self.font_italic.italic = True
        
        self.text: str = ''
        self.lines: list[str] = []
        
        self.can_format: bool = True
        
        self.formating: dict[int, FormatData] = {}
        self.format_box: TextFormatBox = None
        
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
        
        self.prefix: str = ''
        self.offset: int = 0
        
        self.text_face: pygame.Surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.__draw_text()
        
        self.active: bool = False
        
        self.bold: bool = False
        self.italic: bool = False
        self.color: bool = False
        self.color_data: str = ''
        
        self.command: Callable[[TextBox], None] = None
        self.char_limit: int = -1
        
        self.tabbing_command: Callable[[TextBox], None] = None
                
        key_bus.register('mouse_left_down', self.on_click)
        key_bus.register('mouse_left_down', self.check_off_click)
        
        key_bus.register('mouse_right_down', self.on_right_click)
        
        key_bus.register('mouse_left_up', self.on_release)
        
        key_bus.register('mouse_scroll_down', self.mouse_scroll_down)
        key_bus.register('mouse_scroll_up', self.mouse_scroll_up)
        
        key_bus.register('paste', self.paste)
        key_bus.register('copy', self.copy)
        
        key_bus.register('toggle_bold', self.toggle_bold)
        key_bus.register('toggle_italic', self.toggle_italic)
        
        key_bus.register('left_arrow_down', self.left_shift)
        key_bus.register('up_arrow_down', self.up_shift)
        key_bus.register('down_arrow_down', self.down_shift)
        key_bus.register('right_arrow_down', self.right_shift)
        
    def deregister(self) -> None:
        super().deregister()
        
        self.check_off_click()
        
        key_bus.deregister('mouse_left_down', self.on_click)
        key_bus.deregister('mouse_left_down', self.check_off_click)
        
        key_bus.deregister('mouse_right_down', self.on_right_click)
        
        key_bus.deregister('mouse_left_up', self.on_release)
        
        key_bus.deregister('mouse_scroll_down', self.mouse_scroll_down)
        key_bus.deregister('mouse_scroll_up', self.mouse_scroll_up)
        
        key_bus.deregister('paste', self.paste)
        key_bus.deregister('copy', self.copy)
        
        key_bus.deregister('toggle_bold', self.toggle_bold)
        key_bus.deregister('toggle_italic', self.toggle_italic)
        
        key_bus.deregister('left_arrow_down', self.left_shift)
        key_bus.deregister('up_arrow_down', self.up_shift)
        key_bus.deregister('down_arrow_down', self.down_shift)
        key_bus.deregister('right_arrow_down', self.right_shift)
        
    def set_can_format(self, can_format: bool) -> None:
        self.can_format = can_format
        
    def add_command(self, command: Callable[['TextBox'], None]) -> None:
        self.command = command
        
    def add_tabbing(self, command: Callable[['TextBox'], None]) -> None:
        self.tabbing_command = command
        
    def add_prefix(self, prefix: str) -> None:
        self.prefix = prefix    
        self.__draw_text()
    
    def add_char_limit(self, limit: int) -> None:
        self.char_limit = limit 
    
    def change_text(self, new_text: str, format_data: dict[int, FormatData] = None) -> None:
        self.text = new_text
        
        if format_data != None:
            self.formating = format_data
        
        self.__draw_text()
        
    def render_text(self, text: str, color: str, pos: tuple[int, int], is_highlight: bool = False, is_bolded: bool = False, is_italic: bool = False) -> pygame.Surface:
        if is_highlight:
            self.highlighted_text += text
            background_color: str = '#2355ba'
        else:              
            background_color: str = None
            
        if is_bolded:
            self.text_face.blit(self.font_bolded.render(text, True, '#000000', background_color), (pos[0], pos[1] + 1))
            render: pygame.Surface = self.font_bolded.render(text, True, color)
        elif is_italic:
            self.text_face.blit(self.font_italic.render(text, True, '#000000', background_color), (pos[0], pos[1] + 1))
            render: pygame.Surface = self.font_italic.render(text, True, color)
        else:
            self.text_face.blit(self.font.render(text, True, '#000000', background_color), (pos[0], pos[1] + 1))
            render: pygame.Surface = self.font.render(text, True, color)
        self.text_face.blit(render, (pos[0], pos[1]))
        
        return render
        
    def on_right_click(self) -> None:
        if not self.active or not self.hovering or self.box_size[1] == 1:
            return
        
        if not self.can_format:
            return
        
        self.format_box = TextFormatBox((self.cursor_pos[0] + self.rect.x, self.cursor_pos[1] + self.rect.y), self)
        
    def left_shift(self) -> None:
        if not self.active:
            return
            
        if self.highlighted_text:
            self.cursor_index = self.cursor_selection_indexs[0] + 1
            
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
        
        if self.cursor_index == CURSOR_END:
            self.cursor_index = len(self.text) - 1
            
        index: int = 0
        prev_line: int = -1
        relative: int = -1
        for l_index, line in enumerate(self.lines):
            for c_index, char in enumerate(list(line)):
                if index == self.cursor_index:
                    relative = c_index
                    prev_line = l_index - 1
                    
                index += 1
        
        if prev_line == -1:
            self.cursor_index = 0
            self.__draw_text()
            return
        
        index = 0
        for l_index, line in enumerate(self.lines):
            if l_index == prev_line:
                self.cursor_index = index + relative
                break
            
            index += len(line)
            
        self.__draw_text()
        
    def down_shift(self) -> None:
        if not self.active:
            return
            
        self.cursor_active = True
        self.__reset_selection()

        
        if self.box_size[1] == 1:
            self.cursor_index = CURSOR_END
            self.__draw_text()
            return
            
        index: int = 0
        next_line: int = -1
        relative: int = -1
        for l_index, line in enumerate(self.lines):
            for c_index, char in enumerate(list(line)):
                if index == self.cursor_index:
                    relative = c_index
                    next_line = l_index + 1
                    
                index += 1
        
        if next_line >= len(self.lines):
            self.cursor_index = CURSOR_END
            self.__draw_text()
            return
        
        index = 0
        for l_index, line in enumerate(self.lines):
            if l_index == next_line:
                self.cursor_index = index + relative
                break
            
            index += len(line)
            
        self.__draw_text()
    
    def right_shift(self) -> None:
        if not self.active:
            return
            
        if self.cursor_index == CURSOR_END:
            return
        
        if self.highlighted_text:
            self.cursor_index = self.cursor_selection_indexs[1]
        
        self.cursor_active = True
        self.__reset_selection()
        
        self.cursor_index += 1
        
        if self.cursor_index == len(self.text):
            self.cursor_index = CURSOR_END
            
        self.__draw_text()
        
    def is_index_foramt(self, index: int) -> FormatData:
        char_index: int = 0
        
        bold: bool = False
        italic: bool = False
        color: bool = False
        color_data: str = ''
        
        for char in list(self.text):
            if (f_data := self.formating.get(char_index)):
                if f_data.format_type == Format.BOLD:
                    bold = True
                elif f_data.format_type == Format.BOLD_OFF:
                    bold = False
                    
                if f_data.format_type == Format.ITALIC:
                    italic = True
                elif f_data.format_type == Format.ITALIC_OFF:
                    italic = False
                    
                if f_data.format_type == Format.COLOR:
                    color = True
                    color_data = f_data.data
                elif f_data.format_type == Format.COLOR_OFF:
                    color = False
                    color_data = ''
                    
            if char_index == index:
                break
            
            char_index += 1
            
        if bold:
            return FormatData(Format.BOLD, '')
        elif italic:
            return FormatData(Format.ITALIC, '')
        elif color:
            return FormatData(Format.COLOR, color_data)
        else:
            return FormatData(Format.NONE, '')
        
    def __toggle_format_highlight(self, on_toggle: Format, off_toggle: Format, data: str = '') -> None:
        if self.is_index_foramt(self.cursor_selection_indexs[0]).format_type == on_toggle:
            self.formating[self.cursor_selection_indexs[0]] = FormatData(off_toggle, '')
            
            if (f_data := self.formating.get(self.cursor_selection_indexs[1] + 1)) and f_data.format_type == off_toggle:
                self.formating.pop(self.cursor_selection_indexs[1] + 1)
            else:
                self.formating[self.cursor_selection_indexs[1] + 1] = FormatData(on_toggle, data)
        
        else:
            self.formating[self.cursor_selection_indexs[0]] = FormatData(on_toggle, data)
            self.formating[self.cursor_selection_indexs[1] + 1] = FormatData(off_toggle, '')
            
        for index in range(self.cursor_selection_indexs[0] + 1, self.cursor_selection_indexs[1]):
            if f_data := self.formating.get(index):
                if f_data.format_type == on_toggle or f_data.format_type == off_toggle:
                    self.formating.pop(index)
            
        self.cursor_index = self.cursor_selection_indexs[1] + 1
        self.__reset_selection()
        self.__draw_text()
        
    def toggle_bold(self) -> None:
        if not self.active:
            return
        
        if not self.can_format:
            return
        
        if self.highlighted_text:
            self.__toggle_format_highlight(Format.BOLD, Format.BOLD_OFF)
            return
        
        index: int = len(self.text) if self.cursor_index == CURSOR_END else self.cursor_index
        
        if (f_data := self.formating.get(index)) and f_data.format_type == Format.BOLD:
            self.formating.pop(index)
            self.__draw_text()
            return
        
        if (f_data := self.formating.get(index)) and f_data.format_type == Format.BOLD_OFF:
            self.formating.pop(index)
            self.__draw_text()
            return
                
        if self.bold:
            self.formating[index] = FormatData(Format.BOLD_OFF, '')
            self.__draw_text()
            return

        self.formating[index] = FormatData(Format.BOLD, '')
        self.__draw_text()
        
    def toggle_italic(self) -> None:
        if not self.active:
            return
        
        if not self.can_format:
            return
        
        if self.highlighted_text:
            self.__toggle_format_highlight(Format.ITALIC, Format.ITALIC_OFF)
            return
        
        index: int = len(self.text) if self.cursor_index == CURSOR_END else self.cursor_index
        
        if (f_data := self.formating.get(index)) and f_data.format_type == Format.ITALIC:
            self.formating.pop(index)
            self.__draw_text()
            return
        
        if (f_data := self.formating.get(index)) and f_data.format_type == Format.ITALIC_OFF:
            self.formating.pop(index)
            self.__draw_text()
            return
                
        if self.italic:
            self.formating[index] = FormatData(Format.ITALIC_OFF, '')
            self.__draw_text()
            return

        self.formating[index] = FormatData(Format.ITALIC, '')
        self.__draw_text()
        
    def toggle_color(self, color: str) -> None:
        if not self.active:
            return
        
        if not self.can_format:
            return
        
        if self.highlighted_text:
            self.__toggle_format_highlight(Format.COLOR, Format.COLOR_OFF, color)
            return
        
        index: int = len(self.text) if self.cursor_index == CURSOR_END else self.cursor_index
        
        if (f_data := self.formating.get(index)) and f_data.format_type == Format.COLOR:
            self.formating.pop(index)
            self.__draw_text()
            return
                
        if self.color:
            if self.color_data != color:
                self.formating[index] = FormatData(Format.COLOR, color)
            else:
                self.formating[index] = FormatData(Format.COLOR_OFF, '')
                
            self.__draw_text()
            return

        self.formating[index] = FormatData(Format.COLOR, color)
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
        
        if self.format_box:
            self.format_box.no_hover()
            
            if self.format_box.is_hover(pygame.mouse.get_pos()):
                self.format_box.hover()
                
            self.format_box.draw(screen)
        
    def is_hover(self, mouse_pos: tuple[int, int]) -> bool:
        is_hover: bool = False
        
        if self.format_box and self.format_box.is_hover(mouse_pos):
            is_hover = True
        
        return is_hover or super().is_hover(mouse_pos)
        
    def __add_char(self, char: str) -> None:
        if not self.text:
            self.change_text(char)
            return
        
        if self.highlighted_text:
            self.__remove_highlighted_text()
        
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
        self.highlighted_text = ''
        self.cursor_selection = False
        self.cursor_selection_start = ()
        self.cursor_selection_end = ()
        self.cursor_selection_indexs = (sys.maxsize, 0)
        
    def __remove_highlighted_text(self) -> None:
        text: str = ''
        
        for index, char in enumerate(list(self.text)):
            if self.cursor_selection_indexs[0] <= index and index <= self.cursor_selection_indexs[1]:
                self.formating.pop(index, None)
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
            self.formating.pop(len(self.text), None)
            
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
            event_bus.sign('typing_register', None)
            self.hovering = False
            self.check_off_click()
            return
            
        # User used RETURN/ENTER
        if unicode == '\r':
            event_bus.sign('typing_register', None)
            self.hovering = False
            self.check_off_click()
            return
            
        # User used TAB
        if unicode == '\t':
            if not self.tabbing_command:
                return
            
            self.tabbing_command(self)
            
        if not re.match(r'[A-Za-z0-9()-_[\]<> "\'{}#]', unicode) or re.match(r'[:;]', unicode):
            return
        
        if self.char_limit != -1 and len(self.text) >= self.char_limit:
            return
        
        self.__add_char(unicode)
        
    def end_field(self) -> None:
        self.cursor_active = False
        self.cursor_timer.reset()
        
        self.cursor_mouse_pos = CURSOR_MOUSE_POS_DEFUALT
        self.cursor_index = CURSOR_END
        
        self.__reset_selection()
        
        self.active = False
        self.__draw_text()
        
        if self.command:
            self.command(self)
        
    def check_off_click(self) -> None:
        if self.hovering or not self.active:
            return
        
        if self.format_box:
            if self.format_box.rect.collidepoint(pygame.mouse.get_pos()):
                return
            
            self.format_box.deregister()
            self.format_box = None
        
        self.end_field()
    
    def activate(self) -> None:
        self.cursor_active = True
        self.cursor_timer.start()
        
        self.__draw_text()
        
        self.active = True
        event_bus.sign('typing_register', self)
        
    def on_click(self) -> None:
        if not self.hovering:
            return
        
        if self.format_box and not self.format_box.hovering:
            self.format_box.deregister()
            self.format_box = None
        
        if self.active and not (self.format_box and self.format_box.hovering):
            mouse = pygame.mouse.get_pos()
            self.cursor_mouse_pos = (mouse[0] - self.rect.x, mouse[1] - self.rect.y)
            
            self.__reset_selection()
            self.cursor_selection = True
            self.cursor_selection_start = (mouse[0] - self.rect.x, mouse[1] - self.rect.y)
        
        self.activate()
        
    def on_release(self) -> None:
        self.cursor_selection = False
        
    def mouse_scroll_down(self) -> None:
        if len(self.lines) <= self.box_size[1]:
            return
        
        self.offset = min(self.offset + 1, len(self.lines) - self.box_size[1])
        self.__draw_text()
        
    def mouse_scroll_up(self) -> None:
        if len(self.lines) <= self.box_size[1]:
            return
        
        self.offset = max(self.offset - 1, 0)
        self.__draw_text()
        
    def __set_cursor_pos(self, pos: tuple[int, int]) -> None:
        self.cursor_pos = (pos[0] - CURSOR_OFFSET[0], pos[1] - CURSOR_OFFSET[1])
        
    def __create_lines(self) -> None:
        self.lines = []
        
        words: list[str] = self.text.split(' ')
        text: str = ''
        
        bold: bool = False
        
        index: int = 0
        text_size: int = 0
        
        limit: int = self.size[0] - 15
        
        for word in words:
            
            for _i in range(len(' ' + word)):
                if f_data := self.formating.get(index + _i):
                    if f_data.format_type == Format.NEW_LINE:
                        self.lines.append(text)
                        text = ''
                        text_size = 0
                        
                    if f_data.format_type == Format.BOLD or f_data.format_type == Format.COLOR:
                        bold = True
                    elif f_data.format_type == Format.BOLD_OFF or f_data.format_type == Format.COLOR_OFF:
                        bold = False
                        
            if text_size + self.font_bolded.size(word + ' ')[0] >= limit:
                self.lines.append(text)
                text = ''
                text_size = 0
                
            text += word + ' '
            index += len(word + ' ')
                
            if bold:
                render: pygame.Surface = self.font_bolded.render(word + ' ', True, '#000000')
                text_size += render.width
            else:
                render: pygame.Surface = self.font.render(word + ' ', True, '#000000')
                text_size += render.width
                
        self.lines.append(text[:-1])
        
    def __draw_multiline_text(self) -> None:
        y: int = 5
        x: int = 8
        
        self.bold = False
        self.italic = False
        self.color = False
        self.color_data = ''
        
        bold: bool = False
        italic: bool = False
        color: bool = False
        color_data: str = ''
        
        sel_low: tuple[int, int] = ()
        sel_high: tuple[int, int] = ()
        is_highlighted: bool = False
        if self.cursor_selection_end:
            self.highlighted_text = ''
            if self.cursor_selection_start[1] < self.cursor_selection_end[1]:
                sel_low = (self.cursor_selection_start[0], (self.cursor_selection_start[1] - 5) // 25)
                sel_high = (self.cursor_selection_end[0], (self.cursor_selection_end[1] - 5) // 25)
                
            elif self.cursor_selection_start[1] > self.cursor_selection_end[1]:
                sel_low = (self.cursor_selection_end[0], (self.cursor_selection_end[1] - 5) // 25)
                sel_high = (self.cursor_selection_start[0], (self.cursor_selection_start[1] - 5) // 25)
                
            elif self.cursor_selection_start[0] < self.cursor_selection_end[0]:
                sel_low = (self.cursor_selection_start[0], (self.cursor_selection_start[1] - 5) // 25)
                sel_high = (self.cursor_selection_end[0], (self.cursor_selection_end[1] - 5) // 25)
                
                
            else:
                sel_low = (self.cursor_selection_end[0], (self.cursor_selection_end[1] - 5) // 25)
                sel_high = (self.cursor_selection_start[0], (self.cursor_selection_start[1] - 5) // 25)
                
        self.cursor_selection_indexs = (sys.maxsize, 0)
                
        # [(minX, maxX, minY, maxY, advance**), ...]
        text_metrics: list[tuple[int, ...]] = self.font.metrics(self.text)
        
        index: int = 0
        for l_index, line in enumerate(self.lines):
            if l_index <= self.offset - 1:
                index += len(line)
                continue
            
            if l_index > self.box_size[1] + self.offset:
                index += len(line)
                continue
            
            chars: list[str] = list(line)
            
            for char in chars:
                
                is_highlighted = False
            
                if sel_low and l_index - self.offset == sel_low[1] and l_index - self.offset == sel_high[1]:
                    if sel_low[0] < x + (text_metrics[index][4] / 4) and x + (text_metrics[index][4] / 4) < sel_high[0]:
                        self.cursor_selection_indexs = (
                            min(index, self.cursor_selection_indexs[0]),
                            max(index, self.cursor_selection_indexs[1])
                        )
                        is_highlighted = True
                        
                elif sel_low and l_index - self.offset == sel_low[1]:
                    if sel_low[0] < x + (text_metrics[index][4] / 4):
                        self.cursor_selection_indexs = (
                            min(index, self.cursor_selection_indexs[0]),
                            self.cursor_selection_indexs[1]
                        )
                        is_highlighted = True
                        
                elif sel_low and l_index - self.offset == sel_high[1]:
                    if x + (text_metrics[index][4] / 4) < sel_high[0]:
                        self.cursor_selection_indexs = (
                            self.cursor_selection_indexs[0],
                            max(index, self.cursor_selection_indexs[1])
                        )
                        is_highlighted = True
                        
                elif sel_low and sel_low[1] < l_index - self.offset and l_index - self.offset < sel_high[1]:
                    is_highlighted = True
                
                f_data: FormatData = self.formating.get(index)
                if not f_data:
                    f_data = FormatData(Format.NONE, '')
                    
                if f_data.format_type == Format.COLOR:
                    color = True
                    color_data = f_data.data
                elif f_data.format_type == Format.COLOR_OFF:
                    color = False
                    color_data = ''    
                
                elif f_data.format_type == Format.BOLD:
                    bold = True
                elif f_data.format_type == Format.BOLD_OFF:
                    bold = False
                    
                elif f_data.format_type == Format.ITALIC:
                    italic = True
                elif f_data.format_type == Format.ITALIC_OFF:
                    italic = False
                    
                if self.cursor_index == index:
                    self.bold = bold
                    self.italic = italic
                    self.color = color
                    self.color_data = color_data
                    
                    self.__set_cursor_pos((x, y))
                    
                if color:
                    render: pygame.Surface = self.render_text(char, color_data, (x, y), is_highlight=is_highlighted, is_bolded=True)
                elif bold:
                    render: pygame.Surface = self.render_text(char, '#ffffff', (x, y), is_highlight=is_highlighted, is_bolded=True)
                elif italic:
                    render: pygame.Surface = self.render_text(char, '#ffffff', (x, y), is_highlight=is_highlighted, is_italic=True)
                    x -= render.width
                    x += max(self.font.metrics(char)[index][1], self.font.metrics(char)[index][4])
                else:
                    render: pygame.Surface = self.render_text(char, '#ffffff', (x, y), is_highlight=is_highlighted)
                    
                x += render.width
                index += 1
                
                if self.cursor_mouse_pos[0] < x + (render.width / 2) and self.cursor_mouse_pos[1] // 25 == l_index - self.offset:
                    self.__set_cursor_pos((x - render.width, y))
                    self.cursor_mouse_pos = CURSOR_MOUSE_POS_DEFUALT
                    self.cursor_index = index
                                    
            if line == self.lines[-1]:
                continue
            
            y += 25
            x = 8
            
        if (f_data := self.formating.get(index)):
            if f_data.format_type == Format.BOLD:
                bold = True
            elif f_data.format_type == Format.BOLD_OFF:
                bold = False
                
            elif f_data.format_type == Format.ITALIC:
                italic = True
            elif f_data.format_type == Format.ITALIC_OFF:
                italic = False
                
            elif f_data.format_type == Format.COLOR:
                color = True
                color_data = f_data.data
            elif f_data.format_type == Format.COLOR_OFF:
                color = False
                color_data = ''
                
        if (self.cursor_mouse_pos[1] // 25) == l_index - self.offset and self.cursor_mouse_pos[0] > x:
            self.cursor_index = CURSOR_END
                
        if self.cursor_index == CURSOR_END:
            self.bold = bold
            self.italic = italic
            self.color = color
            self.color_data = color_data
            
            self.__set_cursor_pos((x, y))
        
    def __draw_text(self) -> None:
        self.text_face.fill((0, 0, 0, 0))
        
        if self.box_size[1] > 1:
            self.__create_lines()
            self.__draw_multiline_text()
            return
        
        text: str = self.text
        if self.prefix:
            text = self.prefix + self.text
        
        text_size: tuple[int, int] = self.font.size(text)
        surf_size: tuple[int, int] = self.text_face.size
        pos: tuple[int, int] = (
            (surf_size[0] / 2) - (text_size[0] / 2),
            (surf_size[1] / 2) - (text_size[1] / 2)
        )
        
        # [(minX, maxX, minY, maxY, advance**), ...]
        text_metrics: list[tuple[int, ...]] = self.font.metrics(text)
        
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
        index: int = 0
        for char in text:
            if char == self.prefix:
                self.render_text(char, '#ffffff', pos)
                pos = (pos[0] + text_metrics[index][4], pos[1])
                text_metrics.pop(index)
                continue
            
            if sel_low and sel_low[0] < pos[0] + (text_metrics[index][4] / 2) and pos[0] + (text_metrics[index][4] / 2) < sel_high[0]:
                self.cursor_selection_indexs = (
                    min(index, self.cursor_selection_indexs[0]),
                    max(index, self.cursor_selection_indexs[1])
                )
                self.render_text(char, '#ffffff', pos, is_highlight=True)
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
                
            index += 1
                
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