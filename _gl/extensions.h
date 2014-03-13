#include <stdio.h>

#include <OGL.h>

#if defined(HX_WINDOWS) && !defined(OGL_EXTENSIONS_INITIALIZED)

#define DEFINE_EXTENSION
#include <OGLExtensions.h>
#undef DEFINE_EXTENSION

void gl_init_extensions()
{
    static bool extensions_init = false;
    if(!extensions_init)
    {
        extensions_init = true;
        #define GET_EXTENSION
        #include <OGLExtensions.h>
        #undef GET_EXTENSION
    }
}

#define OGL_EXTENSIONS_INITIALIZED
#endif