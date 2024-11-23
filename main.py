from settings import *

from menu import Menu


pygame.init()

clock: pygame.time.Clock = pygame.time.Clock()

screen: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption('FFXIV TTRPG Stat Card Build')
pygame.key.set_repeat(200, 100)

if __name__ == '__main__':
    Menu(screen, clock).main()