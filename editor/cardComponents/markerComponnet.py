import pygame

from editor.ui.paintbursh import Paint, get_tileset
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
        
        self.marker_area: list[list[Paint]] = []
        for y in range(height):
            row = []
            for x in range(width):
                row.append(Paint.GRID)
                
            self.marker_area.append(row)
            
        self.marker_overlays: dict[str, list[tuple[int, int]] | tuple[int, int]] = {
            'STAKE': [],
            
            'STACK': [],
            'STACK_LINE': [],
            'STACK_MULTI': [],
            
            'TANKBUSTER': [],
            'TANKBUSTER_AOE': [],
            'TANKBUSTER_CAUTION': [],
            
            'PROXIMITY': None
        }
        
        self.marker_tileset: dict[int, pygame.Surface] = get_tileset('.\\assets\\markerIcons\\SquareMarkerTileset.png')
        self.origin_tileset: dict[int, pygame.Surface] = get_tileset('.\\assets\\markerIcons\\SquareOriginTileset.png')
        self.instant_tileset: dict[int, pygame.Surface] = get_tileset('.\\assets\\markerIcons\\SquareInstantTileset.png')
        self.stack_tileset: dict[int, pygame.Surface] = get_tileset('.\\assets\\markerIcons\\SquareStackTileset.png')
        self.tankbuster_tileset: dict[int, pygame.Surface] = get_tileset('.\\assets\\markerIcons\\SquareTankbusterTileset.png')
        
        self.stack_icon: pygame.Surface = resourceHandler.load_image('.\\assets\\markerIcons\\StackMarker.png')
        self.line_stack_icon: pygame.Surface = resourceHandler.load_image('.\\assets\\markerIcons\\LineStackMarker.png')
        self.multi_stack_icon: pygame.Surface = resourceHandler.load_image('.\\assets\\markerIcons\\MultiStackMarker.png')
        
        self.tankbuster_icon: pygame.Surface = resourceHandler.load_image('.\\assets\\markerIcons\\TankBusterMarker.png')
        self.aoe_tankbuster_icon: pygame.Surface = resourceHandler.load_image('.\\assets\\markerIcons\\AOETankBusterMarker.png')
        self.caution_tankbuster_icon: pygame.Surface = resourceHandler.load_image('.\\assets\\markerIcons\\CautionTankBusterMarker.png')
        
        self.stake_icon: pygame.Surface = resourceHandler.load_image('.\\assets\\markerIcons\\StakeMarker.png')
        
        self.proximity_icon: pygame.Surface = resourceHandler.load_image('.\\assets\\markerIcons\\ProximityMarker.png')
        
        self.icons: dict[int, pygame.Surface] = {
            Paint.GRID: resourceHandler.load_image('.\\assets\\markerIcons\\SquareGrid.png'),
            Paint.STAKE: resourceHandler.load_image('.\\assets\\markerIcons\\SquareOriginOutline.png'),
            Paint.TANK: resourceHandler.load_image('.\\assets\\markerIcons\\TankMarker.png'),
            Paint.DPS: resourceHandler.load_image('.\\assets\\markerIcons\\DPSMarker.png'),
            Paint.HEALER: resourceHandler.load_image('.\\assets\\markerIcons\\HealerMarker.png'),
        }
            
        self.__render_tiles()
        
    def refresh(self) -> None:
        self.size = (self.grid_size[0] * 25, self.grid_size[1] * 25)
        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        self.pos = (self.component.size[0] - (min(25 * self.grid_size[0], 250) + 12), 22)
        
        self.__render_tiles()
        
    def add_marker_area(self, marker_area: list[list[int]], marker_overlays: dict[str, list]) -> None:
        self.marker_area: list[list[int]] = []
        for row in marker_area:
            
            new_row = []
            for col in row:
                new_row.append(Paint(col))
                
            self.marker_area.append(new_row)
        
        for overlay_type, overlay_list in marker_overlays.items():
            if not overlay_list:
                continue
            
            if not isinstance(overlay_list, list):
                self.marker_overlays[overlay_type] = (overlay_list[0], overlay_list[1])
                continue
            
            new_list: list[tuple[int, int]] = []
            for overlay in overlay_list:
                new_list.append((overlay[0], overlay[1]))
                
            self.marker_overlays[overlay_type] = new_list
            
        print(self.marker_overlays)
        
        self.__render_tiles()
        
    def draw(self, screen: pygame.Surface, parent_pos: tuple[int, int]) -> None:
        super().draw(screen, parent_pos)
        
        rect_image = pygame.Surface(self.face.size, pygame.SRCALPHA)
        pygame.draw.rect(rect_image, (255, 255, 255), (0, 0, *self.face.size), border_radius=8)
        self.face.blit(rect_image, (0, 0), None, pygame.BLEND_RGBA_MIN)
        pygame.draw.rect(self.face, '#5C5856', (0, 0, *self.face.size), width=2, border_radius=8)
        
        self.image.blit(self.face, (0, 0))
        screen.blit(self.image, self.rect.topleft)
        
    def save(self) -> dict:
        marker_list: list[list[int]] = []
        
        for col in self.marker_area:
            col_list: list[int] = []
            for row in col:
                col_list.append(row.value)
                
            marker_list.append(col_list)
            
        return {
            'grid_size': self.grid_size,
            'marker_overlay': self.marker_overlays,
            'marker_area': marker_list
        }
        
    def __render_tile(self, x: int, y: int, tileset: dict[str, pygame.Surface], tile: int) -> None:
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
        
    def __role_underfil(self, x: int, y: int, tileset: dict[str, pygame.Surface], tile: int) -> None:
        top: bool = False
        bottom: bool = False
        left: bool = False
        right: bool =  False
        
        if y != 0 and self.marker_area[y - 1][x] == tile:
            top = True
        if y != len(self.marker_area) - 1 and self.marker_area[y + 1][x] == tile:
            bottom = True
        
        if x != 0 and self.marker_area[y][x - 1] == tile:
            left = True
        if x != len(self.marker_area[y]) - 1 and self.marker_area[y][x + 1] == tile:
            right = True
            
        is_under: bool = False
        if top and bottom:
            is_under = True
        elif left and right:
            is_under = True
        elif top and left: 
            is_under = True
        elif top and right: 
            is_under = True
        elif bottom and left:
            is_under = True
        elif bottom and right:
            is_under = True
        
        if not is_under:
            return
        
        self.__render_tile(x, y, tileset, tile)
        
    def __render_tiles(self) -> None:
        self.face = pygame.Surface((self.grid_size[0] * 25, self.grid_size[1] * 25), pygame.SRCALPHA)
        self.face.fill((0, 0, 0, 0))
        
        for y in range(self.grid_size[1]):
            for x in range(self.grid_size[0]):
                tile: int = self.marker_area[y][x]
                if tile == Paint.MARKER:
                    self.__render_tile(x, y, self.marker_tileset, Paint.MARKER)
                    continue
                
                elif tile == Paint.ORIGIN:
                    self.__render_tile(x, y, self.origin_tileset, Paint.ORIGIN)
                    continue          
                
                elif tile == Paint.INSTANT:
                    self.face.blit(self.icons.get(Paint.GRID), (x * 25, y * 25))
                    self.__render_tile(x, y, self.instant_tileset, Paint.INSTANT)
                    continue
                
                elif tile == Paint.STACK_MARKER:
                    self.__render_tile(x, y, self.stack_tileset, Paint.STACK_MARKER)
                    continue
                
                elif tile == Paint.TANKBUSTER_MARKER:
                    self.__render_tile(x, y, self.tankbuster_tileset, Paint.TANKBUSTER_MARKER)
                    continue
                     
                elif tile == Paint.DPS or tile == Paint.TANK or tile == Paint.HEALER:
                    self.face.blit(self.icons[Paint.GRID], (x * 25, y * 25))
                    
                    self.__role_underfil(x, y, self.marker_tileset, Paint.MARKER)
                    self.__role_underfil(x, y, self.stack_tileset, Paint.STACK_MARKER)
                    self.__role_underfil(x, y, self.origin_tileset, Paint.ORIGIN)
                    self.__role_underfil(x, y, self.instant_tileset, Paint.INSTANT)
                    self.__role_underfil(x, y, self.tankbuster_tileset, Paint.TANKBUSTER_MARKER)
                    
                icon: pygame.Surface = self.icons.get(tile, self.icons[Paint.GRID])
                self.face.blit(icon, (x * 25, y * 25))
                
        for pos in self.marker_overlays['STAKE']:
            self.face.blit(self.icons[Paint.STAKE], (pos[1] * 25, pos[0] * 25))
            
            self.face.blit(self.stake_icon, (pos[1] * 25, (pos[0] * 25) - 25))
            
            if self.marker_area[pos[0]][pos[1]] == Paint.DPS:
                self.face.blit(self.icons[Paint.DPS], (pos[1] * 25, pos[0] * 25))
            
            elif self.marker_area[pos[0]][pos[1]] == Paint.HEALER:
                self.face.blit(self.icons[Paint.HEALER], (pos[1] * 25, pos[0] * 25))
                
            elif self.marker_area[pos[0]][pos[1]] == Paint.TANK:
                self.face.blit(self.icons[Paint.TANK], (pos[1] * 25, pos[0] * 25))
            
        for pos in self.marker_overlays['STACK']:
            self.face.blit(self.stack_icon, ((pos[1] * 25) - 50, (pos[0] * 25) - 50))
            
        for pos in self.marker_overlays['STACK_LINE']:
            self.face.blit(self.line_stack_icon, ((pos[1] * 25) - 50, (pos[0] * 25) - 50))
            
        for pos in self.marker_overlays['STACK_MULTI']:
            self.face.blit(self.multi_stack_icon, ((pos[1] * 25) - 50, (pos[0] * 25) - 50))
            
        for pos in self.marker_overlays['TANKBUSTER']:
            self.face.blit(self.tankbuster_icon, ((pos[1] * 25) - 25, (pos[0] * 25) - 25))
            
        for pos in self.marker_overlays['TANKBUSTER_AOE']:
            self.face.blit(self.aoe_tankbuster_icon, ((pos[1] * 25) - 50, (pos[0] * 25) - 50))
            
        for pos in self.marker_overlays['TANKBUSTER_CAUTION']:
            self.face.blit(self.caution_tankbuster_icon, ((pos[1] * 25) - 25, (pos[0] * 25) - 25))
            
        if pos := self.marker_overlays['PROXIMITY']:
            height: int = min(self.grid_size[1] - pos[0], 10)
        
            scaled: pygame.Surface = pygame.transform.scale(self.proximity_icon, (25, height * 25))
            self.face.blit(scaled, (pos[1] * 25, pos[0] * 25))
            
        self.face = pygame.transform.scale(self.face, (
            min(self.size[0], 250),
            min(self.size[1], 250)
        ))
        
                
                
                    
                
                    
                
                