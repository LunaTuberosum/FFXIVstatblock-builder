from enum import Enum

import pygame

from singletons import resourceHandler
from uiComponents.button import Button
    

class MarkerOverlay():
    def __init__(self, pos: tuple[int, int], data: str = '') -> None:
        self.pos: tuple[int, int] = pos
        self.data: str = data

class Paint(Enum):
    GRID: int = 0
    
    MARKER: int = 1
    ORIGIN: int = 2
    
    STAKE: int = 3
    STAKE_BLUE: int = 4
    STAKE_PURPLE: int = 5
    STAKE_GREEN: int = 6
    
    INSTANT: int = 7
    PROXIMITY: int = 8
    
    STACK_MARKER: int = 9
    STACK: int = 10
    STACK_LINE: int = 11
    STACK_MULTI: int = 12
    
    TANKBUSTER_MARKER: int = 13
    TANKBUSTER: int = 14
    TANKBUSTER_AOE: int = 15
    TANKBUSTER_CAUTION: int = 16
    
    TOWER: int = 147# One day...
    TOWER_2: int = 18 # One day...
    TOWER_3: int = 19 # One day...
    TOWER_4: int = 20 # One day...
    
    DPS: int = 21
    HEALER: int = 22
    TANK: int = 23
    
class Paintbrush():
    def __init__(self) -> None:
        self.paint: Paint = Paint.GRID
        self.active_button: Button = None
        
def get_tileset(image: str) -> None:
    tileset: dict[int, pygame.Surface] = {}
    set_image: pygame.Surface = resourceHandler.load_image(image)
    
    def get_tile(pos: tuple[int, int]) -> pygame.Surface:
        square: pygame.Surface = pygame.Surface((25, 25), pygame.SRCALPHA)
        square.blit(set_image, pos)
        return square
    
    tileset[16] = get_tile((0, 0))
    tileset[17] = get_tile((0, -25))
    tileset[1] = get_tile((0, -50))
    tileset[0] = get_tile((0, -75))
    
    tileset[20] = get_tile((-25, 0))
    tileset[21] = get_tile((-25, -25))
    tileset[5] = get_tile((-25, -50))
    tileset[4] = get_tile((-25, -75))
    
    tileset[84] = get_tile((-50, 0))
    tileset[85] = get_tile((-50, -25))
    tileset[69] = get_tile((-50, -50))
    tileset[68] = get_tile((-50, -75))
    
    tileset[80] = get_tile((-75, 0))
    tileset[81] = get_tile((-75, -25))
    tileset[65] = get_tile((-75, -50))
    tileset[64] = get_tile((-75, -75))
    
    tileset[213] = get_tile((-100, 0))
    tileset[29] = get_tile((-100, -25))
    tileset[23] = get_tile((-100, -50))
    tileset[117] = get_tile((-100, -75))
    
    tileset[92] = get_tile((-125, 0))
    tileset[127] = get_tile((-125, -25))
    tileset[223] = get_tile((-125, -50))
    tileset[71] = get_tile((-125, -75))
    
    tileset[116] = get_tile((-150, 0))
    tileset[253] = get_tile((-150, -25))
    tileset[247] = get_tile((-150, -50))
    tileset[197] = get_tile((-150, -75))
    
    tileset[87] = get_tile((-175, 0))
    tileset[113] = get_tile((-175, -25))
    tileset[209] = get_tile((-175, -50))
    tileset[93] = get_tile((-175, -75))
    
    tileset[28] = get_tile((-200, 0))
    tileset[31] = get_tile((-200, -25))
    tileset[95] = get_tile((-200, -50))
    tileset[7] = get_tile((-200, -75))
    
    tileset[125] = get_tile((-225, 0))
    tileset[119] = get_tile((-225, -25))
    tileset[255] = get_tile((-225, -50))
    tileset[199] = get_tile((-225, -75))
    
    tileset[124] = get_tile((-250, 0))
    tileset[-1] = get_tile((-250, -25))
    tileset[221] = get_tile((-250, -50))
    tileset[215] = get_tile((-250, -75))
    
    tileset[112] = get_tile((-275, 0))
    tileset[245] = get_tile((-275, -25))
    tileset[241] = get_tile((-275, -50))
    tileset[193] = get_tile((-275, -75))
    
    return tileset