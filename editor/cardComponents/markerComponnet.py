import pygame

from editor.ui.paintbursh import get_tileset
from singletons import resourceHandler
from uiComponents.componet import Component


GRID: int = 0
MARKER: int = 1
ORIGIN: int = 2

class MarkerComponent(Component):
    def __init__(self, width: int, height: int, component) -> None:
        from editor.cardComponents.abilityComponent import AbilityComponent
        self.component: AbilityComponent = component
        
        super().__init__(
            pos=(self.component.size[0] - ((25 * width) + 12), 22),
            size=(25 * width, 25 * height)
        )
        
        self.face: pygame.Surface = pygame.Surface(self.size, pygame.SRCALPHA)
        
        self.grid_size: tuple[int, int] = (width, height)
        
        self.marker_area: list[list[int]] = []
        for y in range(height):
            row = []
            for x in range(width):
                row.append(0)
                
            self.marker_area.append(row)
            
        self.marker_overlays: dict[str, list[tuple[int, int]] | tuple[int, int]] = {
            'STAKE': [],
            'STACK': [],
            'STACK_LINE': [],
            'STACK_MULTI': [],
            'PROXIMITY': None
        }
            
        self.__render_tiles()
        
    def add_marker_area(self, marker_area: list[list[int]]) -> None:
        self.marker_area = marker_area
        self.__render_tiles()
        
    def draw(self, screen: pygame.Surface, parent_pos: tuple[int, int]) -> None:
        super().draw(screen, parent_pos)
        
        rect_image = pygame.Surface(self.face.size, pygame.SRCALPHA)
        pygame.draw.rect(rect_image, (255, 255, 255), (0, 0, *self.face.size), border_radius=8)
        self.face.blit(rect_image, (0, 0), None, pygame.BLEND_RGBA_MIN)
        pygame.draw.rect(self.face, '#5C5856', (0, 0, *self.face.size), width=2, border_radius=8)
        
        self.image.blit(self.face, (0, 0))
        screen.blit(self.image, self.rect.topleft)
        
    def __render_tile(self, x: int, y: int, tileset, tile: int) -> None:
        top: bool = False
        bottom: bool = False
        left: bool = False
        right: bool = False
        top_left: bool = False
        top_right: bool = False
        bottom_left: bool = False
        bottom_right: bool = False
        
        if x != 0:
            left = self.marker_area[y][x - 1] == tile
            
        if  y != 0:
            top = self.marker_area[y - 1][x] == tile
            
        if x != self.grid_size[0] - 1:
            right = self.marker_area[y][x + 1] == tile
            
        if y != self.grid_size[1] - 1:
            bottom = self.marker_area[y + 1][x] == tile
            
        if x != 0 and y != 0:
            top_left = self.marker_area[y - 1][x - 1] == tile
            
        if x != self.grid_size[0] - 1 and y != 0:
            top_right = self.marker_area[y - 1][x + 1] == tile
            
        if x != 0 and y != self.grid_size[1] - 1:
            bottom_left = self.marker_area[y + 1][x - 1] == tile
            
        if x != self.grid_size[0] - 1 and y != self.grid_size[1] - 1:
            bottom_right = self.marker_area[y + 1][x + 1] == tile
            
        if not (top and left): top_left = False
        if not (top and right): top_right = False
        if not (bottom and left): bottom_left = False
        if not (bottom and right): bottom_right = False
        
        total = 0b00000000
        if top:             total += (1 << 0)
        if top_right:       total += (1 << 1)
        if right:           total += (1 << 2)
        if bottom_right:    total += (1 << 3)
        if bottom:          total += (1 << 4)
        if bottom_left:     total += (1 << 5)
        if left:            total += (1 << 6)
        if top_left:        total += (1 << 7)
        
        surface = tileset.get(total, None)
        if not surface:
            return
        
        self.face.blit(surface, (x * 25, y * 25))
        
    def __render_tiles(self) -> None:
        self.face.fill((0, 0, 0, 0))
        
        marker_tileset: dict[int, pygame.Surface] = get_tileset('.\\assets\\markerIcons\\SquareMarkerTileset.png')
        origin_tileset: dict[int, pygame.Surface] = get_tileset('.\\assets\\markerIcons\\SquareOriginTileset.png')
        grid_image: pygame.Surface = resourceHandler.load_image('.\\assets\\markerIcons\\SquareGrid.png')
        
        for y in range(self.grid_size[0]):
            for x in range(self.grid_size[1]):
                tile: int = self.marker_area[y][x]
                if tile == GRID:
                    self.face.blit(grid_image, (x * 25, y * 25))
                    continue
                
                elif tile == ORIGIN:
                    self.__render_tile(x, y, origin_tileset, ORIGIN)
                    continue                    
                
                self.__render_tile(x, y, marker_tileset, MARKER)
                
                
                    
                
                    
                
                