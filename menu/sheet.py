import pygame

from menu.menuObject import MenuObject

from singletons import resourceHandler

from singletons.eventBus import event_bus

from ui.confirmElement import ConfirmElement


ENTRY_START_Y: int = 60
ENTRY_MAX_LINES: int = 6

Y_OFFSET: int = 30

SEPERATOR_SIZE: tuple[int, int] = (185, 3)
SEPERATOR_POS: tuple[int, int] = (33, 55)

RECT_POS: tuple[int, int] = (19, 19)
RECT_SIZE: tuple[int, int] = (212, 212)

class Sheet(MenuObject):
    def __init__(self, path: str, sheet: str) -> None:
        super().__init__(
            sheet.replace('.json', ''), 
            path, 
            'StatSaveBackground'
        )
        
        self.sheet_info: dict = resourceHandler.load_json(f'.\\saves\\{path}\\{sheet}')
        
    def deregister(self):
        super().deregister()
        
    def on_click(self) -> None:
        if not self.hovering:
            return
        
        super().on_click()
        
        if self.click_timer.time_left() > 0:
            self.no_hover()
            self.click_timer.reset()
            self.drag = False
            event_bus.sign('load_sheet', self)
        else:
            self.click_timer.start()
            
            if not self.drag:
                mouse: tuple[int, int] = pygame.mouse.get_pos()
                self.drag_pos = (mouse[0] - self.rect.x, mouse[1] - self.rect.y)
                
            self.drag = True
        
    def get_entry(self, entry) -> str:
        return super().get_entry(entry['components']['Name_Component']['name'])
        
    def draw(self, screen: pygame.Surface, x: int, y: int):
        if self.drag:
            mouse: tuple[int, int] = pygame.mouse.get_pos()
            x = mouse[0] - self.drag_pos[0] - RECT_POS[0]
            y = mouse[1] - self.drag_pos[1] - RECT_POS[1]
        
        super().draw(x, y, Y_OFFSET)
        self.rect = pygame.Rect((x + RECT_POS[0], y + RECT_POS[1]), RECT_SIZE)
        
        self.image.blit(pygame.transform.scale(self.seperator, SEPERATOR_SIZE), SEPERATOR_POS)
        
        self.draw_entries(self.sheet_info.values(), ENTRY_START_Y, ENTRY_MAX_LINES)

        if self.hovering:
            screen.blit(self.add_outline(self.image), (x - 2, y - 2))
        else:
            screen.blit(self.image, (x, y))
            
    def context_menu(self) -> None:
        if not self.hovering: 
            return
        
        event_bus.sign('context_menu', {
            '': None,
            'Change Name': self.change_name,
            'Duplicate': self.duplicate,
            'Delete': self.delete
        }, True)
            
    def duplicate(self) -> None:
        def confirm():
            event_bus.sign('duplicate_sheet', self)
            event_bus.sign('ui_window', None)
        
        event_bus.sign('ui_window', 
            ConfirmElement(
                'Are you sure you want to make a copy of this sheet?',
                confirm,
                confirm_text='Duplicate'
            )
        )
            
    def rename(self, text: str) -> None:
        if not text:
            text = 'New Sheet Name'
            
        if not resourceHandler.rename_json(f'.\\saves\\{self.path}\\{self.name}.json', f'.\\saves\\{self.path}\\{text}.json'):
            return
        
        self.name = text
            