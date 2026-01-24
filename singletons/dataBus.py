from typing import Callable

from singletons.bus import Bus


class DataBus(Bus):
    def __init__(self) -> None:
        super().__init__(
            {
                'get_display': None,
                
                'get_resolution': None,
                'get_fullscreen': None,
                'get_fps': None,
                'get_monitor': None,
                
                'get_folder_id': None,
                
                'add_color': None,
                'get_colors': None,
            }
        )
        
    def deregister(self, signal: str, call: Callable[[None], None]) -> None:
        try:
            _signal: Callable[[None], None] = self.signals.get(signal)
            if _signal != call:
                raise Exception()
            
            self.signals[signal] = None
            
        except:
            raise Exception(f'Could not find signal: {signal}')
        
    def register(self, signal: str, call: Callable[[None], None]) -> None:
        try:
            self.signals.get(signal)
            
            self.signals[signal] = call
            
        except:
            raise Exception(f'Could not find signal: {signal}')

    def sign(self, signal: str, *data) -> any:
        try:
            _signal: Callable[..., None] = self.signals.get(signal)
            
            return _signal(*data)
                
        except Exception as e:
            print(e)
            raise Exception(f'Could not find signal: {signal}')
        
data_bus: DataBus = DataBus()