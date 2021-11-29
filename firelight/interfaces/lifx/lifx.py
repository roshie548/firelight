from lifxlan import LifxLAN
from firelight.interfaces.light import LightSystem, LightDevice
from firelight.interfaces.color import HLSColor

SMOOTHING_COEFFICIENT = 0.80


class LifxSystem(LightSystem):
    def __init__(self, transition_time=600, smoothing=True):
        self._lifxlan = LifxLAN()
        self._transition_time = transition_time
        self._smoothing = smoothing
        if smoothing:
            self._prev_l = 1

    def set_transition_time(self, transition_time):
        self._transition_time = transition_time

    def discover_lights(self):
        lights = self._lifxlan.get_color_lights()
        return [LifxLight(light, self._transition_time) for light in lights]

    def set_color_all_lights(self, color: HLSColor):
        h, l, s = color.values()

        # Smooth luminance, otherwise we will get some "shakey" light effects
        if self._smoothing:
            l = self._prev_l*SMOOTHING_COEFFICIENT + \
                l*(1.0 - SMOOTHING_COEFFICIENT)
            self._prev_l = l

        self._lifxlan.set_color_all_lights(
            [65535*h, 65535*s, 65535*l, 3500], self._transition_time, True)


class LifxLight(LightDevice):
    def __init__(self, light, transition_time=400):
        self._light = light
        self._transition_time = transition_time

    def turn_on(self):
        self._light.set_power("on")

    def turn_off(self):
        self._light.set_power("off")

    def set_transition_time(self, transition_time):
        self._transition_time = transition_time

    def set_color(self, color):
        self._light.set_color(color, self._transition_time, True)
