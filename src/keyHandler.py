import pygame

from singletons.keyBus import key_bus
from singletons.eventBus import event_bus

from uiComponents.textBox import TextBox


class KeyHandler():
    def __init__(self) -> None:
        self.textbox: TextBox = None
        
        event_bus.register('typing_register', self.typing_register)
    
    def typing_register(self, textbox: TextBox) -> None:
        self.textbox = textbox
    
    def handle_keys(self) -> None:
        self.__key_down()
        self.__key_up()
        
    def __key_down(self) -> None:
        keys = pygame.key.get_just_pressed()
        
        if self.textbox:
            return
    
        if keys[pygame.K_ESCAPE]:
            key_bus.sign('esc_down')
    
    def __key_up(self) -> None:
        keys = pygame.key.get_just_released()