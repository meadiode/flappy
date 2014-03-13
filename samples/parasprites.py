#! /usr/bin/env python
# encoding: utf-8

import flappy
from flappy.display import Sprite, Bitmap, BitmapData, Tilesheet
from flappy.events import Event, MouseEvent
from flappy.geom import Rectangle, Point

import math
import random
from time import time

WIDTH = 1000
HEIGHT = 600
START_PARASPRITES = 5
MAX_PARASPRITES = 1000


class ParaspritesExample(Sprite):

    def __init__(self):
        super(ParaspritesExample, self).__init__()

        background = Bitmap(BitmapData.load('./resources/ponyville.jpg'))
        background.width = WIDTH
        background.height = HEIGHT
        self.addChild(background)

        self.tile_layer = Sprite()
        self.addChild(self.tile_layer)

        parasprites_bd = BitmapData.load('./resources/parasprite_sheet.png')
        self.parasprites_ts = Tilesheet(parasprites_bd)

        twidth = parasprites_bd.width / 4.0
        theight = parasprites_bd.height / 3.0

        for i in range(3):
            for j in range(4): 
                self.parasprites_ts.addTileRect(
                    Rectangle(twidth * j, theight * i, twidth, theight),
                        Point(twidth * 0.5, theight * 0.5))

        self.parasprites = [ ]
        for i in range(START_PARASPRITES):
            self.parasprites.append(
                Parasprite(
                    random.uniform(WIDTH * 0.1, WIDTH * 0.9),
                        random.uniform(HEIGHT * 0.1, HEIGHT * 0.9),
                    ))

        self.addEventListener(Event.ENTER_FRAME, self.on_enter_frame)
        self.tile_layer.addEventListener(MouseEvent.CLICK, self.on_click)
        self.old_time = time()

    def on_enter_frame(self, event):
        new_time = time()
        dt = new_time - self.old_time

        tilesheet_data = []

        for parasprite in self.parasprites:
            parasprite.process(dt)
            tilesheet_data += parasprite.get_tile_data()

        self.tile_layer.graphics.clear()
        self.tile_layer.graphics.drawTiles(
                            self.parasprites_ts, tilesheet_data, 
                                Tilesheet.TILE_ROTATION | \
                                    Tilesheet.TILE_SCALE | \
                                        Tilesheet.TILE_SMOOTH)
        self.old_time = new_time

    def on_click(self, event):
        if len(self.parasprites) <= MAX_PARASPRITES:
            self.parasprites.append(Parasprite(event.stageX, event.stageY))


class Parasprite(object):
    ANIM_TIME = 0.025
    NFRAMES = 4
    RADIUS = 25.0

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.frame_time = 0.0
        self.frame = 0
        self.anim_dir = 1
        self.tileset = random.randint(0, 2)
        self.speed = random.uniform(80.0, 250.0)
        direction_angle = random.uniform(0.0, math.pi * 2.0)
        self.direction_x = math.cos(direction_angle)
        self.direction_y = math.sin(direction_angle)
        self.rotation = random.uniform(-math.pi * 0.2, math.pi * 0.2)
        self.scale = random.uniform(1.0, 1.2)
        self.radius = self.RADIUS * self.scale

    def process(self, dt):
        self.frame_time += dt
        if self.frame_time >= self.ANIM_TIME:
            self.frame_time = 0.0
            self.frame += self.anim_dir
            if not (0 <= self.frame < self.NFRAMES):
                self.frame -= self.anim_dir
                self.anim_dir = -self.anim_dir

        self.x += self.speed * dt * self.direction_x 
        self.y += self.speed * dt * self.direction_y

        if not (self.radius < self.x < (WIDTH - self.radius)):
            self.direction_x = -self.direction_x
            self.x = max(self.radius, min(WIDTH - self.radius, self.x))
        if not (self.radius < self.y < (HEIGHT - self.radius)):
            self.direction_y = -self.direction_y
            self.y = max(self.radius, min(HEIGHT - self.radius, self.y))

    def get_tile_data(self):
        return  [
                    self.x,
                    self.y,
                    self.tileset * self.NFRAMES + self.frame,
                    self.scale,
                    self.rotation, 
                ]

if __name__ == '__main__':
    flappy.start(ParaspritesExample, width=WIDTH, 
                                        height=HEIGHT, title=__file__)
