from settings import *
from ui.background import Background
from ui.button import Button


class ConfirmUI(Background):
    def __init__(self, handler: object, text: str, confrimCommand: callable, confirmText: str = 'Confirm', cancelText: str = 'Cancel'):
        super().__init__(
            'ConfirmUI',
            'Confirmation',
            [500, 200],
            [
                (SCREEN_WIDTH / 2) - 250,
                (SCREEN_HEIGHT / 2) - 100
            ],
            False
        )

        self.handler: object = handler

        self.text: str = text
        self.textSize: tuple[int] = self.font.size(self.text)

        self.confirmCommand: callable = confrimCommand

        self.confirmText: str = confirmText
        self.cancelText: str = cancelText

        self.components.append(
            Button(
                [30, (self.size[1] - 65) + self.pos[1]],
                [198, 38],
                'assets/icons/button.png',
                'assets/icons/button_hover.png',
                self.confirmCommand,
                self.confirmText
            )
        )

        self.components.append(
            Button(
                [self.size[0] - 228, (self.size[1] - 65) + self.pos[1]],
                [198, 38],
                'assets/icons/button.png',
                'assets/icons/button_hover.png',
                self.cancel,
                self.cancelText
            )
        )

    def draw(self, screen: pygame.Surface, right: int, zoom: list[int]):
        super().draw(screen, right, zoom)

        self.image.blit(self.font.render(self.text, True, '#000000'), ((self.size[0] / 2) - (self.textSize[0] / 2), 61))
        self.image.blit(self.font.render(self.text, True, '#EEE1C5'), ((self.size[0] / 2) - (self.textSize[0] / 2), 60))

        screen.blit(self.image, self.pos)

        for _comp in self.components:
            _comp.draw(screen, self.rect.left, zoom)

    def cancel(self):
        self.handler.window = None

