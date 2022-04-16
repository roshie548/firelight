from openrgb import OpenRGBClient,utils
from firelight.interfaces.light import LightSystem, LightGroup, LightDevice
from firelight.interfaces.color import HLSColor
import time

SMOOTHING_COEFFICIENT = 0.8
group_names = {
    'keyboard': utils.DeviceType.KEYBOARD,
    'mousemat': utils.DeviceType.MOUSEMAT,
    'mouse': utils.DeviceType.MOUSE
}


class OpenRGBSystem(LightSystem):
    def __init__(self, transition_time=300, smoothing=True):
        self._openrgb = OpenRGBClient('localhost', 6742)
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
        lights = self._openrgb.devices
        for light in lights:
            self._lights[light.id] = light
            light.set_custom_mode()
            group = [group_name for group_name, enum in group_names.items() if enum == light.type][0]
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

        smoothColor = HLSColor(h, l, s)
        rgb = smoothColor.to_rgb()

        for device in self._lights:
            self._lights[device]._set_device_color(utils.RGBColor(
                int(rgb.values()[0]), int(rgb.values()[1]), int(rgb.values()[2])
            ))

    def list_groups(self):
        return [group for group in self._groups]

    def get_light_group(self, name: str):
        if name not in self._groups:
            print("Group " + name + " could not be found.")
        group = self._openrgb.get_devices_by_type(group_names[name])
        return OpenRGBGroup(group, self._transition_time)


class OpenRGBGroup(LightGroup):
    def __init__(self, group, transition_time=300, smoothing=True):
        self._group = group
        self._transition_time = transition_time
        self._smoothing = smoothing
        if smoothing:
            self._prev_l = 1.0

    def turn_on(self):
        for device in _group:
            device._set_device_color(utils.RGBColor(255, 255, 255))

    def turn_off(self):
        for device in _group:
            device.off()

    def set_transition_time(self, transition_time):
        self._transition_time = transition_time

    def set_color(self, color):
        h, l, s = color.values()

        # Smooth luminance, otherwise we will get some "shakey" light effects
        if self._smoothing:
            l = self._prev_l*SMOOTHING_COEFFICIENT + \
                l*(1.0 - SMOOTHING_COEFFICIENT)
            self._prev_l = l

        smoothColor = HLSColor(h, l, s)
        rgb = smoothColor.to_rgb()

        for device in self._group:
            device._set_device_color(utils.RGBColor(
                int(rgb.values()[0]), int(rgb.values()[1]), int(rgb.values()[2])
            ))

class OpenRGBLight(LightDevice):
    def __init__(self, light, transition_time=300):
        self._light = light
        self._transition_time = transition_time

    def turn_on(self):
        self._light._set_device_color(utils.RGBColor(255, 255, 255))

    def turn_off(self):
        self._light.off()

    def set_transition_time(self, transition_time):
        self._transition_time = transition_time

    def set_color(self, color):
        self._light.set_device_color(color, self._transition_time, True)
