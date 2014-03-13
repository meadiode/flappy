

class TextFormat(object):

    def __init__(self, font='_sans', size=12, color=0x0, bold=False, 
                    italic=False, underline=False, url='', target='', 
                        align='left', leftMargin=0, rightMargin=0, 
                            indent=0, leading=0):
        self.font = font
        self.size = size
        self.color = color
        self.bold = bold
        self.italic = italic
        self.underline = underline
        self.url = url
        self.target = target
        self.leftMargin = leftMargin
        self.rightMargin = rightMargin
        self.indent = indent
        self.leading = leading
        self.align = align

    @property
    def align(self):
        return TextFormatAlign._STR_MAP[self._align]

    @align.setter
    def align(self, value):
        if not (value in TextFormatAlign._INT_MAP):
            raise ValueError('Invalid text format align value "%s"' % align)
        self._align = TextFormatAlign._INT_MAP[value]


class TextFormatAlign(object):
    LEFT    = 'left'
    RIGHT   = 'right'
    CENTER  = 'center'
    JUSTIFY = 'justify'
    
    _INT_MAP = {
        CENTER  : 0,
        JUSTIFY : 1,
        LEFT    : 2,
        RIGHT   : 3,
    }

    _STR_MAP = {
        0 : CENTER,
        1 : JUSTIFY,
        2 : LEFT,
        3 : RIGHT,
    }
