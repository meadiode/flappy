
import struct
from flappy import _gl as gl

class IndexBuffer3D(object):

    def __init__(self, data=None):
        self.gl_buffer = gl.createBuffer()
        self.num_indeces = 0
        if data:
            self.upload(data)

    def __del__(self):
        gl.deleteBuffer(self.gl_buffer)

    def upload(self, data):
        ndata = struct.pack('%sH' % len(data), *data)
        gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, self.gl_buffer)
        gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, ndata, gl.STATIC_DRAW)
        self.num_indeces = len(data)