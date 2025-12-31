import pygame

from editor.cardComponents.cardComponent import CardComponent

from singletons import resourceHandler

from singletons.eventBus import event_bus

from uiComponents.textFormat import Format, FormatData


class TraitComponent(CardComponent):
    def __init__(self, card: object) -> None:
        super().__init__(
            name='TraitComponent',
            size=(518, 40),
            pos=(12, 12),
            card=card
        )
        
        self.font_title: pygame.Font = resourceHandler.load_font('.\\assets\\fonts\\NotoSans-Bold.ttf', 19)
        self.font: pygame.Font = resourceHandler.load_font('.\\assets\\fonts\\noto-sans.regular.ttf', 15)

        self.font_bolded: pygame.Font = resourceHandler.load_font('.\\assets\\fonts\\noto-sans.regular.ttf', 15)
        self.font_bolded.bold = True

        self.font_italic: pygame.Font = resourceHandler.load_font('.\\assets\\fonts\\noto-sans.regular.ttf', 15)
        self.font_italic.italic = True
        
        self.name: str = ''
        self.formating: dict[int, FormatData] = {}
        self.desc: str = ''
        
        self.lines: list[str] = []
        
    def draw(self, screen: pygame.Surface) -> None:
        super().draw(screen)    
                
        self.image.blit(self.text_face, (0, 0))
        
        if not self.is_last:
            self.image.blit(self.divider, (0, self.rect.height - 5))
            
        screen.blit(self.image, (self.pos[0] + self.offset[0], self.pos[1] + self.offset[1]), special_flags=pygame.BLEND_RGBA_MIN if self.hovering else 0)
        
    def on_click(self) -> None:
        if not self.hovering:
            return
        
        from editor.ui.traitElement import TraitElement
        event_bus.sign('ui_window',TraitElement(self))
        
    def load(self, data: dict[str]) -> None:
        self.name = data['name']
        self.desc = data['desc']
        
        for index, f_data in data['format'].items():
            self.formating[int(index)] = FormatData(Format(f_data['type']), f_data['data'])
            
        self.__find_size()
        
        self.__draw_text_face()
    
    def refresh(self) -> None:
        self.__find_size()
        self.__draw_text_face()
            
    def __find_size(self) -> None:
        self.lines = []
        
        words: list[str] = self.desc.split(' ')
        text: str = ''
        
        bold: bool = False
        
        index: int = 0
        text_size: int = 0
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
            
            if text_size + self.font_bolded.size(word + ' ')[0] >= 500:
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
                
        self.lines.append(text)
        
        self.size = (518, 40 + (16 * len(self.lines)))
        
        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=self.pos)
        
        self.text_face = pygame.Surface(self.size, pygame.SRCALPHA)
        
    def __draw_text_face(self) -> None:
        self.text_face.fill((0,0,0,0))
        
        self.text_face.blit(self.font_title.render(self.name, True, '#000000'), (1,0))
        
        y: int = 26
        x: int = 0
        
        bold: bool = False
        italic: bool = False
        color: bool = False
        color_data: str = ''
        
        index: int = 0
        for line in self.lines:
            chars: list[str] = list(line)
            
            for char in chars:
                f_data: FormatData = self.formating.get(index)
                if not f_data:
                    f_data = FormatData(Format.NONE, '')
                    
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
                
                if bold:
                    render: pygame.Surface = self.font_bolded.render(char, True, '#000000')
                elif italic:
                    render: pygame.Surface = self.font_italic.render(char, True, '#000000')
                elif color:
                    render: pygame.Surface = self.font_bolded.render(char, True, color_data)
                else:
                    render: pygame.Surface = self.font.render(char, True, '#000000')
                    
                self.text_face.blit(render, (x, y))
                x += render.width
                index += 1
                
            y += 16
            x = 0
        