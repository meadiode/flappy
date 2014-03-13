

from flappy._core import _get_fonts_directory
import os

class Font(object):

    def __init__(self, filename='', style=None, type_=None):
        print filename, style, type_

    @staticmethod
    def enumerateFonts(enumerateDeviceFonts=False):
        result = []
        fonts_dir = _get_fonts_directory()
        
        if enumerateDeviceFonts:
            for dirpath, dirnames, filenames in os.walk(fonts_dir):
                for filename in filenames:
                    style = FontStyle.REGULAR
                    lname = filename.lower()

                    if lname.endswith(('bold italic.ttf', 
                                            'bold-italic.ttf', 
                                                'bolditalic.ttf')):
                        style = FontStyle.BOLD_ITALIC
                    elif lname.endswith('italic.ttf'):
                        style = FontStyle.ITALIC
                    elif lname.endswith('bold.ttf'):
                        style = FontStyle.BOLD

                    fnt = Font(os.path.join(dirpath, filename), 
                                                    style, FontType.DEVICE)
                    result.append(fnt)

        return result


class FontStyle(object):
    BOLD            = 'bold'
    BOLD_ITALIC     = 'boldItalic'
    ITALIC          = 'italic'
    REGULAR         = 'regular'

class FontType(object):
    DEVICE          = 'device'
    EMBEDDED        = 'embedded'
    EMBEDDED_CFF    = 'embeddedCFF'
