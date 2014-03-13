
cdef extern from "TextField.h" namespace "lime":
    
    cdef enum AntiAliasType:
        aaAdvanced,
        aaNormal

    cdef enum AutoSizeMode:
        asCenter, 
        asLeft, 
        asNone, 
        asRight 

    cdef enum TextFormatAlign:
        tfaCenter,
        tfaJustify,
        tfaLeft,
        tfaRight

    enum GridFitType:
        gftNone,
        gftPixel,
        gftSubPixel

    cdef cppclass Optional[T]:
        Optional(T &val)
        T& __Get()
        void Set()
        # T& operator=(T &rhs)

    cdef cppclass TextFormat:
        void DecRef()

        Optional[TextFormatAlign]   align
        Optional[int]               blockIndent
        Optional[bool]              bold
        Optional[bool]              bullet
        Optional[uint32]            color
        Optional[WString]           font
        Optional[int]               indent
        Optional[bool]              italic
        Optional[bool]              kerning
        Optional[int]               leading
        Optional[int]               leftMargin
        Optional[int]               letterSpacing
        Optional[int]               rightMargin
        Optional[int]               size
        # Optional[QuickVec[int] ]tabStops
        Optional[WString]           target
        Optional[bool]              underline
        Optional[WString]           url

    cdef cppclass TextField(DisplayObject):
        TextField()

        void appendText(WString inString)
        Rect getCharBoundaries(int inCharIndex)
        int getCharIndexAtPoint(double x, double y)
        int getFirstCharInParagraph(int inCharIndex)
        int getLineIndexAtPoint(double x,double y)
        int getLineIndexOfChar(int inCharIndex)
        int getLineLength(int inLineIndex)
        WString getLineText()
        int getParagraphLength(int inCharIndex)
        TextFormat *getTextFormat(int inFirstChar, int inEndChar)
        bool isFontCompatible(const WString &inFont, const WString &inStyle)
        void replaceSelectedText(const WString &inText)
        void replaceText(int inBeginIndex, int inEndIndex, const WString &inText)
        int  setSelection(int inFirst, int inLast)
        void setTextFormat(TextFormat *inFormat, int inFirstChar, int inLastChar)
        bool getSelectable()
        void setSelectable(bool inSelectable)
        void setTextColor(int inColor)
        int  getTextColor()
        bool getIsInput()
        void setIsInput(bool inIsInput)
        AutoSizeMode getAutoSize()
        void  setAutoSize(int inAutoSize)

        int   getCaretIndex()
        int   getMaxScrollH()
        int   getMaxScrollV()
        int   getBottomScrollV()
        int   getScrollH()
        void  setScrollH(int inScrollH)
        int   getScrollV()
        void  setScrollV(int inScrollV)
        int   getNumLines()
        int   getSelectionBeginIndex()
        int   getSelectionEndIndex()

        const TextFormat *getDefaultTextFormat()
        void setDefaultTextFormat(TextFormat *inFormat)

        bool  getBackground()
        void  setBackground(bool inBackground)
        int   getBackgroundColor()
        void  setBackgroundColor(int inBackgroundColor)
        bool  getBorder()
        void  setBorder(bool inBorder)
        int   getBorderColor()
        void  setBorderColor(int inBorderColor)
        bool  getMultiline()
        void  setMultiline(bool inMultiline)
        bool  getWordWrap()
        void  setWordWrap(bool inWordWrap)
        int   getMaxChars()
        void  setMaxChars(int inMaxChars)
        bool  getDisplayAsPassword()
        void  setDisplayAsPassword(bool inValue)
        int   getLineOffset(int inLine)
        WString getLineText(int inLine)
        # TextLineMetrics *getLineMetrics(int inLine);

        double getWidth()
        void setWidth(double inWidth)
        double getHeight()
        void setHeight(double inHeight)

        WString getHTMLText()
        void setHTMLText(const WString &inString)
        WString getText()
        void setText(const WString &inString)

        int   getLength()
        double   getTextHeight()
        double   getTextWidth()

cdef extern from "Font.h" namespace "lime::TextFormat":
    TextFormat* Create()
    TextFormat* Default()

cdef _from__text_format(TextFormat *ntf):
    from flappy.text import TextFormat
    
    tf = TextFormat()
    tf.font = WideToUTF8(ntf.font.__Get()).c_str()
    tf.size = ntf.size.__Get()
    tf.bold = ntf.bold.__Get()
    tf.color = ntf.color.__Get()
    tf.align = ntf.align.__Get()
    tf.indent = ntf.indent.__Get()
    tf.italic = ntf.italic.__Get()
    tf.underline = ntf.underline.__Get()
    tf.leading = ntf.leading.__Get()
    tf.leftMargin = ntf.leftMargin.__Get()
    tf.rightMargin = ntf.rightMargin.__Get()
    tf.target = WideToUTF8(ntf.target.__Get()).c_str()
    tf.url = WideToUTF8(ntf.url.__Get()).c_str()
    # tf.blockIndent = ntf.blockIndent.__Get()
    # tf.letterSpacing = ntf.letterSpacing.__Get()
    # tf.bullet = ntf.bullet.__Get()
    # tf.kerning = ntf.kerning.__Get()

    return tf

cdef TextFormat* _to__text_format(tf):
    cdef TextFormat* ntf = Create()

    ntf.font            = Optional[WString](UTF8ToWide(tf.font))
    ntf.size            = Optional[int](tf.size)
    ntf.bold            = Optional[bool](tf.bold)
    ntf.color           = Optional[uint32](tf.color)
    ntf.align           = Optional[TextFormatAlign](tf._align)
    ntf.indent          = Optional[int](tf.indent)
    ntf.italic          = Optional[bool](tf.italic)
    ntf.underline       = Optional[bool](tf.underline)
    ntf.leading         = Optional[int](tf.leading)
    ntf.leftMargin      = Optional[int](tf.leftMargin)
    ntf.rightMargin     = Optional[int](tf.rightMargin)
    ntf.target          = Optional[WString](UTF8ToWide(tf.target))
    ntf.url             = Optional[WString](UTF8ToWide(tf.url))
    # ntf.letterSpacing   = Optional[int](tf.letterSpacing)
    # ntf.blockIndent     = Optional[int](tf.blockIndent)
    # ntf.bullet          = Optional[bool](tf.bullet)
    # ntf.kerning         = Optional[bool](tf.kerning)

    ntf.font.Set()
    ntf.size.Set() 
    ntf.bold.Set()
    ntf.color.Set() 
    ntf.align.Set()
    ntf.indent.Set()
    ntf.italic.Set()
    ntf.underline.Set()
    ntf.leading.Set()
    ntf.leftMargin.Set()
    ntf.rightMargin.Set()
    ntf.target.Set()
    ntf.url.Set() 
    return ntf

def _get_fonts_directory():
    IF PLATFORM == 'WINDOWS':
        raise NotImplementedError
    ELIF PLATFORM == 'MAC':
        raise NotImplementedError
    ELSE:
        return '/usr/share/fonts/truetype/'

cdef class _TextField(_DisplayObject):
    cdef TextField *tf_ptr

    def __init__(self):
        self.tf_ptr = new TextField()
        self.do_ptr = <DisplayObject*>self.tf_ptr
        self.do_ptr.IncRef()
        self.created = True

    def setText(self, char *text):
        cdef WString ws = UTF8ToWide(text)
        self.tf_ptr.setText(ws)

    def getText(self):
        cdef WString ws = self.tf_ptr.getText()
        cdef string ret = WideToUTF8(ws)
        return ret.c_str()    

    def setHTMLText(self, char *text):
        cdef WString ws = UTF8ToWide(text)
        self.tf_ptr.setHTMLText(ws)

    def getHTMLText(self):
        cdef WString ws = self.tf_ptr.getHTMLText()
        cdef string ret = WideToUTF8(ws)
        return ret.c_str()

    def getBackground(self):
        return self.tf_ptr.getBackground()

    def setBackground(self, bool value):
        self.tf_ptr.setBackground(value)    

    def getBackgroundColor(self):
        return self.tf_ptr.getBackgroundColor()

    def setBackgroundColor(self, uint32 value):
        self.tf_ptr.setBackgroundColor(value)    

    def getAutoSize(self):
        return self.tf_ptr.getAutoSize()

    def setAutoSize(self, int value):
        self.tf_ptr.setAutoSize(value)    

    def getBorder(self):
        return self.tf_ptr.getBorder()

    def setBorder(self, bool value):
        self.tf_ptr.setBorder(value)

    def getBorderColor(self):
        return self.tf_ptr.getBorderColor()

    def setBorderColor(self, uint32 value):
        self.tf_ptr.setBorderColor(value)

    def getBottomScrollV(self):
        return self.tf_ptr.getBottomScrollV()    

    def getMaxScrollH(self):
        return self.tf_ptr.getMaxScrollH()    

    def getMaxScrollV(self):
        return self.tf_ptr.getMaxScrollV()

    def getScrollH(self):
        return self.tf_ptr.getScrollH()

    def setScrollH(self, int value):
        self.tf_ptr.setScrollH(value)    

    def getScrollV(self):
        return self.tf_ptr.getScrollV()

    def setScrollV(self, int value):
        self.tf_ptr.setScrollV(value)

    def getDisplayAsPassword(self):
        return self.tf_ptr.getDisplayAsPassword()

    def setDisplayAsPassword(self, bool value):
        self.tf_ptr.setDisplayAsPassword(value)

    def geMaxCharse(self):
        return self.tf_ptr.getMaxChars()

    def setMaxChars(self, int value):
        self.tf_ptr.setMaxChars(value)

    def getMultiline(self):
        return self.tf_ptr.getMultiline()

    def setMultiline(self, bool value):
        self.tf_ptr.setMultiline(value)

    def getNumLines(self):
        return self.tf_ptr.getNumLines()

    def getSelectable(self):
        return self.tf_ptr.getSelectable()

    def setSelectable(self, bool value):
        self.tf_ptr.setSelectable(value)

    def getTextColor(self):
        return self.tf_ptr.getTextColor()

    def setTextColor(self, uint32 value):
        self.tf_ptr.setTextColor(value)

    def getTextWidth(self):
        return self.tf_ptr.getTextWidth()    

    def getTextHeight(self):
        return self.tf_ptr.getTextHeight()

    def getIsInput(self):
        return self.tf_ptr.getIsInput()

    def setIsInput(self, bool value):
        self.tf_ptr.setIsInput(value)

    def getWordWrap(self):
        return self.tf_ptr.getWordWrap()

    def setWordWrap(self, value):
        self.tf_ptr.setWordWrap(value)

    def setTextFormat(self, tf, int first=-1, int last=-1):
        cdef TextFormat *ntf = _to__text_format(tf)
        self.tf_ptr.setTextFormat(ntf, first, last)
        ntf.DecRef()

    def setDefaultTextFormat(self, tf):
        cdef TextFormat *ntf = _to__text_format(tf)
        self.tf_ptr.setDefaultTextFormat(ntf)      
        ntf.DecRef()

