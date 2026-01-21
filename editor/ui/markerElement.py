import pygame

from editor.cardComponents.abilityComponent import AbilityComponent

from editor.ui.paintbursh import Paintbrush, Paint
from editor.ui.statCardElement import StatCardElement

from uiComponents.button import Button
from uiComponents.dropdown import Dropdown
from uiComponents.marker import Marker
from uiComponents.textBox import TextBox


ELEMENT_SIZE: tuple[int, int] = (870, 560)
W_HALF: int = 435
H_HALF: int = 280

class MarkerElement(StatCardElement[AbilityComponent]):
    def __init__(self, component) -> None:
        screen = pygame.display.get_surface()
        
        super().__init__(
            name='Marker',
            title='Marker',
            size=ELEMENT_SIZE,
            pos=(
                (screen.size[0] / 2) - W_HALF,
                (screen.size[1] / 2) - H_HALF,
            ),
            component=component
        )
        
        self.paletes_buttons: list[Button] = []
        self.brush: Paintbrush = Paintbrush()
        
        apply = self.get_component('Apply')
        apply.pos = (self.size[0] - 436, apply.pos[1])
        
        self.add_component(
            'Width_Text',
            TextBox(
                pos=(220, 80),
                size=(60, 1)
            )
        ).change_text(str(self.component.marker.grid_size[0]))
        
        self.add_component(
            'Width_Plus',
            Button(
                pos=(280, 80),
                size=(32, 34),
                image='.\\assets\\icons\\AddButton.png',
                image_hover='.\\assets\\icons\\AddButton_hover.png',
                command=None
            )
        )
        self.add_component(
            'Width_Minus',
            Button(
                pos=(310, 80),
                size=(32, 34),
                image='.\\assets\\icons\\MinusButton.png',
                image_hover='.\\assets\\icons\\MinusButton_hover.png',
                command=None
            )
        )
        
        self.add_component(
            'Height_Text',
            TextBox(
                pos=(220, 120),
                size=(60, 1)
            )
        ).change_text(str(self.component.marker.grid_size[0]))
        
        self.add_component(
            'Height_Plus',
            Button(
                pos=(280, 120),
                size=(32, 34),
                image='.\\assets\\icons\\AddButton.png',
                image_hover='.\\assets\\icons\\AddButton_hover.png',
                command=None
            )
        )
        self.add_component(
            'Height_Minus',
            Button(
                pos=(310, 120),
                size=(32, 34),
                image='.\\assets\\icons\\MinusButton.png',
                image_hover='.\\assets\\icons\\MinusButton_hover.png',
                command=None
            )
        )
        
        self.add_component(
            'Marker',
            Marker(
                pos=(410, 80),
                marker_component=self.component.marker,
                parent=self
            )
        )
        
        self.add_component(
            'Palete_Drowdown',
            Dropdown(
                pos=(120, 180),
                options={
                    'Normal': self.palete_normal,
                    'Stack': self.palete_stack,
                    'Tankbuster': self.palete_tankbuster
                },
                default='Please Select a Palete...',
                size='Small'
            )
        )
        
        self.add_component(
            'Remove',
            Button(
                pos=(30, self.size[1] - 65),
                size=(198, 38),
                image='.\\assets\\icons\\button.png',
                image_hover='.\\assets\\icons\\button_hover.png',
                command=None,
                text='Remove  Marker'
            )
        )
        
    def draw(self, screen: pygame.Surface) -> None:
        super().draw(screen)
        
        if self.pos[0] != (screen.size[0] / 2) - W_HALF \
        or self.pos[1] != (screen.size[1] / 2) - H_HALF:
                    
            self.pos = (
                (screen.size[0] / 2) - W_HALF,
                (screen.size[1] / 2) - H_HALF
            )
            
        self.image.blit(self.text_face)
            
        screen.blit(self.image, self.pos)
    
        for button in self.paletes_buttons:
            button.active = False
            if button == self.brush.active_button:
                button.active = True
            
            button.no_hover()
            
            if button.rect.collidepoint(pygame.mouse.get_pos()):
                button.hover()
                
            button.draw(screen, self.pos)    
    
        for comp in self.components.values():
            comp.draw(screen, self.pos)
        
            
    def __dergister_palete(self) -> None:
        for button in self.paletes_buttons:
            button.deregister()
            
    def __add_class_buttons(self) -> None:
        last_pos: tuple[int, int] = self.paletes_buttons[-1].pos
        
        def tank():
            self.brush.paint = Paint.TANK
            self.brush.active_button = self.paletes_buttons[-3]
        self.paletes_buttons.append(
            Button(
                pos=(last_pos[0] + 32, 230),
                size=(32, 34),
                image='.\\assets\\icons\\TankButton.png',
                image_hover='.\\assets\\icons\\TankButton_hover.png',
                command=tank
            )
        )
        
        def dps():
            self.brush.paint = Paint.DPS
            self.brush.active_button = self.paletes_buttons[-2]
        self.paletes_buttons.append(
            Button(
                pos=(last_pos[0] + 64, 230),
                size=(32, 34),
                image='.\\assets\\icons\\DPSButton.png',
                image_hover='.\\assets\\icons\\DPSButton_hover.png',
                command=dps
            )
        )
        
        def healer():
            self.brush.paint = Paint.HEALER
            self.brush.active_button = self.paletes_buttons[-1]
        self.paletes_buttons.append(
            Button(
                pos=(last_pos[0] + 96, 230),
                size=(32, 34),
                image='.\\assets\\icons\\HealerButton.png',
                image_hover='.\\assets\\icons\\HealerButton_hover.png',
                command=healer
            )
        )
            
    def palete_normal(self) -> None:
        self.__dergister_palete()
        
        def grid():
            self.brush.paint = Paint.GRID
            self.brush.active_button = self.paletes_buttons[0]
        def marker():
            self.brush.paint = Paint.MARKER
            self.brush.active_button = self.paletes_buttons[1]
        def origin():
            self.brush.paint = Paint.ORIGIN
            self.brush.active_button = self.paletes_buttons[2]
        def stake():
            self.brush.paint = Paint.STAKE
            self.brush.active_button = self.paletes_buttons[3]
        def instant():
            self.brush.paint = Paint.INSTANT
            self.brush.active_button = self.paletes_buttons[4]
        def proximity():
            self.brush.paint = Paint.PROXIMITY
            self.brush.active_button = self.paletes_buttons[5]  
        
        self.paletes_buttons = [
            Button(
                pos=(50, 230),
                size=(32, 34),
                image='.\\assets\\icons\\GridButton.png',
                image_hover='.\\assets\\icons\\GridButton_hover.png',
                command=grid
            ),
            Button(
                pos=(82, 230),
                size=(32, 34),
                image='.\\assets\\icons\\MarkerButton.png',
                image_hover='.\\assets\\icons\\MarkerButton_hover.png',
                command=marker
            ),
            Button(
                pos=(114, 230),
                size=(32, 34),
                image='.\\assets\\icons\\OriginButton.png',
                image_hover='.\\assets\\icons\\OriginButton_hover.png',
                command=origin
            ),
            Button(
                pos=(146, 230),
                size=(32, 34),
                image='.\\assets\\icons\\OriginOutlineStakeButton.png',
                image_hover='.\\assets\\icons\\OriginOutlineStakeButton_hover.png',
                command=stake
            ),
            Button(
                pos=(178, 230),
                size=(32, 34),
                image='.\\assets\\icons\\InstantButton.png',
                image_hover='.\\assets\\icons\\InstantButton_hover.png',
                command=instant
            ),
            Button(
                pos=(210, 230),
                size=(32, 34),
                image='.\\assets\\icons\\ProximityButton.png',
                image_hover='.\\assets\\icons\\ProximityButton_hover.png',
                command=proximity
            )
        ]
        grid()
        
        self.__add_class_buttons()
        
    def palete_stack(self) -> None:
        self.__dergister_palete()
        
        def grid():
            self.brush.paint = Paint.GRID
            self.brush.active_button = self.paletes_buttons[0]
        def stack_marker():
            self.brush.paint = Paint.STACK_MARKER
            self.brush.active_button = self.paletes_buttons[1]
        def stack_origin():
            self.brush.paint = Paint.STACK
            self.brush.active_button = self.paletes_buttons[2]
        def stack_origin_line():
            self.brush.paint = Paint.STACK_LINE
            self.brush.active_button = self.paletes_buttons[3]
        def stack_origin_multi():
            self.brush.paint = Paint.STACK_MULTI
            self.brush.active_button = self.paletes_buttons[4]
            
        
        self.paletes_buttons = [
            Button(
                pos=(50, 230),
                size=(32, 34),
                image='.\\assets\\icons\\GridButton.png',
                image_hover='.\\assets\\icons\\GridButton_hover.png',
                command=grid
            ),
            Button(
                pos=(82, 230),
                size=(32, 34),
                image='.\\assets\\icons\\StackButton.png',
                image_hover='.\\assets\\icons\\StackButton_hover.png',
                command=stack_marker
            ),
            Button(
                pos=(114, 230),
                size=(32, 34),
                image='.\\assets\\icons\\StackOriginButton.png',
                image_hover='.\\assets\\icons\\StackOriginButton_hover.png',
                command=stack_origin
            ),
            Button(
                pos=(146, 230),
                size=(32, 34),
                image='.\\assets\\icons\\LineStackOriginButton.png',
                image_hover='.\\assets\\icons\\LineStackOriginButton_hover.png',
                command=stack_origin_line
            ),
            Button(
                pos=(178, 230),
                size=(32, 34),
                image='.\\assets\\icons\\MultiStackOriginButton.png',
                image_hover='.\\assets\\icons\\MultiStackOriginButton_hover.png',
                command=stack_origin_multi
            )
        ]
        grid()
        
        self.__add_class_buttons()
            
    def palete_tankbuster(self) -> None:
        self.__dergister_palete()
        
        def grid():
            self.brush.paint = Paint.GRID
            self.brush.active_button = self.paletes_buttons[0]
        def tankbuster_marker():
            self.brush.paint = Paint.TANKBUSTER_MARKER
            self.brush.active_button = self.paletes_buttons[1]
        def tankbuster():
            self.brush.paint = Paint.TANKBUSTER
            self.brush.active_button = self.paletes_buttons[2]
        def aoe_tankbuster():
            self.brush.paint = Paint.TANKBUSTER_AOE
            self.brush.active_button = self.paletes_buttons[3]
        def caution_tankbuster():
            self.brush.paint = Paint.TANKBUSTER_CAUTION
            self.brush.active_button = self.paletes_buttons[4]
        
        self.paletes_buttons = [
            Button(
                pos=(50, 230),
                size=(32, 34),
                image='.\\assets\\icons\\GridButton.png',
                image_hover='.\\assets\\icons\\GridButton_hover.png',
                command=grid
            ),
            Button(
                pos=(82, 230),
                size=(32, 34),
                image='.\\assets\\icons\\TankbusterButton.png',
                image_hover='.\\assets\\icons\\TankbusterButton_hover.png',
                command=tankbuster_marker
            ),
            Button(
                pos=(114, 230),
                size=(32, 34),
                image='.\\assets\\icons\\TankBusterOriginButton.png',
                image_hover='.\\assets\\icons\\TankBusterOriginButton_hover.png',
                command=tankbuster
            ),
            Button(
                pos=(146, 230),
                size=(32, 34),
                image='.\\assets\\icons\\AOETankBusterOriginButton.png',
                image_hover='.\\assets\\icons\\AOETankBusterOriginButton_hover.png',
                command=aoe_tankbuster
            ),
            Button(
                pos=(178, 230),
                size=(32, 34),
                image='.\\assets\\icons\\CautionTankBusterOriginButton.png',
                image_hover='.\\assets\\icons\\CautionTankBusterOriginButton_hover.png',
                command=caution_tankbuster
            )
        ]
        grid()
        
        self.__add_class_buttons()
            
    def _render_text_face(self):
        super()._render_text_face()
        
        self.render_text('Size', '#C2C2C2', (25, 55))
        self.render_text('Width', '#EEE1C5', (50, 80))
        self.render_text('Height', '#EEE1C5', (50, 120))
        
        self.render_text('Marker Palete', '#C2C2C2', (25, 155))
        self.render_text('Palete', '#EEE1C5', (50, 185))
            
        pygame.draw.rect(self.text_face, '#525552', (47, 227, 326, 108))
        pygame.draw.rect(self.text_face, '#D4B155', (47, 227, 326, 108), 2)
        pygame.draw.rect(self.text_face, '#6A4A32', (49, 229, 322, 104), 1)
            