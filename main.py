from settings import *

import menu


pygame.init()

clock: pygame.time.Clock = pygame.time.Clock()

screen: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE, vsync=1)
pygame.display.set_caption('FFXIV TTRPG Stat Card Build')
pygame.key.set_repeat(200, 100)

if __name__ == '__main__':
    menu.main(screen, clock)