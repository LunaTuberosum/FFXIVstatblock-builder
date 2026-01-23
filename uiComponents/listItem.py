from typing import Callable
import pygame

from editor.cardComponents.abilityComponent import EffectData

from singletons import resourceHandler

from singletons.eventBus import event_bus
from singletons.keyBus import key_bus

from src.timer import Timer
from ui.confirmElement import ConfirmElement


BACKGROUND_TILE_SIZE: int = 10
BACKGROUND_TILE_SIZE_X2: int = 20

class ListItem():
    def __init__(self, size: tuple[int, int], effect_name: str, effect_data: EffectData, command: Callable[['ListItem'], None], parent) -> None:
        from uiComponents.list import List
        self.parent: List = parent
            
        self.size: tuple[int, int] = size
        self.effect_name: str = effect_name
        self.effect_data: EffectData = effect_data
        
        self.command: Callable[['ListItem'], None] = command
        
        self.background: pygame.Surface =pygame.Surface(self.size, pygame.SRCALPHA)
        self.__draw_background()
        
        self.image: pygame.Surface =pygame.Surface(self.size, pygame.SRCALPHA)
        self.rect: pygame.Rect = self.image.get_rect()
        
        self.font_bolded: pygame.Font = resourceHandler.load_font('.\\assets\\fonts\\noto-sans.regular.ttf', 15)
        self.font_bolded.bold = True
        
        self.cursor_timer: Timer = Timer(300)
        self.cursor_timer.start()
        self.cursor_pos: tuple = (self.size[0] - 30, 0)
        self.cursor_cycle: int = -1
        self.cursor: pygame.Surface = resourceHandler.load_image('.\\assets\\icons\\Cursor.png')
        
        self.drag: bool = False
        self.drag_pos: tuple[int, int] = ()
        
        self.text_face: pygame.Surface =pygame.Surface(self.size, pygame.SRCALPHA)
        self.__render_text_face()
        
        self.hovering: bool = False
        
        self.current: bool = False
        self.click_timer: Timer = Timer(300)
        
        self.active: bool = True
        
        key_bus.register('mouse_left_down', self.on_click)
        key_bus.register('mouse_left_up', self.on_release)
        
        key_bus.register('mouse_right_down', self.context_menu)
        
    def deregister(self) -> None:
        key_bus.deregister('mouse_left_down', self.on_click)
        key_bus.deregister('mouse_left_up', self.on_release)
        
        key_bus.deregister('mouse_right_down', self.context_menu)
        
    def draw(self, screen: pygame.Surface, pos: tuple[int, int]) -> None:
        x, y = pos
        if self.drag:
            mouse: tuple[int, int] = pygame.mouse.get_pos()
            x = min(max(mouse[0] - self.drag_pos[0], self.parent.rect.x + 5), self.parent.rect.x + 5)
            y = min(max(mouse[1] - self.drag_pos[1], self.parent.rect.y + 49), self.parent.rect.bottom - 37)
            
        self.image.fill((0, 0, 0, 0))
        self.rect.topleft = (x, y)
        self.image.blit(self.background)
        self.image.blit(self.text_face)
        
        if self.cursor_timer.is_done():
            self.cursor_pos = (self.cursor_pos[0] + (5 * self.cursor_cycle), 0)
            self.cursor_cycle *= -1
            self.cursor_timer.start()
        
        if self.current:
            self.image.blit(self.cursor, self.cursor_pos)
        elif self.hovering:
            self.image.blit(self.cursor, (self.size[0] - 30, 0))
        
        screen.blit(self.image, (x, y))
        
    def on_click(self) -> None:
        if not self.hovering:
            return
        event_bus.sign('play_se', 'confirm')
        
        if self.click_timer.time_left() > 0:
            self.command(self)
            self.click_timer.start()
            return
        
        self.click_timer.start()
        
        if not self.drag:
            mouse: tuple[int, int] = pygame.mouse.get_pos()
            self.drag_pos = (mouse[0] - self.rect.x, mouse[1] - self.rect.y)
            
        self.drag = True
        
    def on_release(self) -> None:
        if not self.drag:
            return
        
        self.drag = False
        
        event_bus.sign('swap_effects', self)
        
    def no_hover(self) -> None:
        if not self.hovering:
            return
        
        self.hovering = False
        
    def hover(self) -> None:
        self.hovering = True
        
    def is_hover(self, mouse_pos: tuple[int, int]) -> bool:
        return self.rect.collidepoint(mouse_pos)
    
    def context_menu(self) -> None:
        if not self.hovering:
            return
        
        event_bus.sign('context_menu', {
            'Edit': self.edit,
            'Delete': self.delete,
            'Duplicate': self.duplicate,
        })
        
    def edit(self) -> None:
        event_bus.sign('context_menu', None)
        self.parent.element.current_effect = (self.effect_name, self.effect_data)
        self.parent.element.update_effect()
            
    def delete(self) -> None:
        def delete():
            event_bus.sign('context_menu', None)
            self.parent.element.effects.pop(self.effect_name)
            self.parent.get_component('Effect_Text').change_text(str(int(self.parent.get_component('Effect_Text').text) - 1))
            
            self.parent.set_effects()
            
        def confirm():
            event_bus.sign('ui_window', None)
            delete()
            
        if not self.effect_name.startswith('Effect') or self.effect_data.desc != '':
            event_bus.sign('ui_window', ConfirmElement(
                text='This effect has been modified.\nDo you wish to delete it?',
                confrim_command=confirm
            ), True)
            return
        
        delete()
    
    def duplicate(self) -> None:
        event_bus.sign('context_menu', None)
        self.parent.element.effects[f'{self.effect_name} Copy'] = self.effect_data
        self.parent.get_component('Effect_Text').change_text(str(int(self.parent.get_component('Effect_Text').text) + 1))
        
        self.parent.set_effects()
        
    def refresh(self) -> None:
        self.__render_text_face()    
        
    def __render_text_face(self) -> None:
        self.text_face.fill((0, 0, 0, 0))
        
        name: str = ''
        
        width: int = 0
        for char in self.effect_name:
            name += char
            
            if self.font_bolded.size(name)[0] >= self.size[0] - 12:
                name = name[:-4]
                name += '...'
                break
        
        self.text_face.blit(self.font_bolded.render(name, True, '#995745'), (6, 3))
    
    def __draw_background(self) -> None:
        _background: dict[str, pygame.Surface] = ListItem.__split_background()

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
        _img = resourceHandler.load_image('.\\assets\\backgrounds\\ListItemBackground.png')

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
        _temp['TopRight'].blit(_img, (-BACKGROUND_TILE_SIZE_X2, 0))

        _temp['Left'] = pygame.surface.Surface((BACKGROUND_TILE_SIZE, BACKGROUND_TILE_SIZE), pygame.SRCALPHA)
        _temp['Left'].blit(_img, (0, -BACKGROUND_TILE_SIZE))
        _temp['Middle'] = pygame.surface.Surface((BACKGROUND_TILE_SIZE, BACKGROUND_TILE_SIZE), pygame.SRCALPHA)
        _temp['Middle'].blit(_img, (-BACKGROUND_TILE_SIZE, -BACKGROUND_TILE_SIZE))
        _temp['Right'] = pygame.surface.Surface((BACKGROUND_TILE_SIZE, BACKGROUND_TILE_SIZE), pygame.SRCALPHA)
        _temp['Right'].blit(_img, (-BACKGROUND_TILE_SIZE_X2, -BACKGROUND_TILE_SIZE))

        _temp['BottomLeft'] = pygame.surface.Surface((BACKGROUND_TILE_SIZE, BACKGROUND_TILE_SIZE), pygame.SRCALPHA)
        _temp['BottomLeft'].blit(_img, (0, -BACKGROUND_TILE_SIZE_X2))
        _temp['BottomMiddle'] = pygame.surface.Surface((BACKGROUND_TILE_SIZE, BACKGROUND_TILE_SIZE), pygame.SRCALPHA)
        _temp['BottomMiddle'].blit(_img, (-BACKGROUND_TILE_SIZE, -BACKGROUND_TILE_SIZE_X2))
        _temp['BottomRight'] = pygame.surface.Surface((BACKGROUND_TILE_SIZE, BACKGROUND_TILE_SIZE), pygame.SRCALPHA)
        _temp['BottomRight'].blit(_img, (-BACKGROUND_TILE_SIZE_X2, -BACKGROUND_TILE_SIZE_X2))

        return _temp