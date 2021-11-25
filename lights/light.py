import abc
from color import Color


class LightSystem(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'set_transition_time') and
                callable(subclass.set_transition_time)
                and hasattr(subclass, 'discover_lights')
                and callable(subclass.discover_lights)
                and hasattr(subclass, 'set_color_all_lights')
                and callable(subclass.set_color_all_lights))

    @abc.abstractmethod
    def discover_lights(self):
        """Discover the lights in this LightSystem and return them in an array."""
        raise NotImplementedError

    @abc.abstractmethod
    def set_transition_time(self, transition_time: int):
        """Set how long it takes in milliseconds for colors to transition."""
        raise NotImplementedError

    @abc.abstractmethod
    def set_color_all_lights(self, color: Color):
        """Set the color of all the lights in the LightSystem."""
        raise NotImplementedError


class LightDevice(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'turn_on')
                and callable(subclass.turn_on)
                and hasattr(subclass, 'turn_off')
                and callable(subclass.turn_off)
                and hasattr(subclass, 'set_transition_time')
                and callable(subclass.set_transition_time)
                and hasattr(subclass, 'set_color')
                and callable(subclass.set_color))

    @abc.abstractmethod
    def turn_on(self):
        """Turn on this light"""
        raise NotImplementedError

    @abc.abstractmethod
    def turn_off(self):
        """Turn off the light"""
        raise NotImplementedError

    @abc.abstractmethod
    def set_transition_time(self, transition_time: int):
        """Set how long it takes in milliseconds for colors to transition."""
        raise NotImplementedError

    @abc.abstractmethod
    def set_color(self, color: Color):
        """Set the color of this light"""
        raise NotImplementedError
