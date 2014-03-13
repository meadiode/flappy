#! /usr/bin/env python
# encoding: utf-8

import flappy
from flappy.events import Event, KeyboardEvent
from flappy.ui import Keyboard
from flappy.geom import Matrix3D
from flappy.display3d import Scene3D, VertexBuffer3D, VertexBuffer3DFormat
from flappy.display3d import IndexBuffer3D, Program3D, Texture
from flappy.display import Sprite

from time import time
import os


WIDTH = 800
HEIGHT = 600
RES_X = 512
RES_Y = 512

RESOURCES_DIR = './resources'

class HerokuShaders(Sprite):

    def __init__(self):
        super(HerokuShaders, self).__init__()

        self.scene = Scene3D()
        self.scene.width = WIDTH
        self.scene.height = HEIGHT        
        self.addChild(self.scene)

        self.texture = Texture(RES_X, RES_Y)

        quad_vertices = [
            -1.0, -1.0,
             1.0, -1.0,
            -1.0,  1.0,
             1.0,  1.0,
        ]

        quad_indeces = [0, 1, 2, 2, 1, 3]

        self.vbuffer = VertexBuffer3D(data32_per_vertex=2, data=quad_vertices)
        self.ibuffer = IndexBuffer3D(quad_indeces)

        self.heroku_program = Program3D()
        self.render_program = Program3D()
        
        self.vshader_src = \
        '''
            attribute vec2 pos;
            
            uniform vec2 surfaceSize;
            uniform vec2 resolution;

            varying vec2 surfacePosition;
            
            void main() {
                
                surfacePosition = pos;
                vec2 p = (resolution / surfaceSize) * pos;
                gl_Position = vec4( p.x, p.y, 1.0, 1.0 );
                
            }
        '''

        self.fshader_src = \
        '''
            uniform sampler2D tex;
            varying vec2 surfacePosition;

            void main(void){
                gl_FragColor = texture2D(tex, (surfacePosition + 1.0) * 0.5);
            }
        '''

        self.render_program.upload(self.vshader_src, self.fshader_src)
        
        self.next_shader_index = 0
        self.shader_files = []
        for fname in os.listdir(RESOURCES_DIR):
            ffname = os.path.join(RESOURCES_DIR, fname)
            if os.path.isfile(ffname):
                if fname.startswith('heroku_') and fname.endswith('.frag'):
                    self.shader_files.append(ffname)
        self.set_next_shader()

        self.addEventListener(Event.ENTER_FRAME, self.on_enter_frame)
        self.addEventListener(Event.ADDED_TO_STAGE, self.on_stage)
        self.addEventListener(KeyboardEvent.KEY_DOWN, self.on_key_down)

        self.start_time = time()

    def on_stage(self, event):
        self.stage.focus = self

    def on_key_down(self, event):
        if event.keyCode == Keyboard.SPACE:
            self.set_next_shader()

    def on_enter_frame(self, event):
        timeval = time() - self.start_time
        
        scene = self.scene
        scene.clear(0.0, 0.0, 0.0, 1.0)

        scene.setRenderToTexture(self.texture)
        scene.setProgram(self.heroku_program)
        scene.setVertexBufferAt('pos', self.vbuffer, 0, 
                                            VertexBuffer3DFormat.FLOAT_2)

        scene.setProgramConstant('resolution', [float(RES_X), float(RES_Y)])
        scene.setProgramConstant('surfaceSize', [float(RES_X), float(RES_Y)])
        scene.setProgramConstant('time', timeval)
        scene.setProgramConstant('mouse', [0.5, 0.5])
        scene.setProgramConstant('backbuffer', 0)
        scene.drawTriangles(self.ibuffer)

        scene.setRenderToBackBuffer()
        scene.setProgram(self.render_program)
        scene.setVertexBufferAt('pos', self.vbuffer, 0, 
                                            VertexBuffer3DFormat.FLOAT_2)
        scene.setProgramConstant('resolution', [float(WIDTH), float(HEIGHT)])
        scene.setProgramConstant('surfaceSize', [float(WIDTH), float(HEIGHT)])
        scene.setTextureAt('tex', self.texture)
        scene.drawTriangles(self.ibuffer)

    def set_next_shader(self):
        file_name = self.shader_files[self.next_shader_index]
        print(file_name)
        fshader_file = open(file_name, 'r')
        fshader_src = fshader_file.read()
        self.heroku_program.upload(self.vshader_src, fshader_src)
        self.next_shader_index += 1
        if self.next_shader_index >= len(self.shader_files):
            self.next_shader_index = 0


if __name__ == '__main__':
    flappy.start(HerokuShaders, width=WIDTH, height=HEIGHT, title=__file__)
