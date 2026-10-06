import pygame

from menu.menuObject import MenuObject

from menu.ui.descriptionElement import DescriptionElement

from singletons import resourceHandler

from singletons.eventBus import event_bus

from ui.confirmElement import ConfirmElement


ENTRY_INCREASE: int = 25
ENTRY_X_BOUND: int = 200

ENTRY_START_Y: int = 55
ENTRY_MAX_LINES: int = 6

Y_OFFSET: int = 25

SEPERATOR_SIZE: tuple[int, int] = (144, 3)
SEPERATOR_POS_1: tuple[int, int] = (53, 50)
SEPERATOR_POS_2: tuple[int, int] = (53, 197)

RECT_POS: tuple[int, int] = (19, 19)
RECT_SIZE: tuple[int, int] = (212, 212)

class Encounter(MenuObject):
    def __init__(self, path: str, encounter: str) -> None:
        super().__init__(
            name=encounter.replace('.json', ''), 
            path=path, 
            background='EncounterSaveBackground'
        )
        self.ENTRY_START_X: int = 55
        
        self.encounter_info: dict = resourceHandler.load_json(f'.\\saves\\{path}\\{encounter}')
        
    def deregister(self):
        super().deregister()
        
    def on_click(self) -> None:
        if not self.hovering:
            return
        super().on_click()
        event_bus.sign('ui_window', None)
        
        if self.click_timer.time_left() > 0:
            self.no_hover()
            self.click_timer.reset()
            self.drag = False
            event_bus.sign('load_encounter', self)
        else:
            self.click_timer.start()
            
            if not self.drag:
                mouse: tuple[int, int] = pygame.mouse.get_pos()
                self.drag_pos = (mouse[0] - self.rect.x, mouse[1] - self.rect.y)
                
            self.drag = True
        
    def draw(self, screen: pygame.Surface, x: int, y: int):
        if self.drag:
            mouse: tuple[int, int] = pygame.mouse.get_pos()
            x = mouse[0] - self.drag_pos[0] - RECT_POS[0]
            y = mouse[1] - self.drag_pos[1] - RECT_POS[1]
        
        super().draw(x, y, Y_OFFSET)
        self.rect = pygame.Rect((x + RECT_POS[0], y + RECT_POS[1]), RECT_SIZE)
        
        self.image.blit(pygame.transform.scale(self.seperator, SEPERATOR_SIZE), SEPERATOR_POS_1)
        self.image.blit(pygame.transform.scale(self.seperator, SEPERATOR_SIZE), SEPERATOR_POS_2)
        
        self.draw_entries(self.encounter_info['desc'], ENTRY_START_Y, ENTRY_MAX_LINES)

        if self.hovering:
            screen.blit(self.add_outline(self.image), (x - 2, y - 2))
        else:
            screen.blit(self.image, (x, y))
            
    def draw_entries(self, desc: str, entry_start_y: int, entry_max_lines: int) -> None:
        _y = entry_start_y
        line_count: int = 1
        
        if not desc:
            self.render_text('No description', '#EEE1C5' if not self.hovering else '#F7EDD9', (self.ENTRY_START_X, _y))
            return
        
        _x: int = self.ENTRY_START_X
        for word in desc.split():
            if _x + self.font.size(word)[0] > ENTRY_X_BOUND:
                line_count += 1
                
                _x = ENTRY_START_Y
                _y += ENTRY_INCREASE
                
                if line_count == entry_max_lines:
                    _y -= 5
                    self.render_text('...', '#EEE1C5' if not self.hovering else '#F7EDD9', (_x, _y))
                    return

            self.render_text(word, '#EEE1C5' if not self.hovering else '#F7EDD9', (_x, _y))
            _x += self.font.size(word + ' ')[0]
        
        _y += ENTRY_INCREASE
        line_count += 1
        
    def context_menu(self) -> None:
        if not self.hovering: 
            return
        
        event_bus.sign('context_menu', {
            '': None,
            'Change Name': self.change_name,
            'Change Description': self.change_description,
            'Duplicate': self.duplicate,
            'Delete': self.delete
        }, True)
            
    def duplicate(self) -> None:
        def confirm():
            event_bus.sign('duplicate_encounter', self)
            event_bus.sign('ui_window', None)
        
        event_bus.sign('ui_window', 
            ConfirmElement(
                'Are you sure you want to make a copy of this \nencounter?',
                confirm,
                confirm_text='Duplicate'
            )
        )
        
    def rename(self, text: str) -> None:
        if not text:
            text = 'New Encounter Name'
            
        if not resourceHandler.rename_json(f'.\\saves\\{self.path}\\{self.name}.json', f'.\\saves\\{self.path}\\{text}.json'):
            return
        
        self.name = text
        
    def change_description(self) -> None:
        event_bus.sign('context_menu', {})
        event_bus.sign('ui_window', DescriptionElement(self))
    
    def redesc(self, text: str) -> None:        
        self.encounter_info['desc'] = text
        
        resourceHandler.save_json(f'.\\saves\\{self.path}\\{self.name}.json', self.encounter_info)