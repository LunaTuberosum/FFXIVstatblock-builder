import pygame

from editor.cardComponents.cardComponent import CardComponent

from singletons import resourceHandler


class SectionNameComponent(CardComponent):
    def __init__(self, card: object, section: str) -> None:
        super().__init__(
            name='SectionNameComponent',
            size=(520, 42),
            pos=(10, 10),
            card=card
        )
        
        self.section: str = section
        
        self.divider: pygame.Surface = resourceHandler.load_image('.\\assets\\backgrounds\\StatCardDivider.png')

        self.font_cap: pygame.Font = resourceHandler.load_font('assets\\fonts\\LibreBaskerville.ttf', 22)
        self.font: pygame.Font = resourceHandler.load_font('assets\\fonts\\LibreBaskerville.ttf', 18)
        
        self.__draw_text_face()
        
    def draw(self, screen: pygame.Surface) -> None:
        super().draw(screen)    
        self.rect = pygame.Rect((-self.size[0], -self.size[1]), self.size)
                
        self.image.blit(self.text_face, (0, 0))
        
        self.image.blit(self.divider, (2, 39))
        
        screen.blit(self.image, (self.pos[0] + self.offset[0], self.pos[1] + self.offset[1]))
        
    def hover(self) -> None:
        pass

    def no_hover(self) -> None:
        pass

    def on_click(self) -> None:
        pass
    
    def __draw_text_face(self) -> None:
        self._render_small_case(self.section, (0, 0))
    