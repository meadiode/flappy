Flappy
======


Flappy (the name stands for FLash-like APi for PYthon) is a cross-platform graphics/media library with the API very similar to the Adobe Flash API. Flappy is built on top of the SDL2_ library and a slightly modified subset of c/c++ code from the OpenFL-Lime_ project.

Features
--------
* lol
* lol

Quick example
-------------

.. code-block::

    import flappy
    from flappy.display import Sprite
    from flappy.events import MouseEvent

    class Example(Sprite):

        def __init__(self):
            super(Example, self).__init__()

            circle = Sprite()
            circle.graphics.lineStyle(4)
            circle.graphics.beginFill(0xff8000)
            circle.graphics.drawCircle(200, 200, 100)
            circle.graphics.endFill()
            self.addChild(circle)

            circle.addEventListener(MouseEvent.CLICK, self.on_circle_click)

        def on_circle_click(self, event):
            print 'YAY!'

    if __name__ == '__main__':
        flappy.start(Example, width=400, height=400, title='Example')

This code draws a black-outlined orange circle inside a window sized 400x400 pixels. Each time you click on that circle you'll see the string "YAY!" in console output.

.. image:: http://i.imgur.com/wqtfqz2.png

For the comparison, here is the code in ActionScript 3 which does the same:

.. code-block::

    package {
        [SWF (width="400", height="400")]
        
        import flash.display.Sprite;
        import flash.events.MouseEvent;
        
        public class Example extends Sprite
        {
            public function Example()
            {
                    var circle:Sprite = new Sprite();
                    circle.graphics.lineStyle(4);
                    circle.graphics.beginFill(0xff8000);
                    circle.graphics.drawCircle(200, 200, 100);
                    circle.graphics.endFill();
                    
                    this.addChild(circle);
                    
                    circle.addEventListener(MouseEvent.CLICK, on_circle_click);             
            }
            
            public function on_circle_click(event: MouseEvent):void{
                trace('YAY!');
            }
        }
    }

.. _SDL2: http://libsdl.org
.. _OpenFL-Lime: https://github.com/openfl/lime