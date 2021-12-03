from lifxlan import LifxLAN
from firelight.interfaces.light import LightSystem, LightGroup, LightDevice
from firelight.interfaces.color import HLSColor

SMOOTHING_COEFFICIENT = 0.80


class LifxSystem(LightSystem):
    def __init__(self, transition_time=300, smoothing=True):
        self._lifxlan = LifxLAN()
        self._transition_time = transition_time
        self._smoothing = smoothing
        self._groups = []
        self._lights = {}
        if smoothing:
            self._prev_l = 1.0
        self.discover_lights()

    def set_transition_time(self, transition_time):
        self._transition_time = transition_time

    def discover_lights(self):
        lights = self._lifxlan.get_color_lights()
        for light in lights:
            self._lights[light.get_label()] = light
            group = light.get_group()
            if group not in self._groups:
                self._groups.append(group)
        print(self._groups)

    def set_color(self, color: HLSColor):
        h, l, s = color.values()

        # Smooth luminance, otherwise we will get some "shakey" light effects
        if self._smoothing:
            l = self._prev_l*SMOOTHING_COEFFICIENT + \
                l*(1.0 - SMOOTHING_COEFFICIENT)
            self._prev_l = l

        self._lifxlan.set_color_all_lights(
            [65535*h, 65535*s, 65535*l, 3500], self._transition_time, True)

    def list_groups(self):
        return [group for group in self._groups]

    def get_light_group(self, name: str):
        if name not in self._groups:
            print("Group " + name + " could not be found.")
        group = self._lifxlan.get_devices_by_group(name)
        return LifxGroup(group, self._transition_time)


class LifxGroup(LightGroup):
    def __init__(self, group, transition_time=300, smoothing=True):
        self._group = group
        self._transition_time = transition_time
        self._smoothing = smoothing
        if smoothing:
            self._prev_l = 1.0

    def turn_on(self):
        self._group.set_power("on")

    def turn_off(self):
        self._group.set_power("off")

    def set_transition_time(self, transition_time):
        self._transition_time = transition_time

    def set_color(self, color):
        h, l, s = color.values()

        # Smooth luminance, otherwise we will get some "shakey" light effects
        if self._smoothing:
            l = self._prev_l*SMOOTHING_COEFFICIENT + \
                l*(1.0 - SMOOTHING_COEFFICIENT)
            self._prev_l = l

        self._group.set_color(
            [65535*h, 65535*s, 65535*l, 3500], self._transition_time, True)


class LifxLight(LightDevice):
    def __init__(self, light, transition_time=300):
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
