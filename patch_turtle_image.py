from turtle import TurtleScreenBase
from PIL import ImageTk

@staticmethod
def _image(filename):
    return ImageTk.PhotoImage(file=filename)

TurtleScreenBase._image = _image

# If all you care about is screen.bgpic(), you can ignore what follows.

from turtle import Shape, TurtleScreen, TurtleGraphicsError
from os.path import isfile

# Methods shouldn't do `if name.lower().endswith(".gif")` but simply pass
# file name along and let it break during image conversion if not supported.

def register_shape(self, name, shape=None):  # call addshape() instead for original behavior
    if shape is None:
        shape = Shape("image", self._image(name))
    elif isinstance(shape, tuple):
        shape = Shape("polygon", shape)

    self._shapes[name] = shape

TurtleScreen.register_shape = register_shape

def __init__(self, type_, data=None):
    self._type = type_

    if type_ == "polygon":
        if isinstance(data, list):
            data = tuple(data)
    elif type_ == "image":
        if isinstance(data, str):
            if isfile(data):
                data = TurtleScreen._image(data) # redefinition of data type
    elif type_ == "compound":
        data = []
    else:
        raise TurtleGraphicsError("There is no shape type %s" % type_)

    self._data = data

Shape.__init__ = __init__