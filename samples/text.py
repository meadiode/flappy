#! /usr/bin/env python
# encoding: utf-8

import flappy
from flappy.display import Sprite
from flappy.text import TextField, TextFormat, TextFieldAutoSize, Font

WIDTH = 800
HEIGHT = 280

LINE = 'The quick brown fox jumps over the lazy dog\n'
LINE_LEN = len(LINE)

class TextExample(Sprite):
    def __init__(self):
        super(TextExample, self).__init__()

        def_format = TextFormat(size=24, font='_serif')
        txt = TextField()
        txt.defaultTextFormat = def_format
        txt.width = WIDTH
        txt.height = HEIGHT
        txt.selectable = False
        txt.multiline = True

        formats = [
            TextFormat(size=24, font='_serif'),
            TextFormat(size=26, bold=True, font='_serif'),
            TextFormat(size=28, bold=True),
            TextFormat(size=30, color=0xff0000),
            TextFormat(size=22, bold=True, color=0x0000ff, align='right'),            
            TextFormat(size=22, bold=True, color=0x8080ff, align='center'),
            TextFormat(size=26, font='_typewriter'),
            TextFormat(size=30, font='./resources/papercuts-2.ttf'),
        ]

        for line_n in range(len(formats)):
            txt.text += LINE

        for line_n, fmt in enumerate(formats):
            txt.setTextFormat(fmt, 
                                first=LINE_LEN * line_n, 
                                    last = LINE_LEN * (line_n + 1))
        self.addChild(txt)


if __name__ == '__main__':
    flappy.start(TextExample, width=WIDTH, height=HEIGHT, title=__file__)