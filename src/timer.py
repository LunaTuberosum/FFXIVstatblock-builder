import pygame


class Timer():
    def __init__(self, duration: int) -> None:
        self.begin_time: int = 0
        self.duration: int = duration

    def start(self) -> None:
        self.begin_time = pygame.time.get_ticks()

    def reset(self) -> None:
        self.begin_time = 0

    def time_left(self) -> int:
        return (self.begin_time + self.duration) - pygame.time.get_ticks()

    def is_done(self) -> bool:
        if not self.begin_time:
            return False
        
        return self.begin_time + self.duration < pygame.time.get_ticks()