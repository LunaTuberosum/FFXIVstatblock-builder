import pygame

from editor.cardComponents.markerComponnet import MarkerComponent

from editor.ui.paintbursh import Paint, get_tileset

from singletons import resourceHandler

from singletons.keyBus import key_bus

from uiComponents.componet import Component


class Marker(Component):
    def __init__(self, pos: tuple[int, int], marker_component: MarkerComponent, parent):
        super().__init__(
            pos,
            (400, 400)
        )
        
        self.marker_component: MarkerComponent = marker_component
        
        from editor.ui.markerElement import MarkerElement
        self.parent: MarkerElement = parent
        
        self.marker_area: list[list[int]] = []
        for row in self.marker_component.marker_area:
            
            new_row = []
            for col in row:
                new_row.append(Paint(col))
                
            self.marker_area.append(new_row)
            
        self.marker_overlays: dict[str, list[tuple[int, int]] | tuple[int, int]] = {}
        for m_type, overlays in self.marker_component.marker_overlays.items():
            if isinstance(overlays, list):
                self.marker_overlays[m_type] = overlays.copy()
                continue
            
            self.marker_overlays[m_type] = overlays
        
        self.grid_size: tuple[int, int] = self.marker_component.grid_size
        
        self.marker_tileset: dict[int, pygame.Surface] = get_tileset('.\\assets\\markerIcons\\SquareMarkerTileset.png')
        self.origin_tileset: dict[int, pygame.Surface] = get_tileset('.\\assets\\markerIcons\\SquareOriginTileset.png')
        self.instant_tileset: dict[int, pygame.Surface] = get_tileset('.\\assets\\markerIcons\\SquareInstantTileset.png')
        self.stack_tileset: dict[int, pygame.Surface] = get_tileset('.\\assets\\markerIcons\\SquareStackTileset.png')
        
        self.stack_icon: pygame.Surface = resourceHandler.load_image('.\\assets\\markerIcons\\StackMarker.png')
        self.line_stack_icon: pygame.Surface = resourceHandler.load_image('.\\assets\\markerIcons\\LineStackMarker.png')
        self.multi_stack_icon: pygame.Surface = resourceHandler.load_image('.\\assets\\markerIcons\\MultiStackMarker.png')
        
        self.stake_icon: pygame.Surface = resourceHandler.load_image('.\\assets\\markerIcons\\StakeMarker.png')
        
        self.proximity_icon: pygame.Surface = resourceHandler.load_image('.\\assets\\markerIcons\\ProximityMarker.png')
        
        self.icons: dict[int, pygame.Surface] = {
            Paint.GRID: resourceHandler.load_image('.\\assets\\markerIcons\\SquareGrid.png'),
            Paint.STAKE: resourceHandler.load_image('.\\assets\\markerIcons\\SquareOriginOutline.png'),
            Paint.TANK: resourceHandler.load_image('.\\assets\\markerIcons\\TankMarker.png'),
            Paint.DPS: resourceHandler.load_image('.\\assets\\markerIcons\\DPSMarker.png'),
            Paint.HEALER: resourceHandler.load_image('.\\assets\\markerIcons\\HealerMarker.png'),
        }
        
        self.face: pygame.Surface = pygame.Surface((self.grid_size[0] * 25, self.grid_size[1] * 25), pygame.SRCALPHA)
        self.__render_tiles()
        
        self.hover_icon: pygame.Surface = pygame.transform.scale(
            resourceHandler.load_image('.\\assets\\markerIcons\\HoverIcon.png'), 
            (400 / self.grid_size[0], 400 / self.grid_size[1]))
        
        self.hover_pos: tuple[int, int] = None
        self.painting: bool = False
        
        key_bus.register('mouse_left_down', self.on_click)
        key_bus.register('mouse_left_up', self.on_release)
        
    def deregister(self) -> None:
        super().deregister()
        
        key_bus.deregister('mouse_left_down', self.on_click)
        key_bus.deregister('mouse_left_up', self.on_release)
        
    def draw(self, screen: pygame.Surface, parent_pos: tuple[int, int]) -> None:
        super().draw(screen, parent_pos)
        
        if self.painting:
            self.on_click()
        
        self.image.blit(self.face)
        
        if self.hover_pos:
            self.image.blit(self.hover_icon, (
                self.hover_pos[0] * (400 / self.grid_size[0]),
                self.hover_pos[1] * (400 / self.grid_size[1])
            ))
        
        screen.blit(self.image, self.rect.topleft)
        
    def hover(self) -> None:
        super().hover()
        
        mouse: tuple[int, int] = pygame.mouse.get_pos()
        
        relative: tuple[int, int] = (mouse[0] - self.rect.x, mouse[1] - self.rect.y)
        
        scale: tuple[int, int] = (
            25 / ( (self.grid_size[0] * 25) / 400),
            25 / ( (self.grid_size[1] * 25) / 400)
        )
        
        self.hover_pos = (
            int(relative[0] // scale[0]),
            int(relative[1] // scale[1])
        )
        
    def no_hover(self) -> None:
        super().no_hover()
        
        if self.hovering:
            return
        
        self.hover_pos = None
            
    def __add_overlay(self, overlay_list: list[tuple[int, int]], paint: Paint) -> bool:
        if self.parent.brush.paint == paint:
            for pos in overlay_list:
                if pos == (self.hover_pos[1], self.hover_pos[0]):
                    return True
            
            overlay_list.append((self.hover_pos[1], self.hover_pos[0]))
            self.__render_tiles()
            return True
        
        else:
            for pos in overlay_list:
                if pos == (self.hover_pos[1], self.hover_pos[0]):
                    overlay_list.remove(pos)
                    break
                
        return False
            
    def on_click(self) -> None:
        if not self.hovering:
            return
        
        if self.__add_overlay(self.marker_overlays['STAKE'], Paint.STAKE):
            return
                
        if self.__add_overlay(self.marker_overlays['STACK'], Paint.STACK):
            return
        
        if self.__add_overlay(self.marker_overlays['STACK_LINE'], Paint.STACK_LINE):
            return
        
        if self.__add_overlay(self.marker_overlays['STACK_MULTI'], Paint.STACK_MULTI):
            return
        
        if self.parent.brush.paint == Paint.PROXIMITY:
            self.marker_overlays['PROXIMITY'] = (self.hover_pos[1], self.hover_pos[0])
            self.__render_tiles()
            return
        
        elif (self.hover_pos[1], self.hover_pos[0]) == self.marker_overlays['PROXIMITY']:
            self.marker_overlays['PROXIMITY'] = None
            self.__render_tiles()
            return
            
            
        self.painting = True
        
        self.marker_area[self.hover_pos[1]][self.hover_pos[0]] = self.parent.brush.paint
        self.__render_tiles()
        
    def on_release(self) -> None:
        self.painting = False
        
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
        
        for y in range(self.grid_size[0]):
            for x in range(self.grid_size[1]):
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
                     
                elif tile == Paint.DPS or tile == Paint.TANK or tile == Paint.HEALER:
                    self.face.blit(self.icons[Paint.GRID], (x * 25, y * 25))
                    
                    self.__role_underfil(x, y, self.marker_tileset, Paint.MARKER)
                    self.__role_underfil(x, y, self.stack_tileset, Paint.STACK_MARKER)
                    self.__role_underfil(x, y, self.origin_tileset, Paint.ORIGIN)
                    self.__role_underfil(x, y, self.instant_tileset, Paint.INSTANT)
                    
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
            
        if pos := self.marker_overlays['PROXIMITY']:
            height: int = min(self.grid_size[1] - pos[0], 10)
        
            scaled: pygame.Surface = pygame.transform.scale(self.proximity_icon, (25, height * 25))
            self.face.blit(scaled, (pos[1] * 25, pos[0] * 25))
            
        self.face = pygame.transform.scale(self.face, (400, 400))
        