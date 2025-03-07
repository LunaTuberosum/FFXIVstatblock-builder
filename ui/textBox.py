from settings import *


class TextBox():
    BOLD: int = 0
    BOLD_OFF: int = 1
    ITALIC: int = 2
    ITALIC_OFF: int = 3
    ABILITY: int = 4
    ABILITY_OFF: int = 5
    ATTRIBUTE: int = 6
    ATTRIBUTE_OFF: int = 7
    NEW_LINE: int = 8

    END: int = -1
    TEXT_WIDTH: int = 14
    LINE_CHAR: int = 32
    CURSOR_OFFSET: int = 5

    def __init__(self, pos: list[int], size: list[int], exitCommand: callable, topleft: bool = False):
        self.backgroundSelected: dict[str, pygame.Surface] = _splitBackground('assets/backgrounds/UITextBoxBackground_selected.png')
        self.background: dict[str, pygame.Surface] = _splitBackground('assets/backgrounds/UITextBoxBackground.png')

        self.pos: list[int] = pos
        self.size: list[int] = size ## H = number of rows, w = number of pixels
        self.exitCommand: callable = exitCommand

        self.image: pygame.Surface = pygame.Surface((self.size[0], self.size[1] * 30))
        self.rect: pygame.Rect = pygame.Rect(self.pos, self.image.size)

        self.topleft: bool = topleft

        self.text: str = ''
        self.lines: int = 0
        self.lastLines: int = self.lines

        self.cursor: str = '|'
        self.cursorPos: list[int] = [0, 0]
        self.cursorIndex: int = -1

        self.lineCharWidth: list[int] = []

        self.active: bool = False
        self.hovering: bool = False

        self.font: pygame.font.Font = pygame.font.Font('assets/fonts/noto-sans.regular.ttf', 18)

        self.fontBold: pygame.font.Font = pygame.font.Font('assets/fonts/noto-sans.regular.ttf', 18)
        self.fontBold.bold = True

        self.fontItalic: pygame.font.Font = pygame.font.Font('assets/fonts/noto-sans.regular.ttf', 18)
        self.fontItalic.italic = True

        self.format: bool = False
        self.textFormating: dict[int, int] = {}

        self.bold: bool = False
        self.italic: bool = False
        self.red: bool = False
        self.blue: bool = False

        self.currentFormat: dict[str, bool] = {
            'bold': False,
            'italic': False,
            'red': False,
            'blue': False
        }

    def exitField(self):
        self.active = False

        self.cursorIndex = TextBox.END

        if self.exitCommand:
            self.exitCommand()

    def _backspaceFormat(self):
        if not (len(self.text) in self.textFormating):
            return
        
        self.textFormating.pop(len(self.text))

    def _setFormat(self, onFormat: int, offFormat: int):
        _isFormated: bool = False

        for _index, _format in self.textFormating.items():
            if self.cursorIndex != -1 and _index > self.cursorIndex: continue

            if _format == onFormat: _isFormated = True
            if _format == offFormat: _isFormated = False

        self.textFormating[len(self.text) if self.cursorIndex == TextBox.END else self.cursorIndex] = offFormat if _isFormated else onFormat

    def _addChar(self, event: pygame.Event):
        _char: list[str] = list(self.text)

        if self.cursorIndex == TextBox.END: _char.insert(len(self.text), event.unicode)
        else: 
            _char.insert(self.cursorIndex, event.unicode)
            self.cursorIndex += 1

        self.text = ''.join(_char)

    def _removeChar(self):
        _chars: list[str] = list(self.text)
        if len(_chars) == 0: return
                
        _chars.pop(self.cursorIndex - 1 if self.cursorIndex != TextBox.END else self.cursorIndex)
        self.cursorIndex = max(self.cursorIndex - 1, -1)

        self.text = ''.join(_chars)

    def typing(self, event: pygame.Event):
        if self.active:
            # Delete of text and removal of formating
            if event.key == pygame.K_BACKSPACE:
                print(self.cursorIndex)
                self._backspaceFormat()
                self._removeChar()

            # Moving of the cursor
            elif event.key == pygame.K_LEFT:
                if not self.text: return
                if self.cursorIndex == TextBox.END: 
                    self.cursorIndex = len(self.text)

                self.cursorIndex = max(self.cursorIndex - 1, 0)

            elif event.key == pygame.K_RIGHT:
                if not self.text: return
                if self.cursorIndex == TextBox.END: return

                if self.cursorIndex == len(self.text) - 1: 
                    self.cursorIndex = TextBox.END
                    return

                self.cursorIndex = min(self.cursorIndex + 1, len(self.text))

            # Create new line
            elif event.mod & pygame.KMOD_SHIFT and event.key == pygame.K_RETURN:
                self.textFormating[len(self.text) if self.cursorIndex == TextBox.END else self.cursorIndex] = TextBox.NEW_LINE

            # Handle formating creation
            elif event.key == pygame.K_LCTRL:
                self.format = True
            
            elif self.format and event.key == pygame.K_b:
                self.format = False
                self._setFormat(TextBox.BOLD, TextBox.BOLD_OFF)

            elif self.format and event.key == pygame.K_i:
                self.format = False
                self._setFormat(TextBox.ITALIC, TextBox.ITALIC_OFF)

            elif self.format and event.key == pygame.K_a:
                self.format = False
                self._setFormat(TextBox.ABILITY, TextBox.ABILITY_OFF)

            elif self.format and event.key == pygame.K_t:
                self.format = False
                self._setFormat(TextBox.ATTRIBUTE, TextBox.ATTRIBUTE_OFF)

            # Exiting of the text box using enter
            elif event.key == pygame.K_RETURN:
                self.exitField()
                return
            
            # The adding of characters while typing
            else:
                self.format = False
                self._addChar(event)

    def _drawBackground(self, size: list[int], background: dict[str, pygame.Surface]):
        self.image.blit(background['TopLeft'], (0, 0))
        self.image.blit(background['TopRight'], (size[0] - 10, 0))
        self.image.blit(background['BottomLeft'], (0, size[1] - 10))
        self.image.blit(background['BottomRight'], (size[0] - 10, size[1] - 10))

        self.image.blit(pygame.transform.scale(background['TopMiddle'], (size[0] - 20, 10)), (10, 0))
        self.image.blit(pygame.transform.scale(background['Left'], (10, size[1] - 20)), (0, 10))
        self.image.blit(pygame.transform.scale(background['Right'], (10, size[1] - 20)), (size[0] - 10, 10))
        self.image.blit(pygame.transform.scale(background['BottomMiddle'], (size[0] - 20, 10)), (10, size[1] - 10))

        self.image.blit(pygame.transform.scale(background['Middle'], (size[0] - 20, size[1] - 20)), (10, 10))

    def draw(self, screen: pygame.Surface, right: int, scroll: list[int]):
        _background: dict[str, pygame.Surface] = self.background if not self.hovering else self.backgroundSelected
        if self.active:
            _background = self.backgroundSelected

        _size = self.image.size

        self._drawBackground(_size, _background)

        if self.size[1] > 1:
            self.multiLineBlit()

        else:
            _pos: list[int] = [
                _size[0] / 2 - self.font.size(self.text)[0] / 2, 
                _size[1] / 2 - self.font.size(self.text)[1] / 2
            ]

            if self.topleft: _pos = [8, 5]
            elif self.font.size(self.text)[0] > _size[0]: _pos = [
                                                                    _size[0] - self.font.size(self.text)[0] - 10, 
                                                                    _size[1] / 2 - self.font.size(self.text)[1] / 2
                                                                ]

            self.image.blit(self.font.render(self.text + ('_' if self.active else ''), True, '#000000'), (_pos[0] + 1, _pos[1] + 1))
            self.image.blit(self.font.render(self.text + ('_' if self.active else ''), True, '#ffffff'), _pos)
        
        self.rect: pygame.Rect = pygame.Rect((self.pos[0] + right, self.pos[1] + scroll[1]), self.image.size)
        screen.blit(self.image, (self.pos[0] + right, self.pos[1] + scroll[1]))

    def _formatCheck(self, index: int, wordBuffer: str, bufferFormating: dict[int, int]) -> int:
        if not (index in self.textFormating):
            return 0
        
        if self.textFormating[index] == TextBox.NEW_LINE:
            return 1
        
        bufferFormating[len(wordBuffer)] = self.textFormating[index]
        return 0

    def _formatCharSize(self, char: str, index: int) -> int:
        if not (index in self.textFormating):
            return self.font.size(char)[0]
        
        match self.textFormating[index]:
            case TextBox.BOLD: return self.fontBold.size(char)[0]
            case TextBox.ABILITY: return self.fontBold.size(char)[0]
            case TextBox.ATTRIBUTE: return self.fontBold.size(char)[0]

            case TextBox.ITALIC: return self.fontItalic.size(char)[0]
            
            case _: return self.font.size(char)[0]

    def _formatHandle(self, index: int, bufferFormating: dict[int, int]):
        if not (index in bufferFormating):
            return
        
        match (bufferFormating[index]):
            case TextBox.BOLD: self.bold = True
            case TextBox.BOLD_OFF: self.bold = False

            case TextBox.ITALIC: self.italic = True
            case TextBox.ITALIC_OFF: self.italic = False

            case TextBox.ABILITY: self.red = True
            case TextBox.ABILITY_OFF: self.red = False

            case TextBox.ATTRIBUTE: self.blue = True
            case TextBox.ATTRIBUTE_OFF: self.blue = False

    def _renderWord(self, wordBuffer: str, bufferFormating: dict[int, int], x: int, y: int):

        _x: int = x
        _color: str = '#ffffff'
        for _index, _char in enumerate(wordBuffer):
            self._formatHandle(_index, bufferFormating)
            _font: pygame.Font = self.font
            self.currentFormat['bold'] = False
            self.currentFormat['italic'] = False
            self.currentFormat['blue'] = False
            self.currentFormat['red'] = False

            if self.italic:
                _font = self.fontItalic
                self.currentFormat['italic'] = True

            elif self.red: 
                _color = '#D34D35'
                _font = self.fontBold
                self.currentFormat['red'] = True

            elif self.blue: 
                _color = '#2D638E'
                _font = self.fontBold
                self.currentFormat['blue'] = True

            elif self.bold: 
                _font = self.fontBold
                self.currentFormat['bold'] = True

            self.image.blit(_font.render(_char, True, _color), (_x, y))

            _x += self.font.size(_char)[0]

    def _cursorPlaceInBuffer(self):
        _index: int = 0
        _words: list[str] = self.text.split(' ')
        
        for _word in _words:
            for _i, _char in enumerate(_word):
                if _index == self.cursorIndex: return _i
                _index += 1

            _index += 1

        return -1

    def multiLineBlit(self):
        _size: list[int] = self.image.size
        _chars: list[str] = list(self.text)

        _wordBuffer: str = ''
        _bufferFormating: dict[int, int] = {} 

        _lineWidth: int = 0
        _lineIndex: int = 0

        self.lines = 0
        self.lineCharWidth = []

        _x: int = 8
        _y: int = 5

        _cursorInBuffer: bool = False

        for _index, _char in enumerate(_chars):

            if _char == ' ':
                self._renderWord(_wordBuffer, _bufferFormating, _x, _y)
                _x += self.font.size(_wordBuffer)[0] # TODO: needs to check if formated
                _wordBuffer = ''
                _bufferFormating = {}
                _cursorInBuffer = False

            if self._formatCheck(_index, _wordBuffer, _bufferFormating) == 1:
                _y += 20
                _x = 8
                _lineWidth = self.font.size(_wordBuffer)[0]
                self.lines += 1
                self.lineCharWidth.append(_lineIndex - len(_wordBuffer))
                _lineIndex = len(_wordBuffer) - 1

            _charSize: int = self._formatCharSize(_char, _index)

            if _lineWidth + _charSize > _size[0] - TextBox.TEXT_WIDTH:

                if self.font.size(_wordBuffer)[0] + _charSize > _size[0] - TextBox.TEXT_WIDTH:
                    self._renderWord(_wordBuffer, _bufferFormating, _x, _y)
                    _wordBuffer = ''

                _prevX: int = _x - (self.font.size(_wordBuffer.strip())[0])
                _x = 8
                _y += 20

                if _cursorInBuffer:
                    self.cursorPos = [_x - TextBox.CURSOR_OFFSET, _y]
                    _placeInBuffer: int = self._cursorPlaceInBuffer()
                    if _placeInBuffer == -1: self.cursorPos = [_prevX - TextBox.CURSOR_OFFSET, _y - 20]

                    for _i, _c in enumerate(_wordBuffer.strip()):
                        if _i == _placeInBuffer: 
                            break
                        self.cursorPos[0] += self.font.size(_c)[0]

                _lineWidth = self.font.size(_wordBuffer)[0]
                self.lineCharWidth.append(_lineIndex - len(_wordBuffer))
                _wordBuffer = _wordBuffer.strip()

                self.lines += 1

            _lineWidth += _charSize
            _wordBuffer = _wordBuffer + _char
            _lineIndex += 1

            if _index == self.cursorIndex:
                _cursorInBuffer = True
                self.cursorPos = [_x - TextBox.CURSOR_OFFSET, _y]

                for _i, _c in enumerate(_wordBuffer):
                    if _i == len(_wordBuffer) - 1: break
                    self.cursorPos[0] += self.font.size(_c)[0]

        if _wordBuffer:
            self._renderWord(_wordBuffer, _bufferFormating, _x, _y)
            self.lineCharWidth.append(_lineIndex)
            _x += self.font.size(_wordBuffer)[0]

        if self.cursorIndex == TextBox.END:
            self.cursorPos = [_x - TextBox.CURSOR_OFFSET, _y]

        if self.cursorIndex == 0:
            self.cursorPos = [4, 5]

        if self.active:
            self.image.blit(self.font.render(self.cursor, True, '#ffffff'), self.cursorPos)

        if len(self.text) in self.textFormating:
            match self.textFormating[len(self.text)]:
                case TextBox.BOLD: self.currentFormat['bold'] = True
                case TextBox.BOLD_OFF: self.currentFormat['bold'] = False

                case TextBox.ITALIC: self.currentFormat['italic'] = True
                case TextBox.ITALIC_OFF: self.currentFormat['italic'] = False

                case TextBox.ABILITY: self.currentFormat['red'] = True
                case TextBox.ABILITY_OFF: self.currentFormat['red'] = False

                case TextBox.ATTRIBUTE: self.currentFormat['blue'] = True
                case TextBox.ATTRIBUTE_OFF: self.currentFormat['blue'] = False

        self.bold = False
        self.italic = False
        self.red = False
        self.blue = False

    def hover(self):
        self.hovering = True

    def noHover(self):
        if not self.hovering:
            return
        self.hovering = False

    def onClick(self):
        self.active = True

def _splitBackground(file: str) -> dict[str, pygame.Surface]:

    _img = pygame.image.load(file).convert_alpha()

    _temp: dict[str, pygame.Surface] = {
        'TopLeft': None,
        'TopMiddle': None,
        'TopRight': None,
        'Left': None,
        'Middle': None,
        'Right': None,
        'BottomLeft': None,
        'BottomMiddle': None,
        'BottomRight': None
    }

    _temp['TopLeft'] = pygame.surface.Surface((10, 10))
    _temp['TopLeft'].fill('#ff00b6')
    _temp['TopLeft'].set_colorkey('#ff00b6')
    _temp['TopLeft'].blit(_img, (0, 0))
    _temp['TopMiddle'] = pygame.surface.Surface((10, 10))
    _temp['TopMiddle'].fill('#ff00b6')
    _temp['TopMiddle'].set_colorkey('#ff00b6')
    _temp['TopMiddle'].blit(_img, (-10, 0))
    _temp['TopRight'] = pygame.surface.Surface((10, 10))
    _temp['TopRight'].fill('#ff00b6')
    _temp['TopRight'].set_colorkey('#ff00b6')
    _temp['TopRight'].blit(_img, (-20, 0))

    _temp['Left'] = pygame.surface.Surface((10, 10))
    _temp['Left'].fill('#ff00b6')
    _temp['Left'].set_colorkey('#ff00b6')
    _temp['Left'].blit(_img, (0, -10))
    _temp['Middle'] = pygame.surface.Surface((10, 10))
    _temp['Middle'].fill('#ff00b6')
    _temp['Middle'].set_colorkey('#ff00b6')
    _temp['Middle'].blit(_img, (-10, -10))
    _temp['Right'] = pygame.surface.Surface((10, 10))
    _temp['Right'].fill('#ff00b6')
    _temp['Right'].set_colorkey('#ff00b6')
    _temp['Right'].blit(_img, (-20, -10))

    _temp['BottomLeft'] = pygame.surface.Surface((10, 10))
    _temp['BottomLeft'].fill('#ff00b6')
    _temp['BottomLeft'].set_colorkey('#ff00b6')
    _temp['BottomLeft'].blit(_img, (0, -20))
    _temp['BottomMiddle'] = pygame.surface.Surface((10, 10))
    _temp['BottomMiddle'].fill('#ff00b6')
    _temp['BottomMiddle'].set_colorkey('#ff00b6')
    _temp['BottomMiddle'].blit(_img, (-10, -20))
    _temp['BottomRight'] = pygame.surface.Surface((10, 10))
    _temp['BottomRight'].fill('#ff00b6')
    _temp['BottomRight'].set_colorkey('#ff00b6')
    _temp['BottomRight'].blit(_img, (-20, -20))

    return _temp