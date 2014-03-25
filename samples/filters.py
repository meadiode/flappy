#! /usr/bin/env python
# encoding: utf-8

import flappy

from flappy.display import Sprite
from flappy.filters import BlurFilter, GlowFilter, DropShadowFilter
from flappy.text import TextField, TextFormat, TextFieldAutoSize
from flappy.events import Event, MouseEvent
from flappy.geom import Point

import math

WIDTH = 800
HEIGHT = 600

class FiltersExample(Sprite):

    def __init__(self):
        super(FiltersExample, self).__init__()
        
        def create_text(text):
            format = TextFormat(size=62, font='./resources/papercuts-2.ttf')
            tf = TextField()
            tf.defaultTextFormat = format
            tf.autoSize = TextFieldAutoSize.LEFT
            tf.text = text
            tf.selectable = False
            tf.x = (WIDTH - tf.textWidth) * 0.5
            tf.y = (HEIGHT - tf.textHeight) * 0.5
            return tf

        self.blur_txt = create_text('BLUR')
        self.glow_txt = create_text('GLOW')
        self.shadow_txt = create_text('SHADOW')
        
        self.addEventListener(Event.ADDED_TO_STAGE, self.on_stage)
        self.current_setup = 0

    def on_stage(self, event):
        self.stage.addEventListener(MouseEvent.MOUSE_MOVE, self.on_mouse_move)
        self.stage.addEventListener(MouseEvent.CLICK, self.on_click)
        self.set_blur()

    def on_mouse_move(self, event):
        bx = (WIDTH * 0.5 - event.stageX) / WIDTH * 100.0
        by = (HEIGHT * 0.5 - event.stageY) / HEIGHT * 100.0
        self.update_func(bx, by)

    def on_click(self, event):
        setups = [self.set_blur, self.set_glow, self.set_shadow]
        self.current_setup += 1
        if self.current_setup >= len(setups):
            self.current_setup = 0
        self.removeChildAt(0)
        setups[self.current_setup]()

    def set_blur(self):
        self.stage.color = 0xfcdd76
        self.addChild(self.blur_txt)
        self.update_func = self.update_blur

    def update_blur(self, bx, by):
        blur = BlurFilter(blurX=abs(bx), blurY=abs(by))
        self.blur_txt.filters = [blur]    

    def set_glow(self):
        self.stage.color = 0x000020
        self.addChild(self.glow_txt)
        self.update_func = self.update_glow

    def update_glow(self, bx, by):
        glow = GlowFilter(color=0x00ff00, alpha=1.0, 
                            blurX=abs(bx), blurY=abs(by), strength=2.0)
        self.glow_txt.filters = [glow]

    def set_shadow(self):
        self.stage.color = 0xfcdd76
        self.addChild(self.shadow_txt)
        self.update_func =self.update_shadow

    def update_shadow(self, bx, by):
        pt = Point(bx, by)
        distance = pt.length
        pt.normalize()
        angle = (math.atan2(pt.y, pt.x) / math.pi) * 180.0
        shadow = DropShadowFilter(distance=distance, angle=angle, alpha=0.5)
        self.shadow_txt.filters = [shadow]

if __name__ == '__main__':
    flappy.start(FiltersExample, width=WIDTH, height=HEIGHT, title=__file__)