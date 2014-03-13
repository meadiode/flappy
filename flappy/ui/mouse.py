# encoding: utf-8

from flappy.display import Stage

class Mouse(object):

    @staticmethod
    def hide():
        stage = Stage._current_stage
        if stage is not None:
            stage.showCursor(False)

    @staticmethod
    def show():
        stage = Stage._current_stage
        if stage is not None:
            stage.showCursor(True)

