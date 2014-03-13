
from flappy.display import DisplayObject


class InteractiveObject(DisplayObject):

    def __init__(self, name=None):
        DisplayObject.__init__(self, name)

        self.doubleClickEnabled = False

    def requestSoftKeyboard(self):
        raise NotImplementedError

    @property
    def mouseEnabled(self):
        return self.getMouseEnabled()

    @mouseEnabled.setter
    def mouseEnabled(self, value):
        self.setMouseEnabled(value)    

    @property
    def moveForSoftKeyboard(self):
        raise NotImplementedError

    @moveForSoftKeyboard.setter
    def moveForSoftKeyboard(self, value):
        raise NotImplementedError    

    @property
    def needsSoftKeyboard(self):
        raise NotImplementedError

    @needsSoftKeyboard.setter
    def needsSoftKeyboard(self, value):
        raise NotImplementedError
