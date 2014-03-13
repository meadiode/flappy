
from flappy._core import _TextField 
from flappy.display import InteractiveObject

class TextFieldType(object):
    DYNAMIC = 0
    INPUT   = 1


class AntiAliasType(object):
    ADVANCED = 0
    NORMAL   = 1


class TextFieldAutoSize(object):
    CENTER  = 0
    LEFT    = 1
    NONE    = 2
    RIGHT   = 3 


class TextField(_TextField, InteractiveObject):
    def __init__(self, name=None):
        InteractiveObject.__init__(self, name)
        self._children = []

    def _native_init(self):
        _TextField.__init__(self)

    def appendText(self, new_text):
        self.text = self.text + new_text
    
#text
    @property
    def text(self):
        return self.getText()

    @text.setter
    def text(self, value):
        self.setText(value)

#background
    @property
    def background(self):
        return self.getBackground()

    @background.setter
    def background(self, value):
        self.setBackground(value)

#backgroundColor
    @property
    def backgroundColor(self):
        return self.getBackgroundColor()

    @backgroundColor.setter
    def backgroundColor(self, value):
        self.setBackgroundColor(value)

#autoSize
    @property 
    def autoSize(self):
        return self.getAutoSize()

    @autoSize.setter
    def autoSize(self, value):
        self.setAutoSize(value)

#border
    @property
    def border(self):
        return self.getBorder()
    
    @border.setter
    def border(self, value):
        self.setBorder(value)

#borderColor
    @property
    def borderColor(self):
        return self.getBorderColor()
    
    @borderColor.setter
    def borderColor(self, value):
        self.setBorderColor(value)

#bottomScrollV
    @property
    def bottomScrollV(self):
        return self.getBottomScrollV()

#password
    @property
    def displayAsPassword(self):
        return self.getDisplayAsPassword()
    
    @displayAsPassword.setter
    def displayAsPassword(self, value):
        self.setDisplayAsPassword(value)

#htmlText
    @property
    def htmlText(self):
        return self.getHTMLText()
    
    @htmlText.setter
    def htmlText(self, value):
        self.setHTMLText(value)

#maxchars
    @property
    def maxChars(self):
        return self.getMaxChars()
    
    @maxChars.setter
    def maxChars(self, value):
        self.setMaxChars(value)

#maxScrollH(V)
    @property
    def maxScrollH(self):
        return self.getMaxScrollH()

    @property
    def maxScrollV(self):
        return self.getMaxScrollV()

#multiline
    @property
    def multiline(self):
        return self.getMultiline()
    
    @multiline.setter
    def multiline(self, value):
        self.setMultiline(value)

#numlines
    @property
    def numLines(self):
        return self.getNumLines()

#scroll 
    @property
    def scrollH(self):
        return self.getScrollH()
   
    @scrollH.setter
    def scrollH(self, value):
        self.setScrollH(value)

    @property
    def scrollV(self):
        return self.getScrollV()
    
    @scrollV.setter
    def scrollV(self, value):
        self.setScrollV(value)

#selectable
    @property
    def selectable(self):
        return self.getSelectable()
    
    @selectable.setter
    def selectable(self, value):
        self.setSelectable(value)

#color
    @property
    def textColor(self):
        return self.getTextColor()
    
    @textColor.setter
    def textColor(self, value):
        self.setTextColor(value)

#width/height
    @property
    def textWidth(self):
        return self.getTextWidth()
    
    @property
    def textHeight(self):
        return self.getTextHeight()

    @property 
    def width(self):
        return self.getWidth()

    @width.setter
    def width(self, value):
        self.setWidth(value)

    @property 
    def height(self):
        return self.getHeight()        

    @height.setter
    def height(self, value):
        self.setHeight(value)


#type: input/non-input
    @property
    def type(self):
        if self.getIsInput():
            return TextFieldType.INPUT
        return TextFieldType.DYNAMIC

    @type.setter
    def type(self, value):
        if value == TextFieldType.INPUT:
            self.setIsInput(True)
        else:
            self.setIsInput(False)

    @property
    def isInput(self):
        return self.getIsInput()
    
    @isInput.setter
    def isInput(self, value):
        self.setIsInput(value)

#length
    @property
    def length(self):
        return len(self.text)

    @property
    def defaultTextFormat(self):
        raise NotImplementedError
    
    @defaultTextFormat.setter
    def defaultTextFormat(self, value):
        self.setDefaultTextFormat(value)

