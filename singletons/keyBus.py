from singletons.bus import Bus


class KeyBus(Bus):
    def __init__(self) -> None:
        super().__init__(
            {
                'mouse_left_down': [],
                'mouse_left_up': [],
                
                'mouse_right_down': [],
                'mouse_right_up': [],
                
                'mouse_middle_down': [],
                'mouse_middle_up': [],

                'copy': [],
                'paste': [],
                
                'esc_down': [],
                'esc_up': [],
                
                'space_down': [],
                'space_up': [],
                
                'left_arrow_down': [],
                'left_arrow_up': [],
                
                'up_arrow_down': [],
                'up_arrow_up': [],
                
                'down_arrow_down': [],
                'down_arrow_up': [],
                
                'right_arrow_down': [],
                'right_arrow_up': []
            }
        )
        
key_bus: KeyBus = KeyBus()