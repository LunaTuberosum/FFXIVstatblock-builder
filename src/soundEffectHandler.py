import pygame

class SoundeEffectHandler():
    def __init__(self) -> None:
        self.volume: float = 1
        
        self.close_window: pygame.Sound = pygame.Sound('.\\assets\\se\\FFXIV_Close_Window.mp3')
        self.close_window.set_volume(.01)
        
        self.open_window: pygame.Sound = pygame.Sound('.\\assets\\se\\FFXIV_Open_Window.mp3')
        self.open_window.set_volume(.01)
        
        self.confirm: pygame.Sound = pygame.Sound('.\\assets\\se\\FFXIV_Confirm.mp3')
        self.confirm.set_volume(.01)
        
        self.cancel: pygame.Sound = pygame.Sound('.\\assets\\se\\FFXIV_Cancel.mp3')
        self.cancel.set_volume(.01)
        
        self.hover: pygame.Sound = pygame.Sound('.\\assets\\se\\FFXIV_Hover.wav')
        self.hover.set_volume(.03)
        
    def set_volume(self, volume: float) -> None:
        self.volume = volume
        
        self.close_window.set_volume(self.close_window.get_volume() * self.volume)
        self.open_window.set_volume(self.open_window.get_volume() * self.volume)
        self.confirm.set_volume(self.confirm.get_volume() * self.volume)
        self.cancel.set_volume(self.cancel.get_volume() * self.volume)
        self.hover.set_volume(self.hover.get_volume() * self.volume)
        
    def play_se(self, sound_name: str) -> None:
        match (sound_name):
            case 'close_window':
                self.close_window.play()
                
            case 'open_window':
                self.open_window.play()
                
            case 'confirm':
                self.confirm.play()
                
            case 'cancel':
                self.cancel.play()
                
            case 'hover':
                self.hover.play()