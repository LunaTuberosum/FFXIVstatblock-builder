from typing import Callable


class Bus():
    def __init__(self, signals: dict[str, list[Callable[[None], None]]]) -> None:
        self.signals: dict[str, list[Callable[[None], None]]] = signals
        
    def reset(self) -> None:
        for sign in self.signals.keys():
            self.signals[sign] = []
    
    def register(self, signal: str, call: Callable[[None], None]) -> None:
        try:
            self.signals.get(signal).append(call)
            
        except:
            raise Exception(f'Could not find signal: {signal}')
        
    def deregister(self, signal: str, call: Callable[[None], None]) -> None:
        try:
            _signal: list[Callable[[None], None]] = self.signals.get(signal)
            
            for _function in _signal:
                if _function == call:
                    self.signals.get(signal).remove(call)
                    return
            
        except:
            raise Exception(f'Could not find signal: {signal}')
        
    def sign(self, signal: str) -> None:
        try:
            _signal: list[Callable[[None], None]] = self.signals.get(signal)
            
            for _function in _signal:
                _function()
                
        except Exception as e:
            raise Exception(f'Could not find signal: {signal}')