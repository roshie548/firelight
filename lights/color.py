import abc


class Color(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'to_hsv')
                and callable(subclass.to_hsv)
                and hasattr(subclass, 'to_rgb')
                and callable(subclass.to_rgb))

    @abc.abstractmethod
    def to_hsv(self):
        raise NotImplementedError

    @abc.abstractmethod
    def to_rgb(self):
        raise NotImplementedError


# Implementation from "HLS and HSV" wiki: https://en.wikipedia.org/wiki/HSL_and_HSV#Hue_and_chroma
class RGBColor(Color):
    def __init__(self, r, g, b):
        self.__rgb = [r, g, b]

    def to_hsv(self):
        r, g, b = self.__rgb
        M = max(r, g, b)
        m = min(r, g, b)
        C = M - m

        if C == 0:
            print("write this case")
        elif M == r:
            hprime = ((g - b)/C) % 6
        elif M == g:
            hprime = ((b - r)/C + 2)
        elif M == b:
            hprime = ((r - g)/C + 4)

        hue = (hprime / 6.000) & 1.00
        lum = (M + m) / 2.0

        if lum == 1 or lum == 0:
            sat = 0
        else:
            sat = 1 - abs(2*lum - 1)

        return hue, lum, sat

    def to_rgb(self):
        return self.__rgb
