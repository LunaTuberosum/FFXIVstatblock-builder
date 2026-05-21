import pygame

from singletons import resourceHandler
from singletons.eventBus import event_bus

from ui.uiElement import UIElement

from uiComponents.button import Button


ELEMENT_SIZE: tuple[int, int] = (1000, 600)
W_HALF: int = 500
H_HALF: int = 300

SMALL_CASE_UPPER: int = 4
SMALL_CASE_LOWER: int = 8

class ChangelogElement(UIElement):
    def __init__(self, changelog: dict[str, tuple[str, str]], alert: bool = False):
        screen = pygame.display.get_surface()
        self.changelog: dict[str, tuple[str, str]] = changelog
        
        self.alert: bool = alert
        
        super().__init__(
            name='Changelog',
            title='Changelog',
            size=ELEMENT_SIZE,
            pos=(
                (screen.size[0] / 2) - W_HALF,
                (screen.size[1] / 2) - H_HALF,
            ),
            write_config=False
        )
        
        self.font_cap: pygame.Font = resourceHandler.load_font('.\\assets\\fonts\\LibreBaskerville.ttf', 24)
        self.font_cap_small: pygame.Font = resourceHandler.load_font('.\\assets\\fonts\\LibreBaskerville.ttf', 20)
        
        self.font_large: pygame.Font = resourceHandler.load_font('.\\assets\\fonts\\noto-sans.regular.ttf', 20)
        self.font_large.bold = True
        
        self.add_component('Left_Button', Button(
                pos=(440, 543),
                size=(34, 34),
                image='.\\assets\\icons\\left_button.png',
                image_hover='.\\assets\\icons\\left_button_hover.png',
                command=self.left
            )
        )
        self.add_component('Right_Button', Button(
                pos=(525, 543),
                size=(34, 34),
                image='.\\assets\\icons\\right_button.png',
                image_hover='.\\assets\\icons\\right_button_hover.png',
                command=self.right
            )
        )
        
        self.page: int = 0
        
        self.text_face: pygame.Surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self._render_text_face()
        
    def play_open(self):
        if self.alert:
            event_bus.sign('play_se', 'notification')
        else:
            event_bus.sign('play_se', 'open_window')
        
    def check_off_click(self) -> None:
        return
        
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
            
    def _render_small_case(self, text: str, pos: tuple[int, int]) -> None:
        characters: list[str] = list(text)
        
        x: int = pos[0]
        for char in characters:
            if char.isspace():
                x += self.font.size(' ')[0]
                
            elif char.isupper() or char.isnumeric():
                render: pygame.Surface = self.font_cap.render(char, True, '#000000')
                self.text_face.blit(render, (x, pos[1] + SMALL_CASE_UPPER + 1))
                
                render = self.font_cap.render(char, True, '#954E40')
                self.text_face.blit(render, (x, pos[1] + SMALL_CASE_UPPER))
                
                x += render.get_width()
                
            else:
                render: pygame.Surface = self.font_cap_small.render(char.upper(), True, '#000000')
                self.text_face.blit(render, (x, pos[1] + SMALL_CASE_LOWER + 1))
                
                render = self.font_cap_small.render(char.upper(), True, '#954E40')
                self.text_face.blit(render, (x, pos[1] + SMALL_CASE_LOWER))
                
                x += render.get_width()
                
    def render_text(self, text: str, color: str, pos: tuple[int, int]) -> None:
        self.text_face.blit(self.font.render(text, True, '#000000'), (pos[0], pos[1] + 1))
        self.text_face.blit(self.font.render(text, True, color), (pos[0], pos[1]))
        
    def render_text_large(self, text: str, color: str, pos: tuple[int, int]) -> None:
        self.text_face.blit(self.font_large.render(text, True, '#000000'), (pos[0], pos[1] + 1))
        self.text_face.blit(self.font_large.render(text, True, color), (pos[0], pos[1]))
            
    def _render_text_face(self):
        self.text_face.fill((0, 0, 0, 0))
        self._render_small_case(self.changelog['name'], (25, 55))
        
        self.render_text_large(str(self.page + 1), '#EEE1C5', (500 - (self.font_large.size(str(self.page + 1))[0] / 2), 545))
        
        skip: bool = True
        if self.page == 0:
            skip = False
        
        y: int = 90
        
        if self.changelog['warning'] and self.page == 0:
            y += 5
            self.render_text_large('!! WARNING !!', '#D34D35', (W_HALF - (self.font_large.size('!! WARNING !!')[0] / 2), y))
            y += 24
            
            count: int = 0
            text: str = ''
            for word in self.changelog['warning'].split():
                text += word
                count += 1
                if count == 12:
                    count = 0
                    self.render_text_large(text, '#D34D35', (W_HALF - (self.font_large.size(text)[0] / 2), y))
                    text = ''
                    y += 24
                else:
                    text += ' '
            y += 5
                
        for form, text in self.changelog['text']:
            if skip:
                if form == 'break' and text == str(self.page):
                    skip = False
                continue
            
            if form == 'title':
                y += 10
                self.render_text_large(text, '#EEE1C5', (40, y))
                y += 26
            elif form == 'text':
                self.render_text(f'- {text}', '#EEE1C5', (60, y))
                if '\n' in text:
                    y += 28
                y += 28
            elif form == 'break' and text == str(self.page + 1):
                break
            
    def left(self) -> None:
        self.page = max(self.page - 1, 0)
        self._render_text_face()
        
    def right(self) -> None:
        self.page = min(self.page + 1, self.changelog['maxPage'])
        self._render_text_face()
        