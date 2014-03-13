

from flappy import _core, _gl as gl
from flappy.events import Event
from flappy.display import DirectRenderer, Stage, BitmapData
from flappy.geom import Rectangle
from flappy.display3d import Texture
from flappy.display3d.vertexbuffer3d import VertexBuffer3D, VertexBuffer3DFormat


class Scene3DClearMask(object):
    COLOR       = gl.COLOR_BUFFER_BIT
    DEPTH       = gl.DEPTH_BUFFER_BIT
    STENCIL     = gl.STENCIL_BUFFER_BIT
    ALL         = COLOR | DEPTH | STENCIL


class Context3DTriangleFace(object):
    BACK            = 'back'
    FRONT           = 'front'
    FRONT_AND_BACK  = 'frontAndBack'
    NONE            = 'none'


class Scene3D(DirectRenderer):

    def __init__(self, antialias=0, enable_depth_and_stencil=False, 
                                                            name='Scene3D'):
        DirectRenderer.__init__(self, render_func=self._render, name=name)
        self._antialias = antialias
        self._depth_n_stencil = enable_depth_and_stencil
        self._current_prog = None
        self._frame_buffer = None
        self._fb_depth_n_stencil = False
        self._render_to_texture = False

        self._queue = []

        self.scrollRect = Rectangle(0.0, 0.0, 0.0, 0.0)

    def clear(self, red=1.0, green=0.0, blue=0.0, alpha=1.0, 
                            depth=1.0, stencil=0, mask=Scene3DClearMask.ALL):
    #TODO: clear depth and stenicil
        self._do(gl.clearColor, red, green, blue, alpha)
        self._do(gl.clear, mask)

    def setProgram(self, program):
        self._current_prog = program
        self._do(gl.useProgram, program.gl_program)
        gl.useProgram(program.gl_program)

    def setVertexBufferAt(self, locname, vbuffer, offset=0, 
                                        format=VertexBuffer3DFormat.FLOAT_1):
        loc = gl.getAttribLocation(self._current_prog.gl_program, locname)
        gl.bindBuffer(gl.ARRAY_BUFFER, vbuffer.gl_buffer)

        tp = gl.FLOAT
        numbytes = 4
        dimension = 4
        try:
            dimension = {
                VertexBuffer3DFormat.BYTES_4: 4,
                VertexBuffer3DFormat.FLOAT_1: 1,
                VertexBuffer3DFormat.FLOAT_2: 2,
                VertexBuffer3DFormat.FLOAT_3: 3,
                VertexBuffer3DFormat.FLOAT_4: 4,
            }[format]
        except KeyError:
            raise ValueError('Buffer format "%s" is not supported' % \
                                                                str(format))

        self._do(gl.bindBuffer, gl.ARRAY_BUFFER, vbuffer.gl_buffer)
        self._do(gl.enableVertexAttribArray, loc)
        self._do(gl.vertexAttribPointer, loc, dimension, tp, False, 
                    vbuffer.data32_per_vertex * numbytes, offset * numbytes)

    def setProgramConstantFromMatrix(self, locname, mat, transpose=False):
        loc = gl.getUniformLocation(self._current_prog.gl_program, locname)
        self._do(gl.uniformMatrix, loc, transpose, mat)

    def setProgramConstant(self, locname, data):
        loc = gl.getUniformLocation(self._current_prog.gl_program, locname)
        
        if isinstance(data, int):
            self._do(gl.uniform1i, loc, data)
        elif isinstance(data, float):
            self._do(gl.uniform1f, loc, data)
        else:
            assert len(data) <= 4
            meth_tp = 'f' if isinstance(data[0], float) else 'i'
            meth = getattr(gl, 'uniform%d%s' % (len(data), meth_tp))
            self._do(meth, loc, *data)

    def setTextureAt(self, locname, texture, texture_index=0):
        loc = gl.getUniformLocation(self._current_prog.gl_program, locname)

        assert 0 <= texture_index < 8, \
                    'Texture index "%s" is not supported' % str(texture_index)
        self._do(gl.activeTexture, gl.TEXTURE0 + texture_index)

        self._bind_texture(texture)

        self._do(gl.uniform1i, loc, texture_index)
        self._do(gl.texParameter, gl.TEXTURE_2D,
                        gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE)
        self._do(gl.texParameter, gl.TEXTURE_2D,
                        gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE)
        self._do(gl.texParameter, gl.TEXTURE_2D,
                        gl.TEXTURE_MIN_FILTER, gl.LINEAR)
        self._do(gl.texParameter, gl.TEXTURE_2D,
                        gl.TEXTURE_MAG_FILTER, gl.LINEAR)

    def drawTriangles(self, ibuffer, first_index=0, num_triangles=-1):
        num_indeces = 0
        
        if num_triangles == -1:
            num_indeces = ibuffer.num_indeces
        else:
            num_indeces = num_triangles * 3

        self._do(gl.bindBuffer, gl.ELEMENT_ARRAY_BUFFER, ibuffer.gl_buffer)
        self._do(gl.drawElements, gl.TRIANGLES, num_indeces,
                                            gl.UNSIGNED_SHORT, first_index)

    def setRenderToTexture(self, texture, enable_depth_and_stencil=False, 
                                            antialias=0, surface_selector=0):
        if self._frame_buffer is None:
            self._frame_buffer = gl.createFramebuffer()

        self._render_to_texture = True
        self._fb_depth_n_stencil = enable_depth_and_stencil

        self._do(self._bind_texture, texture)
        self._do(gl.texParameter, gl.TEXTURE_2D,
                                    gl.TEXTURE_WRAP_S, gl.REPEAT)
        self._do(gl.texParameter, gl.TEXTURE_2D,
                                    gl.TEXTURE_WRAP_T, gl.REPEAT)
        self._do(gl.texParameter, gl.TEXTURE_2D,
                                    gl.TEXTURE_MIN_FILTER, gl.LINEAR)
        self._do(gl.texParameter, gl.TEXTURE_2D,
                                    gl.TEXTURE_MAG_FILTER, gl.LINEAR)

        self._do(gl.bindFramebuffer, gl.FRAMEBUFFER, self._frame_buffer)
        self._set_depth_and_stencil(enable_depth_and_stencil)
        self._do(gl.framebufferTexture2D, gl.FRAMEBUFFER,gl.COLOR_ATTACHMENT0, 
                                        gl.TEXTURE_2D, texture.gl_texture, 0)
        self._do(gl.viewport, 0, 0, texture.width, texture.height)
        self._do(gl.scissor, 0, 0, texture.width, texture.height)

    def setRenderToBackBuffer(self):
        self._render_to_texture = False
        self._do(gl.bindFramebuffer, gl.FRAMEBUFFER, 0)
        self._set_depth_and_stencil(self._depth_n_stencil)
        sr = self.scrollRect
        self._do(gl.viewport, sr.x, sr.y, sr.width, sr.height)
        self._do(gl.scissor, sr.x, sr.y, sr.width, sr.height)

    def setWidth(self, width):
        super(Scene3D, self).setWidth(width)
        self.scrollRect.width = width
        self.setScrollRect(self.scrollRect)

    def setHeight(self, height):
        super(Scene3D, self).setHeight(height)
        self.scrollRect.height = height
        self.setScrollRect(self.scrollRect)

    def _bind_texture(self, texture):
        if isinstance(texture, BitmapData):
            self._do(_core.bindBitmapDataTexture, texture)
        elif isinstance(texture, Texture):
            self._do(gl.bindTexture, gl.TEXTURE_2D, texture.gl_texture)
        else:
            raise ValueError('Unsupported texture class "%s"' % \
                                                texture.__class__.__name__)

    def _set_depth_and_stencil(self, value):
        if value:
            self._do(gl.enable, gl.DEPTH_TEST)
            self._do(gl.enable, gl.DEPTH_STENCIL)
        else:
            self._do(gl.disable, gl.DEPTH_TEST)
            self._do(gl.disable, gl.DEPTH_STENCIL)                 

    def _do(self, *args):
        self._queue.append(args)

    def _render(self, rect):
        gl.enable(gl.SCISSOR_TEST)
        gl.enable(gl.CULL_FACE)

        if (not self._render_to_texture and self._depth_n_stencil) or \
            (self._render_to_texture and self._fb_depth_n_stencil):
            gl.enable(gl.DEPTH_TEST)
            gl.enable(gl.DEPTH_STENCIL)
        
        gl.viewport(rect.x, rect.y, rect.width, rect.height)
        gl.scissor(rect.x, rect.y, rect.width, rect.height)

        for com in self._queue:
            com[0](*com[1:])

        self._queue = []
        gl.disable(gl.SCISSOR_TEST)
        gl.disable(gl.CULL_FACE)
        gl.disable(gl.DEPTH_TEST)

        gl.useProgram(0)
        gl.bindBuffer(gl.ARRAY_BUFFER, 0)
        gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, 0)
        gl.bindFramebuffer(gl.FRAMEBUFFER, 0)
        gl.viewport(0.0, 0.0, self.stage.stageWidth, self.stage.stageHeight)

