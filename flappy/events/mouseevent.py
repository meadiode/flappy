# -*- coding: utf-8 -*-

from event import Event

class MouseEvent(Event):

    DOUBLE_CLICK      = "doubleClick"
    CLICK             = "click"
    MIDDLE_CLICK      = "middleClick"
    MIDDLE_MOUSE_DOWN = "middleMouseDown"
    MIDDLE_MOUSE_UP   = "middleMouseUp"
    MOUSE_DOWN        = "mouseDown"
    MOUSE_MOVE        = "mouseMove"
    MOUSE_OUT         = "mouseOut"
    MOUSE_OVER        = "mouseOver"
    MOUSE_UP          = "mouseUp"
    MOUSE_WHEEL       = "mouseWheel"
    RIGHT_CLICK       = "rightClick"
    RIGHT_MOUSE_DOWN  = "rightMouseDown"
    RIGHT_MOUSE_UP    = "rightMouseUp"
    ROLL_OUT          = "rollOut"
    ROLL_OVER         = "rollOver"

    efLeftDown        = 0x0001
    efShiftDown       = 0x0002
    efCtrlDown        = 0x0004
    efAltDown         = 0x0008
    efCommandDown     = 0x0010

    efMiddleDown      = 0x0020
    efRightDown       = 0x0040

    efLocationRight   = 0x4000
    efPrimaryTouch    = 0x8000
    efNoNativeClick   = 0x10000


    @staticmethod
    def _create(etype, e, localpoint, target):
        flags = e.flags
        ret = MouseEvent(etype, bubbles=True, cancelable=False, 
            localX=localpoint.x, localY=localpoint.y, relatedObject=None, 
                ctrlKey=(flags & MouseEvent.efCtrlDown) != 0,
                    altKey=(flags & MouseEvent.efAltDown) != 0,
                        shiftKey=(flags & MouseEvent.efShiftDown) != 0,
                            buttonDown=(flags & MouseEvent.efLeftDown) != 0)
        ret.stageX = e.x
        ret.stageY = e.y
        ret.target = target
        return ret

    def __init__(self, etype, bubbles=True, cancelable=False, 
                    localX=0.0, localY=0.0, relatedObject=None, 
                        ctrlKey=False, altKey=False, shiftKey=False, 
                            buttonDown=False, delta=0, commandKey=False, 
                                clickCount=0):
        Event.__init__(self, etype, bubbles, cancelable=True)
        self.localX = float(localX)
        self.localY = float(localY)
        self.relatedObject = relatedObject
        self.ctrlKey = ctrlKey
        self.altKey = altKey
        self.shiftKey = shiftKey
        self.buttonDown = buttonDown
        self.delta = delta
        self.commandKey = commandKey
        self.clickCount = clickCount
        self.stageX = 0.0
        self.stageY = 0.0

    def clone(self):
        return MouseEvent(self.type, self.bubbles, self.cancelable, 
                            self.localX, self.localY, self.relatedObject, 
                                self.ctrlKey, self.altKey, self.shiftKey, 
                                    self.buttonDown, self.delta, 
                                        self.commandKey, self.clickCount)

    def __str__(self):
        s = "[MouseEvent type=%s bubbles=%s cancelable=%s" % \
                (self.type, str(self.bubbles), str(self.cancelable))
        s += "localX=%s localY=%s relatedObject=%s ctrlKey=%s" % \
                (str(self.localX), str(self.localY), str(self.relatedObject), 
                                                            str(self.ctrlKey))
        s += "altKey=%s shiftKey=%s buttonDown=%s delta=%s]" % \
                (str(self.altKey), str(self.shiftKey), str(self.buttonDown), 
                                                            str(self.delta))
        return s

    def _create_similar(self, etype, related=None, target=None):
        ret = MouseEvent(etype, 
            self.bubbles, self.cancelable, self.localX, self.localY, 
                self.relatedObject if related == None else related, 
                    self.ctrlKey, self.altKey, self.shiftKey, self.buttonDown, 
                        self.delta, self.commandKey, self.clickCount)
        ret.stageX = self.stageX
        ret.stageY = self.stageY
        if target != None:
            ret.target = target

        return ret