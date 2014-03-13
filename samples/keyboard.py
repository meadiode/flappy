#! /usr/bin/env python
# encoding: utf-8

import flappy
from flappy.display import Sprite
from flappy.events import Event, MouseEvent, KeyboardEvent
from flappy.ui import Keyboard

from time import time

WIDTH = 600
HEIGHT = 600

BALL_RADIUS = 40
GRAVITY = 200
THRUST = 5000
DAMP = 0.8

class KeyboardExample(Sprite):

    def __init__(self):
        super(KeyboardExample, self).__init__()
        
        self.ball = Sprite()
        self.ball.cacheAsBitmap = True
        gfx = self.ball.graphics
        gfx.beginFill(0x20a000)
        gfx.drawCircle(0.0, 0.0, BALL_RADIUS)
        gfx.endFill()

        self.ball.x = WIDTH * 0.5
        self.ball.y = HEIGHT * 0.5

        self.vx, self.vy = 0.0, 0.0
        self.ax, self.ay = 0.0, 0.0

        self.addChild(self.ball)

        self.addEventListener(Event.ADDED_TO_STAGE, self.on_stage)
        self.addEventListener(Event.ENTER_FRAME, self.on_enter_frame)
        self.addEventListener(MouseEvent.MOUSE_DOWN, self.on_mouse_down)
        self.addEventListener(KeyboardEvent.KEY_DOWN, self.on_key_down)

        self.old_time = time()

    def on_key_down(self, event):
        if event.keyCode == Keyboard.LEFT:
            self.ax -= THRUST        
        if event.keyCode == Keyboard.RIGHT:
            self.ax += THRUST        
        if event.keyCode == Keyboard.UP:
            self.ay -= THRUST        
        if event.keyCode == Keyboard.DOWN:
            self.ay += THRUST

    def on_stage(self, event):
        self.stage.color = 0x383830
        self.stage.focus = self

    def on_mouse_down(self, event):
        self.stage.focus = self

    def on_enter_frame(self, event):
        new_time = time()
        dt = new_time - self.old_time
        
        self.vy += (GRAVITY + self.ay) * dt
        self.vx += self.ax * dt
        self.ball.x += self.vx * dt
        self.ball.y += self.vy * dt
        
        if (self.ball.x + BALL_RADIUS) > WIDTH:
            self.vx = -self.vx * DAMP
            self.ball.x = WIDTH - BALL_RADIUS
        elif (self.ball.x - BALL_RADIUS) < 0.0:
            self.vx = -self.vx * DAMP
            self.ball.x = BALL_RADIUS
        elif (self.ball.y + BALL_RADIUS) > HEIGHT:
            self.vy = -self.vy * DAMP
            self.ball.y = HEIGHT - BALL_RADIUS             
        elif (self.ball.y - BALL_RADIUS) < 0.0:
            self.vy = -self.vy * DAMP
            self.ball.y = BALL_RADIUS            

        self.ax, self.ay = 0.0, 0.0
        self.old_time = new_time


if __name__ == '__main__':
    flappy.start(KeyboardExample, width=WIDTH, height=HEIGHT, title=__file__)