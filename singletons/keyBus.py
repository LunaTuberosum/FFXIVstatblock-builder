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
                
                'mouse_scroll_down': [],
                'mouse_scroll_up': [],

                'copy': [],
                'paste': [],
                
                'toggle_bold': [],
                'toggle_italic': [],
                
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