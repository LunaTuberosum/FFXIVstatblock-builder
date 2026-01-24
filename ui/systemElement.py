from enum import Enum
from screeninfo import get_monitors

import pygame

from singletons import resourceHandler

from src.display import Display, ScreenOptions

from singletons.eventBus import event_bus
from singletons.dataBus import data_bus

from uiComponents.bar import Bar
from uiComponents.button import Button

from ui.uiElement import UIElement
from uiComponents.componet import Component
from uiComponents.dropdown import Dropdown
from uiComponents.switchButton import SwitchButton
from uiComponents.verticalToggleButton import VerticalToggleButtons


ELEMENT_SIZE: tuple[int, int] = (700, 360)
W_HALF: int = 350
H_HALF: int = 180

TEXT_DECREASE: int = 10

class Tab(Enum):
    DISPLAY: int = 0
    SOUND: int = 1

class SystemElement(UIElement):
    def __init__(self) -> None:
        screen = pygame.display.get_surface()
        
        super().__init__(
            name='System',
            title='System',
            size=ELEMENT_SIZE,
            pos=(
                (screen.size[0] / 2) - W_HALF,
                (screen.size[1] / 2) - H_HALF,
            )
        )
        
        self.button_hover: pygame.Surface= resourceHandler.load_image('.\\assets\\icons\\SystemHover.png')
        
        self.tab: Tab = Tab.DISPLAY
        
        self.need_restart: bool = False
        
        self.last_volumes: dict[str, float] = {
            'master': data_bus.sign('get_display').get_volume()
        }
        
        self.text_face: pygame.Surface = pygame.Surface(ELEMENT_SIZE, pygame.SRCALPHA)
        self.__render_text()
                
        self.add_component(
            'Display',
            Button(
                pos=(22, 55),
                size=(46, 46),
                image='.\\assets\\icons\\DisplayButton.png',
                image_hover='.\\assets\\icons\\DisplayButton_hover.png',
                command=self.display
            )
        )
        
        self.add_component(
            'Sound',
            Button(
                pos=(22, 105),
                size=(46, 46),
                image='.\\assets\\icons\\SoundButton.png',
                image_hover='.\\assets\\icons\\SoundButton_hover.png',
                command=self.sound
            )
        )
        
        self.add_component(
            'Close',
            Button(
                pos=(475, 300),
                size=(198, 38),
                image='.\\assets\\icons\\button.png',
                image_hover='.\\assets\\icons\\button_hover.png',
                command=self.close,
                text='Close'
            )
        )
        
        self.add_component(
            'Apply',
            Button(
                pos=(267, 300),
                size=(198, 38),
                image='.\\assets\\icons\\button.png',
                image_hover='.\\assets\\icons\\button_hover.png',
                command=self.apply,
                text='Apply'
            )
        )
        
        self.display(clear=False)
        
    def draw(self, screen: pygame.Surface) -> None:
        super().draw(screen)
        
        if self.pos[0] != (screen.size[0] / 2) - W_HALF \
        or self.pos[1] != (screen.size[1] / 2) - H_HALF:
                    
            self.pos = (
                (screen.size[0] / 2) - W_HALF,
                (screen.size[1] / 2) - H_HALF
            )
        
        fps_text: str = f'{data_bus.sign('get_fps')} fps'
        self.render_text(
            fps_text, 
            '#EEE1C5', 
            (
                self.size[0] - 45 - self.font.size(fps_text)[0],
                20
            )
        )
        
        if self.need_restart:
            self.render_text('Restart Needed', "#863434", (130, 305))
        
        self.image.blit(self.text_face)
        
        screen.blit(self.image, self.pos)
        
        for comp in self.components.values():
            comp.draw(screen, self.pos)
            
        if self.tab == Tab.DISPLAY:
            screen.blit(self.button_hover, self.get_component('Display').rect.topleft)
        elif self.tab == Tab.SOUND:
            screen.blit(self.button_hover, self.get_component('Sound').rect.topleft)
            
    def apply_display(self, display: Display, setting_save: dict) -> dict:
        changed: bool = False
        
        monitors = get_monitors()
        monitors.reverse()
        new_monitor: int = -1
        for index, mon in enumerate(monitors):
            if mon.name == self.get_component('Monitor_Dropdown').selected_option:
                new_monitor = index
                break
            
        if display.get_monitor() != new_monitor + 1:
            setting_save['monitor'] = new_monitor + 1
            changed = True
            
        selected_option: str = self.get_component('Screen_Toggle').button_selected.text
        new_option: ScreenOptions = None
        
        if selected_option == 'Windowed':
            new_option = ScreenOptions.WINDOWED
            
        elif selected_option == 'Windowed Borderless':
            new_option = ScreenOptions.WINDOWED_FULLSCREEN
            
        elif selected_option == 'Fullscreen':
            new_option = ScreenOptions.FULLSCREEN
            
        if display.get_fullscreen() != new_option:
            setting_save['displayOption'] = new_option.value
            changed = True
            
        res: list[str] = self.get_component('Resolution_Dropdown').selected_option.split('x')
        new_res: tuple[int, int] = (int(res[0]), int(res[1]))
        
        if display.get_resolution() != new_res:
            setting_save['windowSize'] = new_res
            changed = True
            
        if changed:
            self.need_restart = True
            
        return setting_save
    
    def apply_sound(self, display: Display, setting_save: dict) -> dict:
        
        
        return setting_save
            
    def apply(self) -> None:
        display: Display = data_bus.sign('get_display')
        
        setting_save = {
            'monitor': display.get_monitor(),
                
            'windowSize': display.get_resolution(),
            'displayOption': display.get_fullscreen().value,
            'framerate': display.get_framerate(),
            'vsync': display.get_vsync(),
            
            'volume': display.get_volume()
        }
        
        if self.tab == Tab.DISPLAY:
            setting_save = self.apply_display(display, setting_save)
        elif self.tab == Tab.SOUND:
            setting_save = self.apply_sound(display, setting_save)

        resourceHandler.save_pickle('.//settings.pkl', setting_save)
            
    def render_text_face(self, text: str, color: str, pos: tuple[int, int]) -> None:
        self.text_face.blit(self.font.render(text, True, '#000000'), (pos[0], pos[1] + 1))
        self.text_face.blit(self.font.render(text, True, color), (pos[0], pos[1]))
            
    def __render_text(self) -> None:
        self.text_face.fill((0, 0, 0, 0))
        
        pygame.draw.rect(self.text_face, '#D4B155', (75, 48, 1, 295))
        pygame.draw.rect(self.text_face, '#525552', (76, 48, 1, 295))
        
        if self.tab == Tab.DISPLAY:
            self.render_text_face('Display Settings', '#C2C2C2', (90, 55))
            self.render_text_face('Main Display', '#EEE1C5', (115, 80))
            
            self.render_text_face('Screen Mode', '#C2C2C2', (90, 115))
            
            self.render_text_face('Resolution', '#C2C2C2', (90, 225))
            self.render_text_face('Preset', '#EEE1C5', (115, 250))
            
        elif self.tab == Tab.SOUND:
            self.render_text_face('Volume Settings', '#C2C2C2', (90, 55))
        
            self.render_text_face('Master Volume', '#C2C2C2', (378, 78))
            
        self.text_face.blit(
            pygame.transform.scale(self.seperator, (600, 3)),
            (78, 290)
        )
        
    def clear_tab_comp(self) -> None:
        remove: list[str] = []
        index: int = 0
        for key, comp in self.components.items():
            if index < 5:
                index += 1
                continue
            
            index += 1
            comp.deregister()
            remove.append(key)
            
        for comp in remove:
            self.components.pop(comp)
        
    def display(self, clear: bool = True) -> None:
        if clear: self.clear_tab_comp()

        self.tab = Tab.DISPLAY
        self.__render_text()
        
        monitors = get_monitors()
        monitors.reverse()
        
        options: dict[str, object] = {}
        for mon in monitors:
            options[mon.name] = self.switch_monitor
        
        self.add_component(
            'Monitor_Dropdown',
            Dropdown(
                pos=(313, 77),
                options=options,
                default=monitors[data_bus.sign('get_monitor') - 1].name
            )
        )
        
        fs: ScreenOptions = data_bus.sign('get_fullscreen')
        defualt: str = ''
        
        if fs == ScreenOptions.FULLSCREEN:
            defualt = 'Fullscreen'
        elif fs == ScreenOptions.WINDOWED_FULLSCREEN:
            defualt = 'Windowed Borderless'
        elif fs == ScreenOptions.WINDOWED:
            defualt = 'Windowed'
        
        self.add_component(
            'Screen_Toggle',
            VerticalToggleButtons(
                pos=(115, 140),
                size=(230, 150),
                options={
                    'Windowed': self.switch_fullscreen,
                    'Windowed Borderless': self.switch_fullscreen,
                    'Fullscreen': self.switch_fullscreen
                },
                default=defualt
            ))
        
        res = data_bus.sign('get_resolution')
        if res == (0, 0):
            info = pygame.display.Info()
            res = (info.current_w, info.current_h)
        
        self.add_component(
            'Resolution_Dropdown',
            Dropdown(
                pos=(313, 247),
                options={
                    "1920x1080": self.switch_resolution,
                    "1440x810": self.switch_resolution,
                    "960x540": self.switch_resolution,
                    "540x960": self.switch_resolution,
                },
                default=f'{res[0]}x{res[1]}'
            )
        )
        
    def switch_monitor(self) -> None:
        pass
    
    def switch_resolution(self) -> None:
        pass
        
    def switch_fullscreen(self, selection: str) -> None:
        self.get_component('Screen_Toggle').set_option(selection)
        
    def sound(self) -> None:
        self.clear_tab_comp()
        
        display: Display = data_bus.sign('get_display')
        
        self.add_component(
            'Master_Bar',
            Bar(
                pos=(115, 90),
                command=self.change_master
            )
        )
        
        if self.last_volumes['master'] > display.get_volume()  * 100:
            self.get_component('Master_Bar').percentage = self.last_volumes['master'] * 100
        else:
            self.get_component('Master_Bar').percentage = display.get_volume()  * 100 
        
        self.add_component(
            'Mute_Switch',
            SwitchButton(
                pos=(353, 83),
                face='.\\assets\\icons\\MuteButton.png',
                face_hover='.\\assets\\icons\\MuteButton_hover.png',
                face_switch='.\\assets\\icons\\MuteButton_Switch.png',
                face_switch_hover='.\\assets\\icons\\MuteButton_Switch_hover.png',
                command=self.mute
            )
        )
        
        if display.get_volume() == 0:
            self.get_component('Mute_Switch').active = True

        self.tab = Tab.SOUND
        self.__render_text()
        
    def change_master(self) -> None:
        bar: Bar = self.get_component('Master_Bar')
        
        event_bus.sign('set_master', bar.percentage / 100)
        self.last_volumes['master'] = bar.percentage / 100
        
    def mute(self) -> None:
        switch: SwitchButton = self.get_component('Mute_Switch')
        
        if switch.active:
            event_bus.sign('mute_master')
        else:
            event_bus.sign('set_master', self.last_volumes['master'])