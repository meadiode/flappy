
from event import Event

class FocusEvent(Event):
    FOCUS_IN = "focusIn"
    FOCUS_OUT = "focusOut"
    KEY_FOCUS_CHANGE = "keyFocusChange"
    MOUSE_FOCUS_CHANGE = "mouseFocusChange"

    def __init__(self, etype, bubbles=True, cancelable=False,
                    relatedObject=None, shiftKey=None, keyCode=0,
                        direction='none'):
        Event.__init__(self, etype, bubbles, cancelable)
        self.relatedObject = relatedObject
        self.keyCode = keyCode
        self.shiftKey = shiftKey

    def clone(self):
        return FocusEvent(self.type, self.bubbles, self.cancelable, 
                            self.relatedObject, self.shiftKey, self.keyCode)

    def __str__(self):
        s = '[FocusEvent type=%s bubbles=%s cancelable=%s' \
                'relatedObject=%s shiftKey=%s keyCode=%s]' % \
                    (self.type, str(self.bubbles), str(self.cancelable), 
                        str(self.relatedObject), str(self.shiftKey), 
                            str(self.keyCode))