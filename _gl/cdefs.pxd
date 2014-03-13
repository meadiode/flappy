#include "config.pxi"

cdef extern from "extensions.h":

    ctypedef int GLint
    ctypedef int GLsizei
    ctypedef void GLvoid
    ctypedef unsigned int GLuint
    ctypedef unsigned int GLenum
    ctypedef unsigned char GLboolean
    ctypedef unsigned char GLubyte
    ctypedef char GLchar
    ctypedef float GLfloat
    ctypedef double GLdouble
    ctypedef int GLsizeiptr

    GLenum glGetError()
    void glFinish()
    void glFlush()

    void glEnable(GLenum cap)
    void glDisable(GLenum cap)

    void glHint(GLenum target, GLenum mode)
    void glLineWidth(GLfloat width)

    void glFrontFace(GLenum face)

    GLboolean glIsBuffer(GLenum val)
    GLboolean glIsEnabled(GLenum val)
    GLboolean glIsProgram(GLenum val)
    GLboolean glIsShader(GLenum val)
    GLboolean glIsTexture(GLenum val)

    void glStencilFunc(GLenum func, GLint ref, GLuint mask)
    void glStencilFuncSeparate(GLenum face, GLenum func, GLint ref, GLuint mask)
    void glStencilMask(GLuint mask)
    void glStencilMaskSeparate(GLenum face, GLuint mask)
    void glStencilOp(GLenum fail, GLenum zfail, GLenum zpass)
    void glStencilOpSeparate(GLenum face, GLenum fail, GLenum zfail, GLenum zpass)

    void glBlendColor(GLfloat r, GLfloat g, GLfloat b, GLfloat a)
    void glBlendEquation(GLenum mode)
    #void glBlendEquationSeparate(unsigned int rgb, unsigned int a)
    void glBlendFunc(GLenum source, GLenum dest)


    GLuint glCreateProgram()
    void glLinkProgram(GLuint program)
    void glValidateProgram(GLuint program)
    void glDeleteProgram(GLuint program)
    void glBindAttribLocation(GLuint program, GLuint index, const GLchar* name)
    int glGetUniformLocation(GLuint program, const GLchar* name)
    int glGetAttribLocation(GLuint program, const GLchar* name)
    void glUseProgram(GLuint program)
    void glGetProgramInfoLog(GLuint program, GLint bufSize, GLint *length, GLchar *infoLog)
    void glGetActiveUniform(GLuint program, GLuint index, GLsizei bufSize, GLsizei* length, 
                                        GLint* size, GLenum* type, GLchar* name)
    void glGetActiveAttrib(GLuint program, GLuint index, GLsizei bufSize, GLsizei *length, 
                                        GLint *size, GLenum *type, GLchar *name)
    void glGetUniformfv(GLuint program, GLint location, GLfloat *params)
    void glGetUniformiv(GLuint program, GLint location, GLint *params)
    void glGetProgramiv(GLenum target, GLenum pname, GLint *params)

    void glEnableVertexAttribArray(GLuint index)
    void glDisableVertexAttribArray(GLuint index)

    void glUniform1i(GLint location, GLint val0)
    void glUniform2i(GLint location, GLint val0, GLint val1)
    void glUniform3i(GLint location, GLint val0, GLint val1, GLint val2)
    void glUniform4i(GLint location, GLint val0, GLint val1, GLint val2, GLint val3)

    void glUniform1f(GLint location, GLfloat val0)
    void glUniform2f(GLint location, GLfloat val0, GLfloat val1)
    void glUniform3f(GLint location, GLfloat val0, GLfloat val1, GLfloat val2)
    void glUniform4f(GLint location, GLfloat val0, GLfloat val1, GLfloat val2, GLfloat val3)

    void glUniform1fv(GLint location, GLsizei count, const GLfloat *value)
    void glUniform2fv(GLint location, GLsizei count, const GLfloat *value)
    void glUniform3fv(GLint location, GLsizei count, const GLfloat *value)
    void glUniform4fv(GLint location, GLsizei count, const GLfloat *value)
    void glUniform1iv(GLint location, GLsizei count, const GLint *value)
    void glUniform2iv(GLint location, GLsizei count, const GLint *value)
    void glUniform3iv(GLint location, GLsizei count, const GLint *value)
    void glUniform4iv(GLint location, GLsizei count, const GLint *value)

    void glVertexAttrib1f(GLuint location, GLfloat val0)
    void glVertexAttrib2f(GLuint location, GLfloat val0, GLfloat val1)
    void glVertexAttrib3f(GLuint location, GLfloat val0, GLfloat val1, GLfloat val2)
    void glVertexAttrib4f(GLuint location, GLfloat val0, GLfloat val1, GLfloat val2, GLfloat val3)
    void glVertexAttribPointer(GLuint index, GLint size, GLenum type, GLboolean normalized, 
                                        GLsizei stride, const GLvoid *pointer)

    void glUniformMatrix2fv(GLint location, GLsizei count, GLboolean transpose, const GLfloat *value)
    void glUniformMatrix3fv(GLint location, GLsizei count, GLboolean transpose, const GLfloat *value)
    void glUniformMatrix4fv(GLint location, GLsizei count, GLboolean transpose, const GLfloat *value)

    GLuint glCreateShader(GLenum type)
    void glDeleteShader(GLuint shader)
    void glCompileShader(GLuint shader)
    void glAttachShader(GLuint program, GLuint shader)
    void glDetachShader(GLuint program, GLuint shader)
    void glShaderSource(GLuint shader, GLsizei count, const GLchar **strings, const GLint *length)
    void glGetShaderiv(GLuint shader, GLenum pname, GLint *params)

    void glActiveTexture(GLenum texture)

    void glGenBuffers(GLsizei n, GLuint *buffers)
    void glBindBuffer(GLenum target, GLuint buffer)
    void glDeleteBuffers(GLsizei n, const GLuint *buffers)
    void glBufferData (GLenum target, GLsizeiptr size, const GLvoid *data, GLenum usage)

    void glViewport(GLuint x, GLuint y, GLuint w, GLuint h)
    void glScissor(GLuint x, GLuint y, GLuint w, GLuint h)
    void glClear(GLuint mask)
    void glClearColor(GLfloat r, GLfloat g, GLfloat b, GLfloat a)

    void glDrawArrays(GLenum mode, GLint first, GLint count)
    void glDrawElements(GLenum mode, GLsizei count, GLenum type, const GLvoid *indices)


    const GLubyte* glGetString(GLenum name)

    void glGetBooleanv(GLenum pname, GLboolean *params)
    void glGetDoublev(GLenum pname, GLdouble *params)
    void glGetFloatv(GLenum pname, GLfloat *params)
    void glGetIntegerv(GLenum pname, GLint *params)


    void glBindFramebuffer(GLenum target, GLuint framebuffer)

    void glBindRenderbuffer(GLenum target, GLuint renderbuffer)
    void glDeleteRenderbuffers(GLsizei n, const GLuint *renderbuffers)
    void glGenRenderbuffers(GLsizei n, GLuint *renderbuffers)
    void glRenderbufferStorage(GLenum target, GLenum internalformat, GLsizei width, GLsizei height)
    void glDeleteFramebuffers(GLsizei n, const GLuint *framebuffers)
    void glGenFramebuffers(GLsizei n, GLuint *framebuffers)
    void glFramebufferTexture2D(GLenum target, GLenum attachment, GLenum textarget, GLuint texture, GLint level)
    void glFramebufferRenderbuffer(GLenum target, GLenum attachment, GLenum renderbuffertarget, GLuint renderbuffer)

    void glTexImage2D(GLenum target, GLint level,
                                    GLint internalFormat,
                                    GLsizei width, GLsizei height,
                                    GLint border, GLenum format, GLenum type,
                                    const GLvoid *pixels)

    void glTexSubImage2D(GLenum target, GLint level,
                                    GLint xoffset, GLint yoffset,
                                    GLsizei width, GLsizei height,
                                    GLenum format, GLenum type,
                                    const GLvoid *pixels)


    void glGenTextures(GLsizei n, GLuint *textures)
    void glDeleteTextures(GLsizei n, const GLuint *textures)
    void glBindTexture(GLenum target, GLuint texture)
    void glActiveTexture(GLenum texture)
    void glTexParameterf(GLenum target, GLenum pname, GLfloat param)
    void glTexParameteri(GLenum target, GLenum pname, GLint param)

    void gl_init_extensions()
