import pygame

from singletons import resourceHandler
from uiComponents.button import Button


BACKGROUND_TILE_SIZE: int = 11
BACKGROUND_TILE_SIZE_X2: int = 22

class TextFormatBox():
    def __init__(self, pos: tuple[int, int], textbox: object) -> None:
        self.pos: tuple[int, int] = pos
        self.size: tuple[int, int] = (176, 44)
        
        from uiComponents.textBox import TextBox
        self.textbox: TextBox = textbox
        
        self.image: pygame.Surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.rect: pygame.Rect = self.image.get_rect(topleft=self.pos)
        
        self.background: pygame.Surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.__draw_background()
        
        self.hovering: bool = False
        
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
            pos=(self.size[0] - 37, 6), 
            size=(32, 34),
            image='.\\assets\\icons\\AddButton.png',
            image_hover='.\\assets\\icons\\AddButton_hover.png',
            command=None
        )
        
    def deregister(self) -> None:
        pass
        
    def draw(self, screen: pygame.Surface) -> None:
        self.image.fill((0,0,0,0))
        self.image.blit(self.background)
        
        screen.blit(self.image, self.pos)
        
        if self.textbox.bold: self.bold_button.active = True
        self.bold_button.draw(screen, self.pos)
        
        if self.textbox.italic: self.italic_button.active = True
        self.italic_button.draw(screen, self.pos)
        
        
        if self.textbox.color and self.textbox.color_data == '#D34D35': 
            self.ability_button.active = True
            
        if self.ability_button.hovering:
            pygame.draw.rect(screen, '#E5553B', (self.ability_button.rect.x + 3, self.ability_button.rect.y + 3, 26, 27))
        else:
            pygame.draw.rect(screen, '#D34D35', (self.ability_button.rect.x + 3, self.ability_button.rect.y + 3, 26, 27))
            
        self.ability_button.draw(screen, self.pos)
        
        if self.textbox.color and self.textbox.color_data == '#2D638E': 
            self.attribute_button.active = True
        
        if self.attribute_button.hovering:
            pygame.draw.rect(screen, '#3371A0', (self.attribute_button.rect.x + 3, self.attribute_button.rect.y + 3, 26, 27))
        else:
            pygame.draw.rect(screen, '#2D638E', (self.attribute_button.rect.x + 3, self.attribute_button.rect.y + 3, 26, 27))
        self.attribute_button.draw(screen, self.pos)
        
        self.add_color_button.draw(screen, self.pos)
        
    def no_hover(self) -> None:
        if not self.hovering:
            return
        self.hovering = False

    def hover(self) -> None:
        self.hovering = True
        
        mouse_pos = pygame.mouse.get_pos()
        
        self.bold_button.no_hover()
        if self.bold_button.rect.collidepoint(mouse_pos):
            self.bold_button.hover()
            
        self.italic_button.no_hover()
        if self.italic_button.rect.collidepoint(mouse_pos):
            self.italic_button.hover()
            
        self.ability_button.no_hover()
        if self.ability_button.rect.collidepoint(mouse_pos):
            self.ability_button.hover()
            
        self.attribute_button.no_hover()
        if self.attribute_button.rect.collidepoint(mouse_pos):
            self.attribute_button.hover()
            
        self.add_color_button.no_hover()
        if self.add_color_button.rect.collidepoint(mouse_pos):
            self.add_color_button.hover() 
        
    def toggle_color(self) -> None:
        if self.ability_button.hovering:
            self.textbox.toggle_color('#D34D35')
            
        elif self.attribute_button.hovering:
            self.textbox.toggle_color('#2D638E')
    
    def __draw_background(self) -> None:
        _background: dict[str, pygame.Surface] = TextFormatBox.__split_background()

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