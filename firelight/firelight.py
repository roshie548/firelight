from __future__ import print_function
import numpy as np
import sys

from firelight.processing.screen_processor import ScreenProcessor
from firelight.interfaces.lifx.lifx import LifxSystem


light_systems = {"lifx": LifxSystem}


def get_system(system):
    if system not in light_systems:
        print("Sorry, that system is not recognized or currently supported.")
        sys.exit("Exiting program.")

    print(system + " selected.")
    system = light_systems[system]
    return system


def group_option(system):
    groups = system.list_groups()

    if not len(groups):
        print("No groups found... continuing with all lights")
        return system
    print("Found the following groups:\n")
    for g in groups:
        print(g)
    print()
    group = input(
        "If you'd like to use a certain group, enter the name of the group.\n"
        + "Otherwise, if you'd like to use all the lights, hit enter.\n")
    if not group:
        return system
    elif group in groups:
        return system.get_light_group(group)
    print("Sorry, that group could not be found. Please type in a group from "
          + "the list above\n")
    return group_option(system)


def main():
    args = sys.argv[1:]

    if not args:
        print("Welcome to Firelight!\n"
              + "We currently support the following lights:\n")

        for key in light_systems.keys():
            print(key)

        system = input("Which system do you use?\n")
    else:
        system = args[0]

    system = get_system(system)()
    system = group_option(system)
    processor = ScreenProcessor()

    print("\nAll good to go! Sit back and enjoy the show :)")
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

        system.set_color(hls)
