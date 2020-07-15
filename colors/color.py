"""
colors.base
===========
Convert colors between rgb, hsv, and hex, perform arithmetic, blend modes,
and generate random colors within boundaries.
"""
import colorsys
import random
import re


HEX_COLOR_PATTERN = '^#?([a-fA-F0-9]{2})([a-fA-F0-9]{2})([a-fA-F0-9]{2})$'
DEFAULT_COLOR = '#333333'


class Color(object):


    def __init__(self, hex_triplet=None, rgb=None, hsv=None, hls=None,
                 yiq=None):
        """Initializes a Color instance with a given argument.

        Initializes a Color instance with a giving argument, populating the
        other color standards. If none of them is present, the Color is
        initialized with the `DEFAULT_COLOR` value.

        Args:
            hex_triplet (str): A rgb color in hexadecimal format like `#ffffff`
                or `ffffff`. Both are accepted.
            rgb (tuple): A tuple with 3 `int`s within the range 0-255,
                like `(255, 255, 255)`, containing the colors for red, green
                and blue.
            hsv (tuple): A tuple with 3 `floats`s. For more information about
                the expected values, please refer to the documentation for
                Python's `colorsys`.
            hls (tuple): A tuple with 3 `floats`s. For more information about
                the expected values, please refer to the documentation for
                Python's `colorsys`.
            yiq (tuple): A tuple with 3 `floats`s. For more information about
                the expected values, please refer to the documentation for
                Python's `colorsys`.
        """

        if hex_triplet:
            self.from_hex_triplet(hex_triplet)

        elif rgb:
            self.from_rgb(rgb)

        elif hsv:
            self.from_hsv(hsv)

        elif hls:
            self.from_hls(hls)

        elif yiq:
            self.from_yiq(yiq)

        else:
            self.from_hex_triplet(DEFAULT_COLOR)


    def from_hex_triplet(self, hex_triplet):
        """Transforms a Color instance from a hex triplet.

        Transforms a Color instance from a hex triplet with format like
            `#ffffff` ou `ffffff`

        Args:
            hex_triplet (str): A rgb color in hexadecimal format like `#ffffff`
                or `ffffff`. Both are accepted.
        """

        hex_match = re.match(HEX_COLOR_PATTERN, hex_triplet)

        if(hex_match):

            self.hex_triplet = "".join(hex_match.groups()).lower()
            self.rgb = tuple(map(lambda x: int(x, base=16), hex_match.groups()))
            self._from_self_rgb()

        else:
            raise ValueError('Invalid hex color.')


    def from_rgb(self, rgb):
        """Transforms a Color instance from rgb tuple.

        Transforms a Color instance from a rgb tuple, with three `int`s, like
            `(255, 255, 255)`

        Args:
            rgb (tuple): A tuple with 3 `int`s within the range 0-255,
                like `(255, 255, 255)`, containing the colors for red, green
                and blue.
        """
        for c in rgb:
            if c < 0 or c > 255:
                raise ValueError('Color values must be between 0 and 255')

        self.rgb = rgb
        self._from_self_rgb()


    def from_hsv(self, hsv):

        h, s, v = hsv

        if s > 1:
            raise ValueError('Saturation has to be less than 1')
        if v > 1:
            raise ValueError('Value has to be less than 1')

        # Hue can safely circle around 1
        if h >= 1:
            h -= int(h)

        self.rgb = hsv_to_rgb(*hsv)
        self._from_self_rgb()


    def from_hls(self, hls):
        self.rgb = hls_to_rgb(*hls)
        self._from_self_rgb()


    def from_yiq(self, yiq):
        self.rgb = hsv_to_rgb(*yiq)
        self._from_self_rgb()


    def _from_self_rgb(self):
        if self.rgb:
            #self.rgb_fraction = tuple(map(lambda x: x / 255.0, self.rgb))
            self.rgb_fraction = tuple((x / 255.0) for x in self.rgb)
            self.hex_triplet = "".join(map(lambda color: format(color, "x"),
                                           self.rgb))
            self.hsv = colorsys.rgb_to_hsv(*self.rgb_fraction)
            self.hls = colorsys.rgb_to_hls(*self.rgb_fraction)
            self.yiq = colorsys.rgb_to_yiq(*self.rgb_fraction)

            self.color = self.rgb

        else:
            return None

    def randomize(self):
        """Transforms the Color instance in a random color.  """

        rand_rgb = tuple(random.randrange(256) for _ in range(3))
        self.from_rgb(rand_rgb)


    def multiply(self, other):

        rgb = tuple(((x * y) /255.0) for x, y in zip(self.rgb, other.rgb))

        return Color(rgb=rgb)

    __mul__ = multiply

    def add(self, other):

        rgb = tuple((x + y) for x, y in zip(self.rgb, other.rgb))
        return Color(rgb=rgb)

    __add__ = add

    def divide(self, other):

        rgb = tuple((x / float(y)) for x, y in zip(self.rgb, other.rgb))
        return Color(rgb=rgb)

    __div__ = divide


    def subtract(self, other):

        rgb = tuple(max(255, (x - y)) for x, y in zip(self.rgb, other.rgb))

        return Color(rgb=rgb)

    __sub__ = subtract


    def screen(self, other):

        rgb = tuple((255-(((255-x)*(255-y))/255.0)) for x, y in zip(self.rgb,
                                                                    other.rgb))

        return Color(rgb=rgb)


    def difference(self, other):

        rgb = tuple(abs(x - y) for x, y in zip(self.rgb, other.rgb))
        return Color(rgb=rgb)

    def overlay(self, other):

        return self.screen(self.multiply(other))

    def invert(self):

        return self.difference(Color(rgb=(255, 255, 255)))

    # TODO: make color __hash__able and use it for comparisons
    #       use its 24 bits for this
    def __eq__(self, other):
        is_equal = tuple((x == y) for x, y in zip(self.rgb, other.rgb))

        return all(is_equal)

    def __contains__(self, item):
        return item in self.color

    def __ne__(self, other):
        return not self.__eq__(other)

    def __iter__(self):
        """ Treat the color object as an iterable to iterate over color values
        Allows mapping such as:

        >>> list(rgb(100, 50, 0))
        [100, 50, 0]
        >>> for i in rgb(100, 50, 0): print i
        100
        50
        0
        """
        return iter(self.color)


    def __int__(self)

        R, G, B = self.rgb

        self.numeric = R<<16 | G<<8 | B

        return self.numeric
#       what is a color lenght? :)
#     def __len__(self):
#         return len(self.color)


    def __str__(self):

        hex_triplet = self.hex_triplet
        return f'#{hex_triplet}'

    def __repr__(self):

        hex_triplet = self.hex_triplet
        rgb = self.rgb
        base = f'<Color `#{hex_triplet}`; rgb {rgb}>'

        return base


class ColorWheel(object):
    """ Iterate random colors disributed relatively evenly
    around the color wheel.

    >>> from colors import ColorWheel
    >>> wheel = ColorWheel()
    >>> print '#%s' % wheel.next().hex
    #cc8b00
    >>> wheel = ColorWheel(start=0.2)
    >>> print '#%s' % wheel.next().hex
    #00cc26
    >>> print '#%s' % wheel.next().hex
    #009ecc
    """
    def __init__(self, start=0):
        # A 1.1 shift is identical to 0.1
        if start >= 1:
            start -= 1
        self._phase = start

    def __iter__(self):
        return self

    def next(self):
        shift = (random_.random() * 0.1) + 0.1
        self._phase += shift
        if self._phase >= 1:
            self._phase -= 1
        return HSVColor(self._phase, 1, 0.8)


