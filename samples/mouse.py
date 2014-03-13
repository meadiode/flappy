#! /usr/bin/env python
# encoding: utf-8

import flappy
from flappy.display import Sprite
from flappy.events import Event, MouseEvent
from flappy.text import TextField, TextFieldAutoSize
from flappy.ui import Mouse

WIDTH = 600
HEIGHT = 600

class MouseExample(Sprite):

    def __init__(self):
        super(MouseExample, self).__init__()

        spr = Sprite()
        spr.x = WIDTH * 0.25
        spr.y = HEIGHT * 0.25
        self.addChild(spr)

        gfx = spr.graphics
        gfx.beginFill(0xe6db74)
        gfx.drawRect(0.0, 0.0, WIDTH * 0.5, HEIGHT * 0.5)
        gfx.endFill()

        self.txt = TextField()
        self.txt.selectable = False
        self.txt.autoSize = TextFieldAutoSize.LEFT
        spr.addChild(self.txt)

        spr.addEventListener(MouseEvent.MOUSE_OVER, self.on_spr_mouse_over)
        spr.addEventListener(MouseEvent.MOUSE_OUT, self.on_spr_mouse_out)
        spr.addEventListener(MouseEvent.MOUSE_DOWN, self.on_spr_mouse_down)
        spr.addEventListener(MouseEvent.MOUSE_UP, self.on_spr_mouse_up)

        self.cursor = Sprite()
        self.cursor.mouseEnabled = False
        self.addChild(self.cursor)

        gfx = self.cursor.graphics
        gfx.lineStyle(2.0, 0x000000)
        gfx.beginFill(0xff0000)
        gfx.lineTo(0.0, 20.0)
        gfx.lineTo(15.0, 10.0)
        gfx.endFill()

        self.addEventListener(Event.ADDED_TO_STAGE, self.on_stage)

    def on_stage(self, event):
        Mouse.hide()
        self.stage.addEventListener(MouseEvent.MOUSE_MOVE, self.on_mouse_move)
        self.stage.color = 0x383830

    def on_mouse_move(self, event):
        self.cursor.x = event.stageX
        self.cursor.y = event.stageY

    def on_spr_mouse_over(self, event):
        self.txt.text = 'MouseEvent.MOUSE_OVER'    

    def on_spr_mouse_out(self, event):
        self.txt.text = 'MouseEvent.MOUSE_OUT'    

    def on_spr_mouse_down(self, event):
        self.txt.text = 'MouseEvent.MOUSE_DOWN'    

    def on_spr_mouse_up(self, event):
        self.txt.text = 'MouseEvent.MOUSE_UP'


if __name__ == '__main__':
    flappy.start(MouseExample, width=WIDTH, height=HEIGHT, title=__file__)