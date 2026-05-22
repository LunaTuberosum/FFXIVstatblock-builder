import re
import pygame

from singletons import resourceHandler
from singletons.dataBus import data_bus

from uiComponents.button import Button


BACKGROUND_TILE_SIZE: int = 11
BACKGROUND_TILE_SIZE_X2: int = 22

class TextFormatBox():
    def __init__(self, pos: tuple[int, int], textbox: object) -> None:
        self.colors: dict[str, Button] = {}
        
        self.pos: tuple[int, int] = pos
        self.size: tuple[int, int] = (177, 44)
        
        from uiComponents.textBox import TextBox
        self.textbox: TextBox = textbox
        
        self.image: pygame.Surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.rect: pygame.Rect = self.image.get_rect(bottomleft=self.pos)
        
        self.background: pygame.Surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.background = self.__draw_background()
        
        self.hovering: bool = False
        
        self.add_background: pygame.Surface = self.__draw_background((166, 44))
        self.add_rect: pygame.Rect = self.add_background.get_rect(topleft=(self.rect.x + 10, self.rect.y - 40))
        
        self.color_textbox: TextBox = TextBox(
            pos=(47, -33), 
            size=(90, 1)
        )
        self.color_textbox.change_text('FFFFFF')
        self.color_textbox.add_command(self.format_color)
        self.color_textbox.add_prefix('#')
        self.color_textbox.add_char_limit(6)
        
        self.color_confirm_button: Button = Button(
            pos=(138, -34),
            size=(32, 34),
            image='.\\assets\\icons\\ConfirmButton.png',
            image_hover='.\\assets\\icons\\ConfirmButton_hover.png',
            command=self.color_confirm
        )
        self.color_text_active: bool = False
        
        self.bold_button: Button = Button(
            pos=(7, 6), 
            size=(32, 34),
            image='.\\assets\\icons\\BoldButton.png',
            image_hover='.\\assets\\icons\\BoldButton_hover.png',
            command=self.textbox.toggle_bold
        )
        
        self.italic_button: Button = Button(
            pos=(40, 6), 
            size=(32, 34),
            image='.\\assets\\icons\\ItalicButton.png',
            image_hover='.\\assets\\icons\\ItalicButton_hover.png',
            command=self.textbox.toggle_italic
        )
        
        self.ability_button: Button = Button(
            pos=(73, 6), 
            size=(32, 34),
            image='.\\assets\\icons\\ColorOverButton.png',
            image_hover='.\\assets\\icons\\ColorOverButton_hover.png',
            command=self.toggle_color
        )
        
        self.attribute_button: Button = Button(
            pos=(106, 6), 
            size=(32, 34),
            image='.\\assets\\icons\\ColorOverButton.png',
            image_hover='.\\assets\\icons\\ColorOverButton_hover.png',
            command=self.toggle_color
        )
        
        self.add_color_button: Button = Button(
            pos=(self.size[0] - 39, 6), 
            size=(32, 34),
            image='.\\assets\\icons\\AddButton.png',
            image_hover='.\\assets\\icons\\AddButton_hover.png',
            command=self.add_color
        )
        
        colors: list[str] = data_bus.sign('get_colors')
        if colors:
            for color in colors:
                self.__add_color_button(color)
        
    def deregister(self) -> None:
        self.color_textbox.deregister()
        self.color_confirm_button.deregister()
        
        self.bold_button.deregister()
        self.italic_button.deregister()
        self.ability_button.deregister()
        self.attribute_button.deregister()
        self.add_color_button.deregister()
        
    def draw(self, screen: pygame.Surface) -> None:
        self.image.fill((0,0,0,0))
        self.image.blit(self.background)
        
        mouse_pos = pygame.mouse.get_pos()
        
        if self.bold_button.is_hover(mouse_pos):
            self.bold_button.hover()
        else:
            self.bold_button.no_hover()
            
        if self.italic_button.is_hover(mouse_pos):
            self.italic_button.hover()
        else:
            self.italic_button.no_hover()
            
        if self.ability_button.is_hover(mouse_pos):
            self.ability_button.hover()
        else:
            self.ability_button.no_hover()
            
        if self.attribute_button.is_hover(mouse_pos):
            self.attribute_button.hover()
        else:
            self.attribute_button.no_hover()
            
        if self.add_color_button.is_hover(mouse_pos):
            self.add_color_button.hover() 
        else:
            self.add_color_button.no_hover()
        
        if self.color_text_active:
            if self.color_textbox.is_hover(mouse_pos):
                self.color_textbox.hover()
            else:
                self.color_textbox.no_hover()
                
            if self.color_confirm_button.is_hover(mouse_pos):
                self.color_confirm_button.hover()
            else:
                self.color_confirm_button.no_hover()
            
            screen.blit(self.add_background, (self.rect.x + 10, self.rect.y - 40))
            
            color: str = '#{message:{fill}{align}{width}}'.format(
                message=re.sub(r'[g-zG-Z]', 'F', self.color_textbox.text),
                fill='F',
                align='<',
                width=6
            )
            pygame.draw.rect(screen, color, (self.rect.x + 17, self.rect.y - 33, 30, 30), border_radius=5)
            pygame.draw.rect(screen, '#C4A463', (self.rect.x + 17, self.rect.y - 33, 30, 30), width=1, border_radius=5)
            
            self.color_textbox.draw(screen, self.rect.topleft)
            self.color_confirm_button.draw(screen, self.rect.topleft)
        
        screen.blit(self.image, self.rect.topleft)
        
        if self.textbox.bold: self.bold_button.active = True
        self.bold_button.draw(screen, self.rect.topleft)
        
        if self.textbox.italic: self.italic_button.active = True
        self.italic_button.draw(screen, self.rect.topleft)
        
        
        if self.textbox.color and self.textbox.color_data == '#D34D35': 
            self.ability_button.active = True
            
        if self.ability_button.hovering:
            pygame.draw.rect(screen, '#E5553B', (self.ability_button.rect.x + 3, self.ability_button.rect.y + 3, 26, 27))
        else:
            pygame.draw.rect(screen, '#D34D35', (self.ability_button.rect.x + 3, self.ability_button.rect.y + 3, 26, 27))
            
        self.ability_button.draw(screen, self.rect.topleft)
        
        if self.textbox.color and self.textbox.color_data == '#2D638E': 
            self.attribute_button.active = True
        
        if self.attribute_button.hovering:
            pygame.draw.rect(screen, '#306B99', (self.attribute_button.rect.x + 3, self.attribute_button.rect.y + 3, 26, 27))
        else:
            pygame.draw.rect(screen, '#2D638E', (self.attribute_button.rect.x + 3, self.attribute_button.rect.y + 3, 26, 27))
        self.attribute_button.draw(screen, self.rect.topleft)
        
        for color, button in self.colors.items():
            button.no_hover()
            if button.is_hover(mouse_pos):
                button.hover()
                
            if self.textbox.color and self.textbox.color_data == color:
                button.active = True
            
            pygame.draw.rect(screen, color, (button.rect.x + 3, button.rect.y + 3, 26, 27))
            if button.hovering:
                hover = pygame.Surface((26, 27), pygame.SRCALPHA)
                hover.fill((226, 226, 226, 140))
                screen.blit(hover, (button.rect.x + 3, button.rect.y + 3))
                
            button.draw(screen, self.rect.topleft)
        
        if self.color_text_active:
            self.add_color_button.active = True
            
        self.add_color_button.draw(screen, self.rect.topleft)
        
    def no_hover(self) -> None:
        if not self.hovering:
            return
        
        self.hovering = False

    def hover(self) -> None:
        self.hovering = True      
        
    def is_hover(self, mouse_pos: tuple[int, int]) -> None:
        is_hover: bool = False
        if self.color_text_active and self.add_rect.collidepoint(mouse_pos):
            is_hover = True
            
        return is_hover or self.rect.collidepoint(mouse_pos)
            
    def toggle_color(self) -> None:
        if self.ability_button.hovering:
            self.textbox.toggle_color('#D34D35')
            return
            
        elif self.attribute_button.hovering:
            self.textbox.toggle_color('#2D638E')
            return
            
        for color, button in self.colors.items():
            if button.hovering:
                self.textbox.toggle_color(color)
                return
    
    def format_color(self, box) -> None:
        text = re.sub(r'[g-zG-Z]', 'F', self.color_textbox.text)
        self.color_textbox.change_text(text.upper())
    
    def add_color(self) -> None:
        if self.color_text_active:
            self.color_text_active = False
            return
            
        self.color_text_active = True
    
    def color_confirm(self) -> None:
        if color := self.__add_color_button(self.color_textbox.text):
            data_bus.sign('add_color', color)
        
        self.color_textbox.change_text('FFFFFF')
        self.color_confirm_button.no_hover()
        self.color_textbox.no_hover()
        self.color_textbox.check_off_click()
        self.color_text_active = False
        
    def __add_color_button(self, color_text: str) -> str:
        color: str = '#{message:{fill}{align}{width}}'.format(
            message=re.sub(r'[g-zG-Z]', 'F', color_text),
            fill='F',
            align='<',
            width=6
        )
        
        if color in self.colors:
            return None
        
        self.colors[color] = Button(
            pos=(139 + (33 * len(self.colors)), 6),
            size=(32, 34),
            image='.\\assets\\icons\\ColorOverButton.png',
            image_hover='.\\assets\\icons\\ColorOverButton_hover.png',
            command=self.toggle_color
        )
        
        self.size = (
            177 + (33 * len(self.colors)),
            44
        )
        
        self.add_color_button.pos = (self.size[0] - 39, 6)
        
        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        self.rect = self.image.get_rect(bottomleft=self.pos)
        self.background = self.__draw_background()
        
        return color
    
    def __draw_background(self, set_size: tuple[int, int] = (0, 0)) -> pygame.Surface:
        size: tuple[int, int] = set_size if set_size[0] else self.size
        
        background: dict[str, pygame.Surface] = TextFormatBox.__split_background()
        background_surface: pygame.Surface = pygame.Surface(size, pygame.SRCALPHA)
        

        background_surface.blit(
            background['TopLeft'], 
            (
                0, 
                0
            )
        )
        background_surface.blit(
            background['TopRight'], 
            (
                size[0] - BACKGROUND_TILE_SIZE, 
                0
            )
        )
        background_surface.blit(
            background['BottomLeft'], 
            (
                0, 
                size[1] - BACKGROUND_TILE_SIZE
            )
        )
        background_surface.blit(
            background['BottomRight'], 
            (
                size[0] - BACKGROUND_TILE_SIZE, 
                size[1] - BACKGROUND_TILE_SIZE
            )
        )

        background_surface.blit(
            pygame.transform.scale(
                background['TopMiddle'], 
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
        background_surface.blit(
            pygame.transform.scale(
                background['Left'], 
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
        background_surface.blit(
            pygame.transform.scale(
                background['Right'], 
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
        background_surface.blit(
            pygame.transform.scale(
                background['BottomMiddle'], 
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

        background_surface.blit(
            pygame.transform.scale(
                background['Middle'], 
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
        
        return background_surface
               
    def __split_background() -> dict[str, pygame.Surface]:
        _img = resourceHandler.load_image('.\\assets\\backgrounds\\TextBoxFormatBackground.png')

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
        _temp['TopRight'].blit(_img, (-BACKGROUND_TILE_SIZE_X2 - BACKGROUND_TILE_SIZE, 0))

        _temp['Left'] = pygame.surface.Surface((BACKGROUND_TILE_SIZE, BACKGROUND_TILE_SIZE), pygame.SRCALPHA)
        _temp['Left'].blit(_img, (0, -BACKGROUND_TILE_SIZE))
        _temp['Middle'] = pygame.surface.Surface((BACKGROUND_TILE_SIZE, BACKGROUND_TILE_SIZE), pygame.SRCALPHA)
        _temp['Middle'].blit(_img, (-BACKGROUND_TILE_SIZE, -BACKGROUND_TILE_SIZE))
        _temp['Right'] = pygame.surface.Surface((BACKGROUND_TILE_SIZE, BACKGROUND_TILE_SIZE), pygame.SRCALPHA)
        _temp['Right'].blit(_img, (-BACKGROUND_TILE_SIZE_X2 - BACKGROUND_TILE_SIZE, -BACKGROUND_TILE_SIZE - BACKGROUND_TILE_SIZE))

        _temp['BottomLeft'] = pygame.surface.Surface((BACKGROUND_TILE_SIZE, BACKGROUND_TILE_SIZE), pygame.SRCALPHA)
        _temp['BottomLeft'].blit(_img, (0, -BACKGROUND_TILE_SIZE_X2 - BACKGROUND_TILE_SIZE))
        _temp['BottomMiddle'] = pygame.surface.Surface((BACKGROUND_TILE_SIZE, BACKGROUND_TILE_SIZE), pygame.SRCALPHA)
        _temp['BottomMiddle'].blit(_img, (-BACKGROUND_TILE_SIZE, -BACKGROUND_TILE_SIZE_X2 - BACKGROUND_TILE_SIZE))
        _temp['BottomRight'] = pygame.surface.Surface((BACKGROUND_TILE_SIZE, BACKGROUND_TILE_SIZE), pygame.SRCALPHA)
        _temp['BottomRight'].blit(_img, (-BACKGROUND_TILE_SIZE_X2 - BACKGROUND_TILE_SIZE, -BACKGROUND_TILE_SIZE_X2 - BACKGROUND_TILE_SIZE))

        return _temp