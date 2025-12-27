from enum import Enum

import pygame


class ScreenOptions(Enum):
    FULLSCREEN: int = 0
    WINDOWED: int = 1
    WINDOWED_FULLSCREEN: int = 2

class Display():
    def __init__(self, width: int, height: int) -> None:
        self.__width: int = width
        self.__height: int = height
        self.__fullscreen: ScreenOptions = ScreenOptions.WINDOWED
        self.__framerate: int = 0
        self.__vsync: bool = False
        
        self.screen: pygame.Surface = None
        
    def get_resolution(self) -> tuple[int, int]:
        return (self.__width, self.__height)
    
    def set_resolution(self, width: int, height: int) -> None:
        self.__width: int = width
        self.__height: int = height
        
    def get_fullscreen_pygame(self) -> int:
        match self.__fullscreen:
            case ScreenOptions.FULLSCREEN:
                self.set_resolution(0, 0)
                return pygame.FULLSCREEN
            
            case ScreenOptions.WINDOWED:
                return pygame.RESIZABLE
            
            case ScreenOptions.WINDOWED_FULLSCREEN:
                self.set_resolution(0, 0)
                return pygame.NOFRAME
    
    def get_fullscreen(self) -> ScreenOptions:
        return self.__fullscreen
    
    def set_fullscreen(self, fullscreen: ScreenOptions) -> None:
        if isinstance(fullscreen, int):
            fullscreen = ScreenOptions(fullscreen)
            
        self.__fullscreen = fullscreen
        
    def get_framerate(self) -> int:
        return self.__framerate
    
    def set_framerate(self, framerate: int) -> None:
        self.__framerate = framerate
        
    def get_vsync(self) -> bool:
        return self.__vsync
    
    def set_vsync(self, vsync: bool) -> None:
        self.__vsync = vsync
        
    def create_screen(self) -> None:
        flags = self.get_fullscreen_pygame()
        res = self.get_resolution()
        self.screen = pygame.display.set_mode(res, flags=flags, vsync=self.get_vsync())
        
    def draw(self) -> None:
        pygame.display.flip()