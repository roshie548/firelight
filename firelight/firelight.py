from __future__ import print_function
import numpy as np
import sys

from firelight.processing.screen_processor import ScreenProcessor
from firelight.interfaces.lifx.lifx import LifxSystem

NUM_CLUSTERS = 16
FILTER_LOW_OCCURENCE_COLORS = True

light_systems = {"lifx": LifxSystem}


def get_system(system):
    if system not in light_systems:
        print("Sorry, that system is not recognized or currently supported.")
        sys.exit("Exiting program.")

    print(system + " selected.")
    system = light_systems[system]
    return system


def main():
    args = sys.argv[1:]

    if not args:
        print(""" Welcome to Firelight!\n
                  We currently support the following lights:""")

        for key in light_systems.keys():
            print(key)

        system = input("Which system do you use?")
    else:
        system = args[0]

    system = get_system(system)()
    processor = ScreenProcessor()

    while(True):
        # Set random seed to avoid "noisy" color changes when there are no
        # changes on the screen
        # Same seed means that kmeans will perform the same way in every
        # iteration for the same input screen image
        np.random.seed(seed=1337)

        im = processor.get_downsampled_screenshot()
        hls = processor.get_accent_color(im)
        if not hls:
            continue

        system.set_color_all_lights(hls)
