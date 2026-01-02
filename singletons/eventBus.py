from typing import Callable

from singletons.bus import Bus


class EventBus(Bus):
    def __init__(self) -> None:
        super().__init__(
            {
                'quit': [],
                
                'change_folder': [],
                'move_file': [],
                'duplicate_sheet': [],
                'delete_file': [],
                
                'load_sheet': [],
                'return_menu': [],
                'swap_traits': [],
                
                'context_menu': [],
                'ui_window': [],
                
                'typing_register': [],
            }
        )

    def sign(self, signal: str, *data) -> None:
        try:
            _signal: list[Callable[..., None]] = self.signals.get(signal)
            
            for _function in _signal:
                _function(*data)
                
        except Exception as e:
            print(e)
            raise Exception(f'Could not find signal: {signal}')
        
event_bus: EventBus = EventBus()