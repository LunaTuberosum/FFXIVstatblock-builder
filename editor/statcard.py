import pygame

from editor.cardComponents.cardComponent import CardComponent
from editor.cardComponents.nameComponent import NameComponent
from editor.cardComponents.sectionNameComponent import SectionNameComponent
from editor.cardComponents.topStatComponent import TopStatComponent
from editor.cardComponents.traitComponent import TraitComponent

from singletons import resourceHandler

from singletons.eventBus import event_bus


BACKGROUND_TILE_SIZE: int = 194
BACKGROUND_TILE_SIZE_X2: int = 388

class StatCard():
    def __init__(self, width: int, height: int) -> None:
        
        self.width: int = width * 3
        self.height: int = height
        self.actual_height: int = max(self.height, 2)
        
        self.size: tuple[int, int] = (self.width * BACKGROUND_TILE_SIZE, self.actual_height * BACKGROUND_TILE_SIZE)
        if width > 1:
            self.size = (self.size[0] - 48, self.size[1])
            
        self.limit: int = self.size[1] - 30
        
        self.background: pygame.Surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.__draw_background()
        
        self.components: dict[str, CardComponent] = {}
        
        self.image: pygame.Surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.rect: pygame.Rect = self.image.get_rect(topleft=(0, 40))
        
        self.dragged_file: CardComponent = None
        
        event_bus.register('swap_traits', self.swap_traits)
        
    def deregister(self) -> None:
        event_bus.deregister('swap_traits', self.swap_traits)
        
        for component in self.components.values():
            component.deregister()
        
    def swap_traits(self, trait: TraitComponent) -> None:
        if not self.dragged_file:
            return
        
        swap_to: TraitComponent = None
        all_traits: list[TraitComponent] = []
        for component in self.components.values():
            if not isinstance(component, TraitComponent):
                continue
            
            all_traits.append(component)
            if component.hovering and component != trait:
                swap_to = component
                
        mouse = pygame.mouse.get_pos()
        if not swap_to and mouse[1] < all_traits[0].rect.y:
            swap_to = all_traits[0]
            
        elif not swap_to and mouse[0] > all_traits[-1].rect.x and mouse[1] > all_traits[-1].rect.y:
            swap_to = all_traits[-1]
            
        if not swap_to:
            return
        
        swapper_name: str = trait.name
        swapper_format = trait.formating
        swapper_desc: str = trait.desc
        
        trait.name = swap_to.name
        trait.formating = swap_to.formating
        trait.desc = swap_to.desc
        
        swap_to.name = swapper_name
        swap_to.formating = swapper_format
        swap_to.desc = swapper_desc
        
        trait.refresh()
        swap_to.refresh()
        
    def update(self, pan: tuple[int, int], x: int) -> None:
        self.rect.topleft = (x + pan[0], 40 + pan[1])
        
        offset: tuple[int, int] = (20, 20)
        list(self.components.values())[-1].is_last = True
        for componet in self.components.values():
            if offset[1] + componet.rect.height >= self.limit:
                offset = (offset[0] + 540, 20)
                
            if self.limit - offset[1] < 130:
                componet.is_last = True
                
            componet.update(offset)
                
            offset = (offset[0], offset[1] + componet.rect.height)
        
    def draw(self, screen: pygame.Surface) -> None:
        self.image.fill((0, 0, 0, 0))
        
        self.image.blit(self.background)
        
        self.dragged_file = None
        for componet in self.components.values():
            if componet.drag:
                self.dragged_file = componet
                continue
            
            componet.draw(self.image)
            
        if self.dragged_file:
            self.dragged_file.draw(self.image)
            
        screen.blit(self.image, self.rect.topleft)
        
    def add_component(self, component_name: str, component: CardComponent) -> CardComponent:
        self.components[component_name] = component
        return component

    def get_component(self, component_name: str) -> CardComponent:
        return self.components[component_name]
        
    def load(self, component_data: dict[str, dict]) -> None:
        self.add_component(
            'Name_Component',
            NameComponent(self)
        )
        self.get_component('Name_Component').load(component_data['Name_Component'])
        
        self.add_component(
            'Top_Stat_Component',
            TopStatComponent(self, component_data['Top_Stat_Component']['token'])
        )
        self.get_component('Top_Stat_Component').load(component_data['Top_Stat_Component'])
        
        for name, data in component_data.items():

            if name == 'Traits_Title':
                self.add_component(
                    'Traits_Title',
                    SectionNameComponent(
                        self,
                        data['section']
                    )
                )
                
            elif name == 'Abilities_Title':
                self.add_component(
                    'Abilities_Title',
                    SectionNameComponent(
                        self,
                        data['section']
                    )
                )
                
            elif name.startswith('Trait'):
                self.add_component(
                    name,
                    TraitComponent(self)
                ).load(component_data[name])
               
    def __draw_background(self) -> None:
        _background: dict[str, pygame.Surface] = StatCard.__split_background()

        x: int = 0
        y: int = 0
        section: str = 'Top'

        for height in range(self.actual_height):
            if height == self.actual_height - 1:
                section = 'Bottom'

            elif height != 0:
                section = ''

            for _w in range(self.width):
                if _w == 0:
                    self.background.blit(_background[f'{section}Left'], (x, y))

                elif _w == self.width - 1:
                    self.background.blit(_background[f'{section}Right'], (x, y))

                else:
                    if _w == 4: x -= 48
                    self.background.blit(_background[f'{section}Middle'], (x, y))

                x += 194

            x = 0
            y += 194
        
    def __split_background() -> dict[str, pygame.Surface]:
        _img = resourceHandler.load_image('.\\assets\\backgrounds\\StatCardBackground.png')

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