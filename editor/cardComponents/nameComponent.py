import pygame

from editor.cardComponents.cardComponent import CardComponent

from singletons.eventBus import event_bus


LEVEL_NUM: int = 0
LEVEL_TIER: int = 1

LEVEL_END: bool = False
LEVEL_TOPRIGHT: bool = True

NAME_LIMIT_END: int = 512
NAME_LIMIT_TOPLEFT: int = 500

BASE_HEIGHT: int = 36
LINE_HEIGHT: int = 30

class NameComponent(CardComponent):
    def __init__(self, card: object, is_tier: bool = False) -> None:
        super().__init__(
            name='NameComponent',
            size=(512, 36),
            pos=(12, 5),
            card=card
        )
        
        self.name: str = 'Character Name'
        self.level_type: int = LEVEL_NUM if not is_tier else LEVEL_TIER
        self.level: str = '00' if self.level_type == LEVEL_NUM else 'Mob'
        self.level_position: bool = LEVEL_TOPRIGHT

        self.__draw_text_face()
        
    def draw(self, screen: pygame.Surface) -> None:
        super().draw(screen)    
                
        self.image.blit(self.text_face, (0, 0))
        
        screen.blit(self.image, (self.pos[0] + self.offset[0], self.pos[1] + self.offset[1]))
        
    def on_click(self) -> None:
        if not self.hovering:
            return
        
        if self.click_timer.time_left() < 0:
            self.click_timer.start()
            return
        
        from editor.ui.nameElement import NameElement
        event_bus.sign('ui_window', NameElement(self))
    
    def save(self) -> dict:
        return {
            'name': self.name,
            'is_tier': self.level_type == LEVEL_TIER,
            'level': self.level,
            'levelPosition': self.level_position
        }
    
    def load(self, data: dict[str]) -> None:
        self.name = data['name']
        self.level_type = LEVEL_TIER if data['is_tier'] else LEVEL_NUM
        self.level = data['level']
        self.level_position = data['levelPosition']

        self.__draw_text_face()
        
    def refresh(self) -> None:
        self.__draw_text_face()
        
    def __draw_text_face(self) -> None:
        self.text_face.fill((0,0,0,0))
        
        level: str = f'[L{self.level}]'
        
        if self.level_type == LEVEL_TIER:
            level = f'{self.level}'
            
            if self.level_position == LEVEL_END:
                level = f'[{self.level}]'
            
        level_size: tuple[int, int] = (
            self.font_cap.size(level[0])[0] + self.font.size(level[1:])[0],
            self.font_tiny.size(level)[1]
        )
        
        limit: int = NAME_LIMIT_TOPLEFT - level_size[0]
        
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
            self._render_tiny_case(level, (limit, 0))
            
        
        