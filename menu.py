from settings import *
import editor


def main(screen: pygame.Surface, clock: pygame.time.Clock) -> None:
    
    while True:
        clock.tick(30)
        screen.fill('#B7B7B7')

        screen.blit(JUPITER_FONT.render('FFXIV TTRPG Stat Card Builder', True, '#000000'), (10, 20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    editor.main(screen, clock, 0)

        pygame.display.flip()