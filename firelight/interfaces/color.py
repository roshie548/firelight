from abc import ABC, abstractmethod


class Color(ABC):
    """Interface that represents color objects."""
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'to_hsv')
                and callable(subclass.to_hsv)
                and hasattr(subclass, 'to_rgb')
                and callable(subclass.to_rgb))

    @abstractmethod
    def values(self):
        """Return the values of this color.

        :rtype: tuple

        """
        raise NotImplementedError

    @abstractmethod
    def to_hls(self):
        """Return this color in HLS color space.

        :return: HLS color object.
        :rtype: HLSColor

        """
        raise NotImplementedError

    @abstractmethod
    def to_rgb(self):
        """Return this color in RGB color space.

        :return: RGB color object.
        :rtype: RGBColor

        """
        raise NotImplementedError


class RGBColor(Color):
    """Represents a color in the RGB color space.

    :param int r: Red color intensity, in the range of [0-255].
    :param int g: Green color intensity, in the range of [0-255].
    :param int b: Blue color intensity, in the range of [0-255].

    """

    def __init__(self, r: int, g: int, b: int):
        """Constructor method"""
        self._rgb = (r, g, b)

    def values(self):
        """Return the values of this color.

        :rtype: Tuple

        """
        return self._rgb

    def to_hls(self):
        """Convert RGB color to the HLS color space.
        Implementation from "HLS and HSV" wiki: https://en.wikipedia.org/wiki/HSL_and_HSV#Hue_and_chroma

        :return: Color in HLS color space.
        :rtype: HLSColor

        """
        r, g, b = self._rgb
        r, g, b = r/255, g/255, b/255
        M = max(r, g, b)
        m = min(r, g, b)
        C = M - m

        if C == 0:
            hprime = 0
        elif M == r:
            hprime = ((g - b)/C) % 6
        elif M == g:
            hprime = ((b - r)/C + 2)
        elif M == b:
            hprime = ((r - g)/C + 4)

        hue = (hprime / 6.000) % 1.00
        lum = (M + m) / 2.0

        if lum == 1 or lum == 0:
            sat = 0
        else:
            sat = C / (1 - abs(2*lum - 1))

        return HLSColor(hue, lum, sat)

    def to_rgb(self):
        """Return this object.

        :return: Color in RGB color space.
        :rtype: RGBColor

        """
        return self._rgb


class HLSColor(Color):
    """Represents a color in the HLS color space.

    :param float h: Hue, in the range of [0-1].
    :param float l: Luminance, in the range of [0-1].
    :param float s: Saturation, in the range of [0-1].

    """

    def __init__(self, h: float, l: float, s: float):
        """Constructor method"""
        self._hls = (h, l, s)

    def values(self):
        """Return the values of this color.

        :rtype: Tuple

        """
        return self._hls

    def to_hls(self):
        """Return this object.

        :return: Color in HLS color space.
        :rtype: HLSColor

        """
        return self

    def to_rgb(self):
        """Convert HLS color to the RGB color space.

        :return: Color in RGB color space.
        :rtype: RGBColor

        """
        h, l, s = self._hls
        a = s * min(l, 1 - l)

        def f(x):
            k = (x + h*12.000) % 12.0
            return l - a * max(-1, min(k - 3, 9 - k, 1))

        r, g, b = f(0)*255, f(8)*255, f(4)*255

        return RGBColor(r, g, b)
