from abc import ABC, abstractmethod
from .color import Color


class LightSystem(ABC):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'set_transition_time')
                and callable(subclass.set_transition_time)
                and hasattr(subclass, 'discover_lights')
                and callable(subclass.discover_lights)
                and hasattr(subclass, 'set_color_all_lights')
                and callable(subclass.set_color_all_lights))

    @abstractmethod
    def discover_lights(self):
        """Discover the lights and groups in this LightSystem."""
        raise NotImplementedError

    @abstractmethod
    def set_transition_time(self, transition_time: int):
        """Set how long it takes in milliseconds for colors to transition."""
        raise NotImplementedError

    @abstractmethod
    def set_color(self, color: Color):
        """Set the color of all the lights in the LightSystem."""
        raise NotImplementedError


class LightGroup(ABC):
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

    @abstractmethod
    def turn_on(self):
        """Turn on the lights in this group."""
        raise NotImplementedError

    @abstractmethod
    def turn_off(self):
        """Turn off the lights in this group."""
        raise NotImplementedError

    @abstractmethod
    def set_transition_time(self, transition_time: int):
        """Set how long it takes in milliseconds for colors to transition."""
        raise NotImplementedError

    @abstractmethod
    def set_color(self, color: Color):
        """Set the color of this light."""
        raise NotImplementedError


class LightDevice(ABC):
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

    @abstractmethod
    def turn_on(self):
        """Turn on this light."""
        raise NotImplementedError

    @abstractmethod
    def turn_off(self):
        """Turn off the light."""
        raise NotImplementedError

    @abstractmethod
    def set_transition_time(self, transition_time: int):
        """Set how long it takes in milliseconds for colors to transition."""
        raise NotImplementedError

    @abstractmethod
    def set_color(self, color: Color):
        """Set the color of this light."""
        raise NotImplementedError
