import pygame

from editor.cardComponents.cardComponent import CardComponent


LEVEL_END = False
LEVEL_TOPLEFT = True

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
        self.levelPosition: bool = LEVEL_END
        
    def draw(self, screen):
        super().draw(screen)    
        
        self.text_face.fill((0,0,0,0))
        self._render_small_case(self.name, 0)
        
        self.image.blit(self.text_face, (0, 0))
        
        screen.blit(self.image, self.pos)
    
    def load(self, data: dict[str]) -> None:
        self.name = data['name']
        self.level = data['level']
        self.levelPosition = data['levelPosition']