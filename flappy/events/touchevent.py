# encoding: utf-8

from event import Event
from mouseevent import MouseEvent

class TouchEvent(MouseEvent):

    TOUCH_BEGIN       = "touchBegin"
    TOUCH_END         = "touchEnd"
    TOUCH_MOVE        = "touchMove"
    TOUCH_OUT         = "touchOut"
    TOUCH_OVER        = "touchOver"
    TOUCH_ROLL_OUT    = "touchRollOut"
    TOUCH_ROLL_OVER   = "touchRollOver"
    TOUCH_TAP         = "touchTap"
    TOUCH_DOUBLE_TAP  = "touchDoubleTap"    

    @staticmethod
    def _create(etype, e, local, target, sizeX, sizeY):
        flags = e.flags
        evt = TouchEvent(etype, 
            bubbles=True, cancelable=False, localX=local.x, localY=local.y, 
                sizeX=sizeX, sizeY=sizeY, relatedObject=None, 
                    ctrlKey=(flags & MouseEvent.efCtrlDown) != 0,
                        altKey=(flags & MouseEvent.efAltDown) != 0,
                            shiftKey=(flags & MouseEvent.efShiftDown) != 0,
                            buttonDown=(flags & MouseEvent.efLeftDown) != 0)
        evt.stageX = e.x
        evt.stageY = e.y
        evt.target = target
        return evt

    def __init__(self, etype, bubbles=True, cancelable=False, 
                    localX=0.0, localY=0.0, sizeX=1.0, sizeY=1.0,
                        relatedObject=None, ctrlKey=False, altKey=False, 
                            shiftKey=False, buttonDown=False, delta=0, 
                                commandKey=False, clickCount=0):
        MouseEvent.__init__(self, etype, bubbles, cancelable, localX, 
                                localY, relatedObject, ctrlKey, altKey, 
                                    shiftKey, buttonDown, delta, commandKey, 
                                        clickCount)

        self.touchPointID = 0
        self.isPrimaryTouchPoint = True
        self.sizeX = sizeX
        self.sizeY = sizeY

    def _create_similar(self, etype, related=None, target=None):
        ret = TouchEvent(
            etype, self.bubbles, self.cancelable, 
                self.localX, self.localY, self.sizeX, self.sizeY,
                    self.relatedObject if related == None else related, 
                        self.ctrlKey, self.altKey, self.shiftKey,
                            self.buttonDown, self.delta, self.commandKey, 
                                self.clickCount)
        ret.touchPointID = self.touchPointID
        ret.isPrimaryTouchPoint = self.isPrimaryTouchPoint  
        ret.stageX = self.stageX 
        ret.stageY = self.stageY
        if target is not None:
            ret.target = target
        return ret
