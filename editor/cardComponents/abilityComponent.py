import pygame

from editor.cardComponents.cardComponent import CardComponent

from singletons import resourceHandler

from singletons.eventBus import event_bus

from uiComponents.textFormat import Format, FormatData


class EffectData():
    def __init__(self, desc: str, format_data: dict[int, FormatData], in_line: bool) -> None:
        self.desc: str = desc
        self.format_data: dict[int, FormatData] = format_data
        self.in_line: bool = in_line

class AbilityComponent(CardComponent):
    def __init__(self, card: object) -> None:
        super().__init__(
            name='AbilityComponent',
            size=(518, 40),
            pos=(12, 12),
            card=card
        )
        
        self.invk_image: pygame.Surface = resourceHandler.load_image('.\\assets\\icons\\INVK.png')
        
        self.font_title: pygame.Font = resourceHandler.load_font('.\\assets\\fonts\\NotoSans-Bold.ttf', 19)
        self.font: pygame.Font = resourceHandler.load_font('.\\assets\\fonts\\noto-sans.regular.ttf', 15)

        self.font_bolded: pygame.Font = resourceHandler.load_font('.\\assets\\fonts\\noto-sans.regular.ttf', 15)
        self.font_bolded.bold = True

        self.font_italic: pygame.Font = resourceHandler.load_font('.\\assets\\fonts\\noto-sans.regular.ttf', 15)
        self.font_italic.italic = True
        
        self.name: str = ''
        self.types: str = ''
        self.effects: dict[str, EffectData] = {}
        self.formating: dict[int, FormatData] = {}
        
        self.marker = None # TODO
        
        self.invk: bool = False
        
        self.lines: list[str] = []
        
    def draw(self, screen: pygame.Surface) -> None:
        x: int = self.pos[0]
        y: int = self.pos[1]
        
        if self.drag:
            self.hovering = True
            mouse: tuple[int, int] = pygame.mouse.get_pos()
            card_width: int = self.card.width / 3
            x =  min(max(mouse[0] - self.drag_pos[0] - self.rect.x + self.pos[0], -self.offset[0] + 32), ((card_width - 1) * 540) - self.offset[0] + (60 if card_width > 2 else 30))
            y =  min(max(mouse[1] - self.drag_pos[1] - self.rect.y + self.pos[1], -self.offset[1] + 32), self.card.size[1] - self.offset[1] - self.rect.height - 20)            
            
        super().draw(screen)    
        
        self.image.blit(self.text_face, (0, 0))
        
        if not self.is_last:
            self.image.blit(self.divider, (0, self.rect.height - 5))
            
        if self.drag:       
            screen.blit(self.image, (x + self.offset[0], y + self.offset[1]))
        else:
            screen.blit(self.image, (x + self.offset[0], y + self.offset[1]), special_flags=pygame.BLEND_RGBA_MIN if self.hovering else 0)
            
    def on_click(self) -> None:
        if not self.hovering:
            return
        
        if not super().on_click():
            return
               
        # from editor.ui.traitElement import TraitElement
        # event_bus.sign('ui_window', TraitElement(self))
        
    def on_release(self) -> None:
        if not super().on_release():
            return
        
        event_bus.sign('swap_abilites', self)
        
    def load(self, data: dict[str]) -> None:
        self.name = data['name']
        self.invk = data['invk']
        self.types = data['types']
        
        for effect_name, effect_data in data['effects'].items():
            
            formating: dict[int, FormatData] = {}
            for index, f_data in effect_data['format'].items():
                formating[int(index)] = FormatData(Format(f_data['type']), f_data['data'])
                
            self.effects[effect_name] = EffectData(effect_data['desc'], formating, effect_data['in_line'])
            
        self.__find_size()
        
        self.__draw_text_face()
    
    def refresh(self) -> None:
        self.__find_size()
        self.__draw_text_face()
        
    def __find_size(self) -> None:
        size: int = 0
        
        limit: int = self.size[0] - 20
        bold: bool = False
        
        if self.marker:
            limit -= 20
            
            
        index: int = 0
        text: str = ''
        for name, effect_data in self.effects.items():
            self.formating[index] = FormatData(Format.EFFECT_NAME, '')
            text = name + ': '
            
            index += len(text) - 1
            self.formating[index] = FormatData(Format.EFFECT_NAME_OFF, '')
            index += 1
            
            if effect_data.in_line:
                text = self.lines.pop() + text
            
            size = self.font_bolded.size(name)[0]
            
            effect_index: int = 0
            for word in effect_data.desc.split():
                for _i in range(len(' ' + word)):
                    if f_data := effect_data.format_data.get(effect_index + _i):
                        self.formating[index + _i] = f_data
                        if f_data.format_type == Format.NEW_LINE:
                            self.lines.append(text)
                            text = ''
                            size = 0
                            
                        if f_data.format_type == Format.BOLD or f_data.format_type == Format.COLOR:
                            bold = True
                        elif f_data.format_type == Format.BOLD_OFF or f_data.format_type == Format.COLOR_OFF:
                            bold = False
                            
                if size + self.font_bolded.size(word + ' ')[0] >= limit:
                    self.lines.append(text)
                    text = ''
                    size = 0
                    
                text += word + ' '
                index += len(word + ' ')
                effect_index += len(word + ' ')
                
                if bold:
                    render: pygame.Surface = self.font_bolded.render(word + ' ', True, '#000000')
                    size += render.width
                else:
                    render: pygame.Surface = self.font.render(word + ' ', True, '#000000')
                    size += render.width
            
            self.lines.append(text)
            
        self.size = (
            518,
            40 + (18 * len(self.lines))
        )
        
        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=self.pos)
        
        self.text_face = pygame.Surface(self.size, pygame.SRCALPHA)
        
    def __draw_text_face(self) -> None:
        self.text_face.fill((0,0,0,0))
        
        self.text_face.blit(self.font_title.render(self.name, True, '#000000'), (1,0))
        
        name_width: int = self.font_title.size(self.name)[0]
        type_width: int = self.font_italic.size(self.types)[0]
        type_overflow: bool = False
        
        if self.invk:
            self.text_face.blit(self.invk_image, (0, 2))
            
            self.text_face.blit(self.font_title.render(self.name, True, '#000000'), (78, 0))
            if name_width + self.invk_image.width + 12 + type_width >= self.size[0]:
                type_overflow = True
            
        else:
            self.text_face.blit(self.font_title.render(self.name, True, '#000000'), (1, 0))
            if name_width + 12 + type_width >= self.size[0]:
                type_overflow = True
                
        self.text_face.blit(self.font_italic.render(self.types, True, '#000000'), (
            self.size[0] - type_width,
            26 if type_overflow else 4
        ))
            
        y: int = 26 + (22 if type_overflow else 0)
        x: int = 1
        
        name: bool = False
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
                    
                if f_data.format_type == Format.EFFECT_NAME:
                    name = True
                elif f_data.format_type == Format.EFFECT_NAME_OFF:
                    name = False
                    
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
                    
                if name:
                    render: pygame.Surface = self.font_bolded.render(char, True, '#995745')
                elif bold:
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
                
            y += 18
            x = 1