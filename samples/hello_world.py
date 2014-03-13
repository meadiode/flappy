#! /usr/bin/env python
# encoding: utf-8

import flappy
from flappy.display import Sprite
from flappy.text import TextField


class HelloWorld(Sprite):

    def __init__(self):
        super(HelloWorld, self).__init__()
        txt = TextField()
        txt.text = 'Hello World!!!'
        txt.selectable = False
        self.addChild(txt)

if __name__ == '__main__':
    flappy.start(HelloWorld, width=320, height=200, title=__file__)
