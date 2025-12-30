import pygame

from editor.cardComponents.cardComponent import CardComponent

from singletons import resourceHandler
from singletons.eventBus import event_bus


WIDTH: int = 526
HEIGHT: int = 171
HEIGHT_TOKEN: int = 101

class TopStatComponent(CardComponent):
    def __init__(self, card: object, is_token: bool = False) -> None:
        super().__init__(
            name='TopStatComponent',
            size=(WIDTH, HEIGHT_TOKEN if is_token else HEIGHT),
            pos=(25, 25),
            card=card
        )
        
        self.is_token: bool = is_token
        
        self.font: pygame.Font = resourceHandler.load_font('.\\assets\\fonts\\NotoSans-Bold.ttf', 16)
        self.font_cap: pygame.Font = resourceHandler.load_font('.\\assets\\fonts\\NotoSans-Bold.ttf', 18)

        self.large_font: pygame.Font = resourceHandler.load_font('.\\assets\\fonts\\NotoSans-Bold.ttf', 18)
        self.large_font_cap: pygame.Font = resourceHandler.load_font('.\\assets\\fonts\\NotoSans-Bold.ttf', 20)
        
        self.background: pygame.Surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.__draw_background()
        
        self.text_face: pygame.Surface = pygame.Surface(self.size, pygame.SRCALPHA)
        
        self.top_line: pygame.Surface = resourceHandler.load_image('.\\assets\\backgrounds\\StatsTopLine.png')
        self.seperator: pygame.Surface = resourceHandler.load_image('.\\assets\\backgrounds\\StatsSeperator.png')
        
        self.miedinger: pygame.Font = resourceHandler.load_font('.\\assets\\fonts\\miedinger_medium.ttf', 18)
        self.miedinger_medium: pygame.Font = resourceHandler.load_font('.\\assets\\fonts\\miedinger_medium.ttf', 20)
        
        self.creature_size: str = 'Medium (1x1)'
        self.species: str = 'Character Species'
        self.vigilance: str = '10'

        self.defense: str = '10'
        self.magic_defense: str = '10'
        self.max_HP: str = '0'
        self.speed: str = '0'

        self.str: str = '0'
        self.dex: str = '0'
        self.vit: str = '0'
        self.int: str = '0'
        self.mnd: str = '0'
        
        self.__draw_text_face()
        
    def draw(self, screen: pygame.Surface) -> None:
        super().draw(screen)
        self.image.fill((0, 0, 0, 0))
        
        self.image.blit(self.background)
        self.image.blit(self.top_line)
        
        self.image.blit(self.text_face)
        
        self.image.blit(self.seperator, (12, 102))
        
        screen.blit(self.image, (self.pos[0] + self.offset[0], self.pos[1] + self.offset[1]))
        
        if self.hovering:
            con_mask: pygame.Mask = pygame.mask.Mask((1, 1), fill=True)
            mask: pygame.Mask = pygame.mask.from_surface(self.image)
            out: pygame.Surface = mask.convolve(con_mask).to_surface(setcolor=(221, 221, 221, 20), unsetcolor=(0,0,0,0))
            
            screen.blit(out, (self.pos[0] + self.offset[0], self.pos[1] + self.offset[1]))
        
        
    def on_click(self) -> None:
        if not self.hovering:
            return
        
        from editor.ui.topStatElement import TopStatElement
        event_bus.sign('ui_window', TopStatElement(self))
        
    def load(self, data: dict[str]) -> None:
        self.creature_size = data['creatureSize']
        self.species = data['species']
        self.vigilance = data['vigilance']

        self.defense = data['defense']
        self.magic_defense = data['magicDefense']

        self.max_HP = data['maxHP']
        self.speed = data['speed']

        self.str = data['str']
        self.dex = data['dex']
        self.vit = data['vit']
        self.int = data['int']
        self.mnd = data['mnd']
        
        self.__draw_text_face()
        
    def refresh(self) -> None:
        self.__draw_text_face()
        
    def __render_large_number(self, text, x: int, y: int) -> None:
        characters: list[str] = list(text)
        
        x: int = x
        y_offset: int = 0
        for char in characters:
            if char.isnumeric():
                render: pygame.Surface = self.miedinger.render(char, True, '#ffffff')
                y_offset = 2
                
            elif char.isupper():
                render: pygame.Surface = self.font_cap.render(char, True, '#ffffff')
                y_offset = 0
                
            elif char.startswith(('(', ')')):
                render: pygame.Surface = self.font.render(char, True, '#ffffff')
                y_offset = 2
                
            elif char.startswith('-'):
                render: pygame.Surface = self.font.render(char, True, '#ffffff')
                y_offset = 0
                
            else:
                render: pygame.Surface = self.font.render(char, True, '#ffffff')
                y_offset = 2
                
            self.text_face.blit(render, (x, y + y_offset))
            x += render.get_width()
        
    def __draw_background(self) -> None:
        background: pygame.Surface = resourceHandler.load_image('.\\assets\\backgrounds\\StatsBackground.png')
        
        middle: pygame.Surface = pygame.Surface((530, 45), pygame.SRCALPHA)
        middle.blit(background)
        middle = pygame.transform.scale(middle, (530, self.size[1] - 60))
        
        bottom: pygame.Surface = pygame.Surface((530, 45), pygame.SRCALPHA)
        bottom.blit(background, (0, -45))
        
        self.background.blit(middle, (3, 18))
        self.background.blit(bottom, (3, self.size[1] - bottom.height))
        
    def __draw_text_face(self) -> None:
        self.text_face.fill((0,0,0,0))
        
        self.__render_large_number(
            f'Size: {self.creature_size} - {self.species}',
            15,
            4
        )
        self.__render_large_number(
            f'Vigilance: {self.vigilance}',
            516 - (self.font_cap.size('Vigilance: ')[0] + self.miedinger.size(self.vigilance)[0]),
            4
        )
        
        self.__render_large_number(
            f'Defense: {self.defense}', 
            15, 
            40
        )
        self.__render_large_number(
            f'Max HP: {self.max_HP}', 
            15, 
            70
        )
        
        self.__render_large_number(
            f'Magic Defense: {self.magic_defense}', 
            263, 
            40
        )
        self.__render_large_number(
            f'Speed: {self.speed}', 
            263, 
            70
        )
        
        stats: dict[str, dict[str, int]] = {
            'STR': {
                'stat': int(self.str),
                'x': 25
            },
            'DEX': {
                'stat': int(self.dex),
                'x': 135
            },
            'VIT': {
                'stat': int(self.vit),
                'x': 244
            },
            'INT': {
                'stat': int(self.int),
                'x': 335
            },
            'MND': {
                'stat': int(self.mnd),
                'x': 427
            }
        }
        
        for stat, data in stats.items():
            render: pygame.Surface = self.miedinger_medium.render(stat, True, '#ffffff')
            self.text_face.blit(render, (data['x'], 112))
            
            sign: str = '+' if data['stat'] > 0 else ''
            sign_render: pygame.Surface = self.miedinger_medium.render(f'{sign}{data['stat']}', True, '#ffffff')
            self.text_face.blit(
                sign_render,
                (
                    data['x'] + render.width / 2 - sign_render.width / 2,
                    137
                ) 
            )
        
        