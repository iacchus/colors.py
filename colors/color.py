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

        hex_match = re.match(HEX_COLOR_PATTERN, hex_triplet)

        if(hex_match):

            self.hex_triplet = "".join(hex_match.groups()).lower()
            self.rgb = tuple(map(lambda x: int(x, base=16), hex_match.groups()))
            self._from_self_rgb()

        else:
            raise ValueError('Invalid hex color.')


    def from_rgb(self, rgb):

        for c in rgb:
            if c < 0 or c > 255:
                raise ValueError('Color values must be between 0 and 255')

        self.rgb = rgb
        self._from_self_rgb()


    def from_hsv(self, hsv):

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
            self.rgb_fraction = tuple(map(lambda x: x / 255.0, self.rgb))
            self.hex_triplet = "".join(map(lambda x: format(x, "x"), self.rgb))
            self.hsv = colorsys.rgb_to_hsv(*self.rgb_fraction)
            self.hls = colorsys.rgb_to_hls(*self.rgb_fraction)
            self.yiq = colorsys.rgb_to_yiq(*self.rgb_fraction)

            self.color = self.rgb

        else:
            return None

    def randomize(self):
        rand_rgb = tuple(random.randrange(256) for _ in range(3))
        self.from_rgb(rand_rgb)


    def multiply(self, other):
        #self_rgb = self.rgb
        #other_rgb = other.rgb
        #return RGBColor(
        return Color(
            rgb=tuple(map(lambda x, y: ((x * y) / 255.0),
                          zip(self.rgb, other.rgb)))
        )
#         return Color(
#             self_rgb.red * other_rgb.red / 255.0,
#             self_rgb.green * other_rgb.green / 255.0,
#             self_rgb.blue * other_rgb.blue / 255.0
#         )

    __mul__ = multiply

    def add(self, other):
#         self_rgb = self.rgb
#         other_rgb = other.rgb
        return Color(
            rgb=tuple(map(lambda x, y: min(255, (x + y)),
                          zip(self.rgb, other.rgb)))
        )
#         return RGBColor(
#             min(255, self_rgb.red + other_rgb.red),
#             min(255, self_rgb.green + other_rgb.green),
#             min(255, self_rgb.blue + other_rgb.blue),
#         )

    __add__ = add

    def divide(self, other):
        self_rgb = self.rgb
        other_rgb = other.rgb
        if 0 in other_rgb:
            raise ZeroDivisionError

        return Color(
            rgb=tuple(map(lambda x, y: x / float(y)),
                          zip(self.rgb, other.rgb)))
        )

#         return RGBColor(
#             self_rgb.red / float(other_rgb.red),
#             self_rgb.green / float(other_rgb.green),
#             self_rgb.blue / float(other_rgb.blue),
#         )

    __div__ = divide

    def subtract(self, other):
#         self_rgb = self.rgb
#         other_rgb = other.rgb
        return Color(
            rgb=tuple(map(lambda x, y: max(255, (x - y)),
                          zip(self.rgb, other.rgb)))
        )
#         return RGBColor(
#             max(0, (self_rgb.red - other_rgb.red)),
#             max(0, (self_rgb.green - other_rgb.green)),
#             max(0, (self_rgb.blue - other_rgb.blue)),
#         )

    __sub__ = subtract

    def screen(self, other):
        self_rgb = self.rgb
        other_rgb = other.rgb

        return Color(
            rgb=tuple(map(lambda x, y: max(255, (x - y)),
                          zip(self.rgb, other.rgb)))
        )
       
        return RGBColor(
            255 - (((255 - self_rgb.red) * (255 - other_rgb.red)) / 255.0),
            255 - (((255 - self_rgb.green) * (255 - other_rgb.green)) / 255.0),
            255 - (((255 - self_rgb.blue) * (255 - other_rgb.blue)) / 255.0),
        )

    def difference(self, other):
        self_rgb = self.rgb
        other_rgb = other.rgb
        return RGBColor(
            abs(self_rgb.red - other_rgb.red),
            abs(self_rgb.green - other_rgb.green),
            abs(self_rgb.blue - other_rgb.blue),
        )

    def overlay(self, other):
        return self.screen(self.multiply(other))

    def invert(self):
        return self.difference(RGBColor(255, 255, 255))

    def __eq__(self, other):
        self_rgb = self.rgb
        other_rgb = other.rgb
        return self_rgb.red == other_rgb.red \
           and self_rgb.green == other_rgb.green \
           and self_rgb.blue == other_rgb.blue

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

    def __len__(self):
        return len(self.color)

    def __str__(self):
        return ', '.join(map(str, self.color))

#     def __repr__(self):
#         base = u'<%s %s>'
#         properties = [
#             '%s: %s' % (prop, getattr(self, prop)) \
#                 for prop in self.Meta.properties
#         ]
#         return base % (self.__class__.__name__, ', '.join(properties))


# class HSVColor(Color):
#     """ Hue Saturation Value """
# 
#     def __init__(self, h=0, s=0, v=0):
#         if s > 1:
#             raise ValueError('Saturation has to be less than 1')
#         if v > 1:
#             raise ValueError('Value has to be less than 1')
# 
#         # Hue can safely circle around 1
#         if h >= 1:
#             h -= int(h)
# 
#         self._color = h, s, v
# 
#     @property
#     def rgb(self):
#         return RGBColor(*map(lambda c: c * 255, colorsys.hsv_to_rgb(*self._color)))
# 
#     @property
#     def hsv(self):
#         return self
# 
#     class Meta:
#         properties = ('hue', 'saturation', 'value')


# class RGBColor(Color):
#     """ Red Green Blue """
# 
#     def __init__(self, r=0, g=0, b=0):
#         self._color = r, g, b
#         for c in self._color:
#             if c < 0 or c > 255:
#                 raise ValueError('Color values must be between 0 and 255')
# 
#     @property
#     def rgb(self):
#         return self
# 
#     @property
#     def hsv(self):
#         return HSVColor(*colorsys.rgb_to_hsv(*map(lambda c: c / 255.0, self._color)))
# 
#     class Meta:
#         properties = ('red', 'green', 'blue')


# class HexColor(RGBColor):
#     """ Typical 6 digit hexadecimal colors.
# 
#     Warning: accuracy is lost when converting a color to hex
#     """
# 
#     def __init__(self, hex='000000'):
#         if len(hex) != 6:
#             raise ValueError('Hex color must be 6 digits')
# 
#         hex = hex.lower()
#         if not set(hex).issubset(HEX_RANGE):
#             raise ValueError('Not a valid hex number')
# 
#         self._color = hex[:2], hex[2:4], hex[4:6]
# 
#     @property
#     def rgb(self):
#         return RGBColor(*[int(c, 16) for c in self._color])
# 
#     @property
#     def hsv(self):
#         return self.rgb.hsv
# 
#     @property
#     def hex(self):
#         return self
# 
#     def __str__(self):
#         return '%s%s%s' % self._color


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


# def random():  # This name might be a bad idea?
#     """ Generate a random color.
# 
#     >>> from colors import random
#     >>> random()
#     <HSVColor hue: 0.310089903395, saturation: 0.765033516918, value: 0.264921257867>
#     >>> print '#%s' % random().hex
#     #ae47a7
# 
#     """
#     return HSVColor(random_.random(), random_.random(), random_.random())

# Simple aliases
# rgb = RGBColor  # rgb(100, 100, 100), or rgb(r=100, g=100, b=100)
# hsv = HSVColor  # hsv(0.5, 1, 1), or hsv(h=0.5, s=1, v=1)
# hex = HexColor  # hex('BADA55')


# """
# colors.primary
# ==============
# """
# 
# black = Color(0, 0, 0)
# white = Color(255, 255, 255)
# red = Color(255, 0, 0)
# green = Color(0, 255, 0)
# blue = Color(0, 0, 255)
# 
# 
# """
# colors.rainbow
# ==============
# ROYGBIV!
# """
# 
# red = Color(255, 0, 0)
# orange = Color(255, 165, 0)
# yellow = Color(255, 255, 0)
# green = Color(0, 128, 0)
# blue = Color(0, 0, 255)
# indigo = Color(75, 0, 130)
# violet = Color(238, 130, 238)