from src.gameLoop import GameLoop
from src.saveConvter import check_saves


if __name__ == '__main__':
    check_saves('')
    
    main_loop: GameLoop = GameLoop()
    
    main_loop.update()