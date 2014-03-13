#! /usr/bin/env python
# encoding: utf-8

import flappy
from flappy.events import Event
from flappy.geom import Matrix3D
from flappy.display3d import Scene3D, VertexBuffer3D, VertexBuffer3DFormat
from flappy.display3d import IndexBuffer3D, Program3D
from flappy.display import Sprite

import math
from time import time

WIDTH = 600
HEIGHT = 600

class Cube3DExample(Sprite):

    def __init__(self):
        super(Cube3DExample, self).__init__()

        self.scene = Scene3D()
        self.scene.width = WIDTH
        self.scene.height = HEIGHT        
        self.addChild(self.scene)

        aspect = WIDTH / HEIGHT
        self.proj_mat = Matrix3D.createPerspective(
                                        fov=math.pi * 0.2,
                                            aspect=WIDTH / HEIGHT,
                                                znear=1.0, zfar=500.0)

        self.prog = Program3D()
        vshader = \
            '''
                attribute vec3 vpos;
                attribute vec4 color;
                varying vec4 vcolor;

                uniform mat4 view_mat;
                uniform mat4 proj_mat;

                void main(void) {
                    gl_Position = vec4(vpos, 1.0) * view_mat * proj_mat;
                    vcolor = color;
                }
            '''

        fshader = \
            '''
                varying vec4 vcolor;

                void main(void) {
                    gl_FragColor = vcolor;
                }
            '''

        self.prog.upload(vshader, fshader)

        vertices = [
        #   coords (x, y, z)       color (r, g, b, a)  
             -1.0,  1.0,  1.0,  1.0, 0.0, 0.0, 1.0,
              1.0,  1.0,  1.0,  1.0, 0.0, 0.0, 1.0,
              1.0, -1.0,  1.0,  1.0, 0.5, 0.0, 1.0,
             -1.0, -1.0,  1.0,  1.0, 0.5, 0.0, 1.0,

             -1.0,  1.0, -1.0,  1.0, 0.0, 1.0, 1.0,
              1.0,  1.0, -1.0,  1.0, 0.0, 1.0, 1.0,
              1.0, -1.0, -1.0,  1.0, 1.0, 0.0, 1.0,
             -1.0, -1.0, -1.0,  1.0, 1.0, 0.0, 1.0,
        ]
        self.vbuffer = VertexBuffer3D(data32_per_vertex=7, data=vertices)

        indeces = [
            0, 2, 1,  0, 3, 2,  #front
            0, 4, 3,  3, 4, 7,  #left
            1, 6, 5,  2, 6, 1,  #right
            4, 5, 6,  4, 6, 7,  #back
            0, 5, 4,  1, 5, 0,  #top
            3, 7, 6,  2, 3, 6,  #bottom
        ]
        self.ibuffer = IndexBuffer3D(indeces)

        self.xrot, self.yrot = 0.0, 0.0
        self.rotspeed = math.pi
        self.lasttime = time()

        self.addEventListener(Event.ENTER_FRAME, self.on_enter_frame)

    def on_enter_frame(self, event):
        curtime = time()
        dt = curtime - self.lasttime

        self.xrot += dt * self.rotspeed * 0.2
        self.yrot += dt * self.rotspeed * 0.5

        m = Matrix3D()
        m.translate(0.0, 0.0, -4.0)
        m.rotate(self.xrot, self.yrot, 0.0)
        self.view_mat = m

        scene = self.scene
        scene.clear(0.0, 0.0, 0.0, 1.0)
        scene.setProgram(self.prog)
        scene.setVertexBufferAt('vpos', self.vbuffer, 0, 
                                            VertexBuffer3DFormat.FLOAT_3)
        scene.setVertexBufferAt('color', self.vbuffer, 3, 
                                            VertexBuffer3DFormat.FLOAT_4)
        scene.setProgramConstantFromMatrix('view_mat', self.view_mat)
        scene.setProgramConstantFromMatrix('proj_mat', self.proj_mat)
        scene.drawTriangles(self.ibuffer)

        self.lasttime = curtime

if __name__ == '__main__':
    flappy.start(Cube3DExample, width=WIDTH, height=HEIGHT, title=__file__)
