
from flappy.geom import Rectangle
from flappy.display import DisplayObjectContainer

class Sprite(DisplayObjectContainer):

    def __init__(self, name=None):
        DisplayObjectContainer.__init__(self, name)

    def startDrag(self, lock_center=False, bounds=None):
        if self.stage:
            self.stage._start_drag(self, lock_center, bounds)

    def stopDrag(self):
        if self.stage:
            self.stage._stop_drag(self)
