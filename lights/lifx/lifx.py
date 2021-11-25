from lifxlan import LifxLAN
from lightDevice import LightSystem, LightDevice


class LifxSystem(LightSystem):
    def __init__(self, transition_time=0):
        self._lifxlan = LifxLAN()
        self._transition_time = transition_time

    def set_transition_time(self, transition_time):
        self._transition_time = transition_time

    def discover_lights(self):
        lights = self._lifxlan.get_color_lights()
        return [LifxLight(light, self._transition_time) for light in lights]

    def set_color_all_lights(self, color):
        self._lifxlan.set_color_all_lights(color, self._transition_time, True)


class LifxLight(LightDevice):
    def __init__(self, light, transition_time):
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
