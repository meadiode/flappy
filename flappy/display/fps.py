
from flappy.text import TextField, TextFormat, TextFieldAutoSize
from flappy.events import Event
import time

class FPS(TextField):

    def __init__(self, x=0.0, y=0.0, color=0xffff00):
        super(FPS, self).__init__()

        self.x = x
        self.y = y

        self.text = 'starting...'
        self.second = 0.0
        self.frames = 0
        self.prevtime = time.time()

        self.addEventListener(Event.ENTER_FRAME, self._on_frame, 
                                            use_weak_reference=True)

    def _on_frame(self, e):
        now = time.time()
        dt = now - self.prevtime
        self.second += dt
        if self.second >= 1.0:
            self.text = 'FPS: ' + str(self.frames)
            self.frames = 0
            self.second = 0.0
        else:
            self.frames += 1
        self.prevtime = now        
