Flappy
======


Flappy (the name stands for FLash-like APi for PYthon) is a cross platform multimedia library with the API very similar to the ActionScript 3 Flash API. Flappy is built on top of the SDL2_ library and a slightly modified subset of c/c++ code from the OpenFL-Lime_ project.

.. _SDL2: http://libsdl.org
.. _OpenFL-Lime: https://github.com/openfl/lime

Features
--------
* Runs on Windows, Linux, Mac OS X
* GPU accelerated
* Drawing images, text, shapes, gradients
* Tile sheet batch rendering
* Flash-like display list, display objects, containers
* User input events and other events handling and propagation
* 3D graphics support

Current status
--------------
* Alpha version
* No Python 3.x support
* No sound playing

Install binary package
----------------------
In Mac or Linux, try:
::
    easy_install flappy

For windows, download the installer (one of Flappy-***.win32.exe files) here_

.. _here: http://pypi.python.org/pypi/Flappy#downloads

Build from source
-----------------
To build Flappy, Cython_ 0.19.1 or above is required. 
.. _Cython: http://cython.org/#download

Also the following libraries needed:
* SDL2
* freetype 2
* libpng 1.6
* libjpeg 6b

You can either install development versions of these libraries to your system (or already have them installed), and build and install Flappy like this:
::
    
    python setup.py install

Or you can clone this repository_ to the same directory as Flappy's source directory and build and install with this command:
::
    
    python setup.py build_extensions_with_waf --use-prebuilt-libs install

.. _repository: https://github.com/pyronimous/flappy_prebuilt_dependencies

Quick example
-------------
This code draws a black-outlined orange circle inside a window sized 400x400 pixels. Each time you click on that circle you'll see the string "YAY!" in console output:

::

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

.. image:: http://i.imgur.com/wqtfqz2.png

For the comparison, here is the code_ in ActionScript 3 which does the same.
.. _code: https://gist.github.com/pyronimous/9588523
    

Help
----
For now, documentation is a stub. But you can take a look at `ActionScript3 API reference for Flash`_. Classes and method in packages flappy.display, flappy.events, flappy.geom, flappy.text are very similar to the classes and methods in Flash's corresponding packages.
.. _`ActionScript3 API reference for Flash`_: http://help.adobe.com/en_US/FlashPlatform/reference/actionscript/3/

Also, see samples:
.. image:: http://i.imgur.com/VVUFH8f.png
