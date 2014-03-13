

include "config.pxi"

from cpython cimport bool
from libc.stdlib cimport malloc, free
from libc.string cimport strcpy, strtok
from cdefs cimport *

import struct

include "constants.pxi"

def getError():
    return glGetError()

def finish():
    glFinish()

def glush():
    glFlush()

def enable(int cap):
    glEnable(cap)

def disable(int cap):
    glDisable(cap)

def hint(int target, int mode):
    glHint(target, mode)

def lineWidth(float width):
    glLineWidth(width)

def frontFace(int face):
    glFrontFace(face)

def isBuffer(int val):
    return glIsBuffer(val) != 0

def isEnabled(int val):
    return glIsEnabled(val) != 0

def isProgram(int val):
    return glIsProgram(val) != 0

def isShader(int val):
    return glIsShader(val) != 0

def isTexture(int val):
    return glIsTexture(val) != 0

def stencilFunc(int func, int ref, int mask):
    glStencilFunc(func, ref, mask)

def stencilFuncSeparate(int face, int func, int ref, int mask):
    glStencilFuncSeparate(face, func, ref, mask)

def stencilMask(int mask):
    glStencilMask(mask)

def stencilMaskSeparate(int face, int mask):
    glStencilMaskSeparate(face, mask)

def stencilOp(int fail, int zfail, int zpass):
    glStencilOp(fail, zfail, zpass)

def stencilOpSeparate(int face, int fail, int zfail, int zpass):
    glStencilOpSeparate(face, fail, zfail, zpass)

def blendColor(float r, float g, float b, float a):
    glBlendColor(r, g, b, a)

def blendEquation(int mode):
    glBlendEquation(mode)

def blendFunc(int source, int dest):
    glBlendFunc(source, dest)

def createProgram():
    return glCreateProgram()

def linkProgram(int program):
    glLinkProgram(program)

def validateProgram(int program):
    glValidateProgram(program)

def deleteProgram(int program):
    glDeleteProgram(program)

def bindAttribLocation(int program, int index, const char* name):
    glBindAttribLocation(program, index, name)

def getUniformLocation(int program, const char* name):
    return glGetUniformLocation(program, name)

def getAttribLocation(int program, const char* name):
    return glGetAttribLocation(program, name)

def useProgram(int program):
    glUseProgram(program)

def getProgramLog(int program):
    cdef char buf[1024]
    glGetProgramInfoLog(program, 1024, NULL, buf)
    return str(buf)

def getUniform(int program, int location):
    cdef char buf[1]
    cdef GLsizei outLen = 1
    cdef GLsizei size = 0
    cdef GLenum tp = 0
    cdef int iresult = 0
    cdef float fresult = 0.0

    glGetActiveUniform(program, location, 1, &outLen, &size, &tp, buf)
    ints, floats, bools = 0, 0, 0

    FLOAT_VEC = { FLOAT_VEC2 : 2, FLOAT_VEC3 : 3, FLOAT_VEC4 : 4}
    INT_VEC = { INT_VEC2 : 2, INT_VEC3 : 3, INT_VEC4 : 4}
    BOOL_VEC = { BOOL_VEC2 : 2, BOOL_VEC3 : 3, BOOL_VEC4 :4}
    FLOAT_MAT = {
        FLOAT_MAT2 : 2,
        FLOAT_MAT3 : 9,
        FLOAT_MAT4 : 16,
    }

    INT_TYPES = [INT, BOOL, SAMPLER_2D]
    
    if tp == FLOAT:
        floats = 1
        glGetUniformfv(program, location, &fresult)
        return fresult
    elif tp in FLOAT_VEC:
        floats = FLOAT_VEC[tp]
    elif tp in INT_VEC:
        ints = INT_VEC[tp]
    elif tp in BOOL_VEC:
        bools = BOOL_VEC[tp]
    elif tp in INT_TYPES:
        ints = 1

    cdef int ibuffer[4]
    if max(ints, bools) > 0:
        glGetUniformiv(program, location, ibuffer)
        return [ibuffer[i] for i in range(max(ints, bools))]

    cdef float fbuffer[16 * 3]
    if floats:
        glGetUniformfv(program, location, fbuffer)
        return [fbuffer[i] for i in range(floats)]

    raise ValueError("Undefined uniform in location %i of program %i" % (program, location))

def getProgramParameter(int program, int name):
    cdef int ret
    glGetProgramiv(program, name, &ret)
    return ret

def getActiveAttrib(int program, int index):
    cdef char buf[1024]
    cdef GLsizei outLen = 1024
    cdef GLsizei size = 0
    cdef GLenum  tp = 0
    glGetActiveAttrib(program, index, 1024, &outLen, &size, &tp, buf)
    ret = {
        'size' : <int>size,
        'type' : <int>tp,
        'name' : str(buf)
    }
    return ret

def getActiveUniform(int program, int index):
    cdef char buf[1024]
    cdef GLsizei outLen = 1024
    cdef GLsizei size = 0
    cdef GLenum  tp = 0
    glGetActiveUniform(program, index, 1024, &outLen, &size, &tp, buf)
    ret = {
        'size' : <int>size,
        'type' : <int>tp,
        'name' : str(buf)
    }
    return ret

def enableVertexAttribArray(int index):
    glEnableVertexAttribArray(index)

def disableVertexAttribArray(int index):
    glDisableVertexAttribArray(index)

def uniform1i(int location, int val0):
    glUniform1i(location, val0)

def uniform2i(int location, int val0, int val1):
    glUniform2i(location, val0, val1)

def uniform3i(int location, int val0, int val1, int val2):
    glUniform3i(location, val0, val1, val2)

def uniform4i(int location, int val0, int val1, int val2, int val3):
    glUniform4i(location, val0, val1, val2, val3)

def uniform1f(int location, float val0):
    glUniform1f(location, val0)

def uniform2f(int location, float val0, float val1):
    glUniform2f(location, val0, val1)

def uniform3f(int location, float val0, float val1, float val2):
    glUniform3f(location, val0, val1, val2)

def uniform4f(int location, float val0, float val1, float val2, float val3):
    glUniform4f(location, val0, val1, val2, val3)

def uniformMatrix(int location, bool transpose, mat):
    cdef float buf[16]
    n = len(mat)
    for i in range(n):
        buf[i] = mat[i]
    if n == 4:
        glUniformMatrix2fv(location, 1, transpose, buf)
    elif n == 9:
        glUniformMatrix3fv(location, 1, transpose, buf)
    elif n == 16:
        glUniformMatrix4fv(location, 1, transpose, buf)
    else:
        raise ValueError("Unsupported matrix type")

#TODO: uniform_x_iv
#TODO: uniform_x_fv

def vertexAttrib1f(int location, float val0):
    glVertexAttrib1f(location, val0)

def vertexAttrib2f(int location, float val0, float val1):
    glVertexAttrib2f(location, val0, val1)

def vertexAttrib3f(int location, float val0, float val1, float val2):
    glVertexAttrib3f(location, val0, val1, val2)

def vertexAttrib4f(int location, float val0, float val1, float val2, float val3):
    glVertexAttrib4f(location, val0, val1, val2, val3)

def vertexAttribPointer(int index, int size, int tp, bool normalized, int stride, int offset):
    glVertexAttribPointer(index, size, tp, normalized, stride, <void*>offset)

def createShader(stype):
    return glCreateShader(stype)

def deleteShader(int shader):
    glDeleteShader(shader)

def compileShader(int shader):
    glCompileShader(shader)

def attachShader(int program, int shader):
    glAttachShader(program, shader)

def detachShader(int program, int shader):
    glDetachShader(program, shader)

def shaderSource(int shader, source):
    pystr = str(source)
    IF GLES == True:
        pystr = "precision mediump float;\n" + pystr
    cdef char *src = pystr
    glShaderSource(shader, 1, <const char**>&src, NULL)

def getShaderParameter(int shader, int param):
    cdef int ret
    glGetShaderiv(shader, param, &ret)
    return ret

def createBuffer():
    cdef int ret
    glGenBuffers(1, <unsigned int*>&ret)
    return ret

def deleteBuffer(int buffer):
    glDeleteBuffers(1, <unsigned int*>&buffer)

def bindBuffer(int target, int buffer):
    glBindBuffer(target, buffer)

def bufferData(int buffer, data, int usage):
    packed = None
    if isinstance(data[0], float):
        packed = struct.pack('%sf' % len(data), *data)
    elif isinstance(data[0], int):
        packed = struct.pack('%si' % len(data), *data)
    elif isinstance(data, str):
        packed = data
    cdef char *cdata = packed
    glBufferData(buffer, len(packed), cdata, usage) 

def viewport(int x, int y, int w, int h):
    glViewport(x, y, w, h)

def scissor(int x, int y, int w, int h):
    glScissor(x, y, w, h)

def clear(unsigned int mask):
    glClear(mask)

def clearColor(float r, float g, float b, float a):
    glClearColor(r, g, b, a)

def drawArrays(int mode, int first, int count):
    glDrawArrays(mode, first, count)

def drawElements(int mode, int count, int tp, first):
    glDrawElements(mode, count, tp, <const void*>(<int>first))

def activeTexture(int texture):
    glActiveTexture(texture)

def bindFramebuffer(int target, int buffer):
    glBindFramebuffer(target, buffer)

def bindRenderbuffer(int target, int buffer):
    glBindRenderbuffer(target, buffer)

def createFramebuffer():
    cdef unsigned int ret
    glGenFramebuffers(1, &ret)
    return ret

def createRenderbuffer():
    cdef unsigned int ret
    glGenRenderbuffers(1, &ret)
    return ret

def framebufferRenderbuffer(int target, int attachment, int rbuffer_target, int rbuffer):
    glFramebufferRenderbuffer(target, attachment, rbuffer_target, rbuffer)

def framebufferTexture2D(int target, int attachment, int texture_target, int texture, int level):
    glFramebufferTexture2D(target, attachment, texture_target, texture, level)

def renderbufferStorage(int target, int internal_format, int width, int height):
    glRenderbufferStorage(target, internal_format, width, height)

def createTexture():
    cdef unsigned int ret
    glGenTextures(1, &ret)
    return ret

def activeTexture(int slot):
    glActiveTexture(slot)

def bindTexture(int target, int slot):
    glBindTexture(target, slot)

def deleteTexture(int texture):
    glDeleteTextures(1, <const unsigned int*>&texture)

def texImage2D(int target, int level, int internal, int width, int height, 
                int border, int format, int tp, buffer):
    cdef char *bytes
    if buffer:
        bytes = <char*>buffer
    else:
        bytes = NULL
    glTexImage2D(target, level, internal, width, height, 
                    border, format, tp, bytes)

def texSubImage2D(int target, int level, int width, int height, 
                int xoffset, int yoffset, int format, int tp, buffer):
    cdef char *bytes = <char*>buffer
    glTexSubImage2D(target, level, width, height, 
                    xoffset, yoffset, format, tp, bytes)

def texParameter(int target, int pname, val):
    if isinstance(val, float):
        glTexParameterf(target, pname, val)
    elif isinstance(val, int):
        glTexParameteri(target, pname, val)

def getSupportedExtensions():
    cdef const char *cext = <const char*>glGetString(EXTENSIONS)
    cdef char *ext = NULL
    cdef char *tok = NULL
    
    ret = []
    if cext != NULL:
        ext = <char*>malloc(len(cext) + 1)
        strcpy(ext, cext)
        tok = strtok(ext, " ")
        while tok != NULL:
            ret.append(str(tok))
            tok = strtok(NULL, " ")
        free(ext)
    return ret

def getParameter(int name):
    floats, ints, strings = 0, 0, 0

    if name in (ALIASED_LINE_WIDTH_RANGE, ALIASED_POINT_SIZE_RANGE, DEPTH_RANGE):
        floats = 2
    elif name in (BLEND_COLOR, COLOR_CLEAR_VALUE):
        floats = 4
    elif name == COLOR_WRITEMASK:
        ints = 4
    elif name == MAX_VIEWPORT_DIMS:
        ints = 2
    elif name in (SCISSOR_BOX, VIEWPORT):
        ints = 4
    elif name in (DEPTH_CLEAR_VALUE,
                    LINE_WIDTH,
                    POLYGON_OFFSET_FACTOR,
                    POLYGON_OFFSET_UNITS,
                    SAMPLE_COVERAGE_VALUE,

                    BLEND,
                    DEPTH_WRITEMASK,
                    DITHER,
                    CULL_FACE,
                    POLYGON_OFFSET_FILL,
                    SAMPLE_COVERAGE_INVERT,
                    STENCIL_TEST,

                    ALPHA_BITS,
                    ACTIVE_TEXTURE,
                    BLEND_DST_ALPHA,
                    BLEND_DST_RGB,
                    BLEND_EQUATION_ALPHA,
                    BLEND_EQUATION_RGB,
                    BLEND_SRC_ALPHA,
                    BLEND_SRC_RGB,
                    BLUE_BITS,
                    CULL_FACE_MODE,
                    DEPTH_BITS,
                    DEPTH_FUNC,
                    DEPTH_TEST,
                    FRONT_FACE,
                    GENERATE_MIPMAP_HINT,
                    GREEN_BITS,
                    MAX_COMBINED_TEXTURE_IMAGE_UNITS,
                    MAX_CUBE_MAP_TEXTURE_SIZE,
                    MAX_TEXTURE_IMAGE_UNITS,
                    MAX_TEXTURE_SIZE,
                    MAX_VERTEX_ATTRIBS,
                    MAX_VERTEX_TEXTURE_IMAGE_UNITS,
                    NUM_COMPRESSED_TEXTURE_FORMATS,
                    PACK_ALIGNMENT,
                    RED_BITS,
                    SAMPLE_BUFFERS,
                    SAMPLES,
                    SCISSOR_TEST,
                    SHADING_LANGUAGE_VERSION,
                    STENCIL_BACK_FAIL,
                    STENCIL_BACK_FUNC,
                    STENCIL_BACK_PASS_DEPTH_FAIL,
                    STENCIL_BACK_PASS_DEPTH_PASS,
                    STENCIL_BACK_REF,
                    STENCIL_BACK_VALUE_MASK,
                    STENCIL_BACK_WRITEMASK,
                    STENCIL_BITS,
                    STENCIL_CLEAR_VALUE,
                    STENCIL_FAIL,
                    STENCIL_FUNC,
                    STENCIL_PASS_DEPTH_FAIL,
                    STENCIL_PASS_DEPTH_PASS,
                    STENCIL_REF,
                    STENCIL_VALUE_MASK,
                    STENCIL_WRITEMASK,
                    SUBPIXEL_BITS,
                    UNPACK_ALIGNMENT,
                    TEXTURE_BINDING_2D,):
        ints = 1
    elif name in (VENDOR, VERSION, RENDERER):
        strings = 1

    cdef int ivals[4]
    cdef float fvals[4]
    cdef char* strval = NULL

    if ints:
        glGetIntegerv(name, ivals)
        return [ivals[i] for i in range(ints)]
    if floats:
        glGetFloatv(name, fvals)
        return [fvals[i] for i in range(floats)]        
    if strings:
        strval = <char*>glGetString(name)
        return str(strval)

    raise ValueError("Unknown parameter id %i" % name)


def _init_extensions():
    IF PLATFORM == 'WINDOWS':
        gl_init_extensions()