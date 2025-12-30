import pygame

from editor.cardComponents.cardComponent import CardComponent

from singletons.eventBus import event_bus


LEVEL_END = False
LEVEL_TOPRIGHT = True

NAME_LIMIT_END: int = 512
NAME_LIMIT_TOPLEFT: int = 500

BASE_HEIGHT: int = 36
LINE_HEIGHT: int = 30

class NameComponent(CardComponent):
    def __init__(self, card: object) -> None:
        super().__init__(
            name='NameComponent',
            size=(512, 36),
            pos=(32, 25),
            card=card
        )
        
        self.name: str = 'Character Name'
        self.level: str = '00'
        self.level_position: bool = LEVEL_END

        self.__draw_text_face()
        
    def draw(self, screen: pygame.Surface, offset: tuple[int, int]) -> None:
        super().draw(screen, offset)    
                
        self.image.blit(self.text_face, (0, 0))
        
        screen.blit(self.image, (self.pos[0] + offset[0], self.pos[1] + offset[1]))
        
    def on_click(self) -> None:
        if not self.hovering:
            return
        
        from editor.ui.nameElement import NameElement
        event_bus.sign('ui_window', NameElement(self))
    
    def load(self, data: dict[str]) -> None:
        self.name = data['name']
        self.level = data['level']
        self.level_position = data['levelPosition']

        self.__draw_text_face()
        
    def refresh(self) -> None:
        self.__draw_text_face()
        
    def __draw_text_face(self) -> None:
        self.text_face.fill((0,0,0,0))
        
        level: str = f'[L{self.level}]'
        
        limit: int = NAME_LIMIT_TOPLEFT - self.font_cap.size(level)[0]
        
        words: list[str] = self.name.split(' ')
        if self.level_position == LEVEL_END:
            words.append(level)
            limit = NAME_LIMIT_END
            
        text: str = ''
        lines: list[str] = []
        
        for word in words:
            if self._size_small_case(text + word) > limit:
                lines.append(text)
                text = word + ' '
                continue
            
            text += word + ' '
            
        lines.append(text)
        
        if len(lines) > 1:
            self.size = (
                NAME_LIMIT_END,
                BASE_HEIGHT + (LINE_HEIGHT * (len(lines) - 1))
            )
            
            self.image = pygame.Surface(self.size, pygame.SRCALPHA)
            self.rect = self.image.get_rect(topleft=self.pos)
            
            self.text_face = pygame.Surface(self.size, pygame.SRCALPHA)
        
        y: int = 0
        for line in lines:
            self._render_small_case(line, (0, y))
            y += LINE_HEIGHT
            
        if self.level_position == LEVEL_TOPRIGHT:
            self._render_small_case(level, (limit, 0))
            
        
        