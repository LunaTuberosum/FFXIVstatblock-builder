import pygame

from menu.menuObject import MenuObject
from menu.sheet import Sheet
from singletons import resourceHandler
from singletons.keyBus import key_bus
from singletons.eventBus import event_bus

from menu.folder import Folder

from src.gameProcess import GameProcess
from ui.confirmElement import ConfirmElement


pygame.font.init()
JUPITER_FONT: pygame.font.Font = resourceHandler.load_font('.\\assets\\fonts\\jupiter_pro_regular.otf', 40)
MIEDINGER: pygame.font.Font = resourceHandler.load_font('assets/fonts/miedinger_medium.ttf', 18)

SAVE_X_START: int = 15
SAVE_Y_START: int = 70
SAVE_INCREASE: int = 260
class Menu(GameProcess):
    def __init__(self, main: object) -> None:
        super().__init__(main)
        
        self.current_folder: Folder = Folder('', '')
        self.prev_folder: list[Folder] = []
        
        self.dragged_file: MenuObject = None
        
    def setup_bus_calls(self) -> None:
        super().setup_bus_calls()
        
        event_bus.register('change_folder', self.change_folder)
        event_bus.register('move_file', self.move_file)
        event_bus.register('delete_file', self.delete_file)
        
        key_bus.register('mouse_right_down', self.menu_context_menu)
        
    def deregister(self) -> None:
        super().deregister()
        
        event_bus.deregister('change_folder', self.change_folder)
        event_bus.deregister('move_file', self.move_file)
        event_bus.deregister('delete_file', self.delete_file)
        
        key_bus.deregister('mouse_right_down', self.menu_context_menu)
        
    def menu_context_menu(self) -> None:
        event_bus.sign('context_menu', {
            'Add Sheet': self.current_folder.create_sheet,
            'Add Folder': self.current_folder.create_folder
        })
        
    def change_folder(self, new_folder: Folder) -> None:
        new_folder.no_hover()
        
        if self.prev_folder:
            if new_folder.name == self.prev_folder[-1].name:
                self.prev_folder.pop()
                new_folder.is_prev = False
                self.current_folder = new_folder
                return
        
        self.current_folder.is_prev = True
        self.prev_folder.append(self.current_folder)
        self.current_folder = new_folder
    
    def __update_folder_path(self, folder: Folder) -> None:
        for m_file in folder.files:
            m_file.path = f'{folder.path}\\{folder.name}'
            
            if isinstance(m_file, Folder):
                self.__update_folder_path(m_file)
            
    
    def __move_folder(self, m_file: Folder, folder: Folder) -> None:
        resourceHandler.move_dir(
            f'.\\saves{m_file.path}\\{m_file.name}', 
            f'.\\saves{folder.path}\\{folder.name}\\{m_file.name}'
        )
        
        m_file.path = f'\\{folder.path}\\{folder.name}'
        self.current_folder.files.remove(m_file)
        folder.files.append(m_file)
        folder.sort()
        
        self.__update_folder_path(m_file)            
    
    def __move_sheet(self, m_file: Sheet, folder: Folder) -> None:
        resourceHandler.rename_json(
            f'.\\saves{m_file.path}\\{m_file.name}.json', 
            f'.\\saves{folder.path}\\{folder.name}\\{m_file.name}.json'
        )
        
        m_file.path = f'\\{folder.path}\\{folder.name}'
        self.current_folder.files.remove(m_file)
        folder.files.append(m_file)
        folder.sort()
            
    def move_file(self, m_file: MenuObject) -> None:
        if isinstance(m_file, Folder) and m_file.is_prev:
            return
        
        if self.prev_folder and m_file.rect.colliderect(self.prev_folder[-1].rect):
            prev_folder: Folder = self.prev_folder[-1]
            
            if isinstance(m_file, Folder):
                self.__move_folder(m_file, prev_folder)
            else:
                self.__move_sheet(m_file, prev_folder)
            
        for file_m in self.current_folder.files:
            if not isinstance(file_m, Folder) or file_m.name == m_file.name:
                continue
            
            if not file_m.rect.colliderect(m_file.rect):
                continue
                
            if isinstance(m_file, Folder):
                self.__move_folder(m_file, file_m)
            else:
                self.__move_sheet(m_file, file_m)
                
            break
        
        m_file.no_hover()
        m_file.drag = False
        
    def __delete_dir(self, folder: Folder) -> None:
        for m_file in folder.files:
            if isinstance(m_file, Folder):
                if m_file.files:
                    self.__delete_dir(m_file)
                
                m_file.deregister()
                resourceHandler.del_dir(f'.\\saves\\{m_file.path}\\{m_file.name}')
                
            else:
                
                m_file.deregister()
                resourceHandler.del_json(f'.\\saves\\{m_file.path}\\{m_file.name}.json')
            
        folder.files = []
        
    def delete_file(self, m_file: MenuObject) -> None:
        def folder_confirm():
            if m_file.files:
                self.__delete_dir(m_file)
                
            m_file.deregister()
                
            resourceHandler.del_dir(f'.\\saves\\{m_file.path}\\{m_file.name}')
            self.current_folder.files.remove(m_file)
                
            event_bus.sign('ui_window', None)
        
        def confirm():
            if isinstance(m_file, Folder):
                if not m_file.files:
                    folder_confirm()
                    return
                
                event_bus.sign('ui_window', ConfirmElement(
                    text='This folder contains other files.\nAre you sure you want to delete it?',
                    confrim_command=folder_confirm
                ))
                return
            
            resourceHandler.del_json(f'.\\saves\\{m_file.path}\\{m_file.name}.json')
            
            m_file.deregister()
            self.current_folder.files.remove(m_file)
            
            event_bus.sign('ui_window', None)
        
        event_bus.sign('context_menu', {})
        event_bus.sign('ui_window', ConfirmElement(
            text=f'Are you sure you want to delete this {m_file.__class__.__name__}?',
            confrim_command=confirm
        ))
        
    def update(self) -> None:
        super().update()
    
        if self.prev_folder:
            prev_folder = self.prev_folder[-1]
            
            prev_folder.no_hover()
            if prev_folder.rect.collidepoint(self.mouse_handler.mouse_pos) and not self.hover_object:
                self.hover_object = prev_folder
                
        for m_file in self.current_folder.files:
            m_file.no_hover()                
            
            if m_file.rect.collidepoint(self.mouse_handler.mouse_pos):
                if m_file.drag: 
                    m_file.hover()
                    continue
                
                if self.hover_object:
                    continue
                
                self.hover_object = m_file

        if self.hover_object:
            self.hover_object.hover()
    
        self.draw()
        
    def draw(self) -> None:
        screen: pygame.Surface = self.main.get_screen()
        
        screen.fill('#313031')

        screen.blit(JUPITER_FONT.render('FFXIV TTRPG Stat Card Builder', True, '#000000'), (10, 22))
        screen.blit(JUPITER_FONT.render('FFXIV TTRPG Stat Card Builder', True, '#CCCCCC'), (10, 20))
        
        x: int = SAVE_X_START
        y: int = SAVE_Y_START
        
        if self.prev_folder:
            prev_folder = self.prev_folder[-1]
            
            prev_folder.draw(screen, x, y)
            x += SAVE_INCREASE
        
        self.dragged_file = None
        pos: tuple[int, int] = ()
        for m_file in self.current_folder.files:
            if m_file.drag:
                self.dragged_file = m_file
                pos = (x, y)
                
            else:
                m_file.draw(screen, x, y)
            
            x += SAVE_INCREASE
            
            if x + SAVE_INCREASE >= screen.size[0]:
                x = SAVE_X_START
                y += SAVE_INCREASE
                
        if self.dragged_file:
            self.dragged_file.draw(screen, pos[0], pos[1])
                
        screen.blit(MIEDINGER.render(str(round(self.main.clock.get_fps(), 1)), True, '#00ff00'), (screen.size[0]- 100, 10))
        
        super().draw()