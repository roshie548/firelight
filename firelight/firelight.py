from __future__ import print_function
import numpy as np
import scipy
from lifxlan import LifxLAN
from mss import mss

from firelight.processing.screen_processor import ScreenProcessor
from firelight.interfaces.lifx.lifx import LifxSystem

NUM_CLUSTERS = 16
FILTER_LOW_OCCURENCE_COLORS = True


def main():
    sct = mss()

    # TODO: CONSIDER BLURRING IMAGE (CONVOLVING WITH A GUASSIAN KERNEL) TO GET BETTER COLORS? LESS VARIANCE?

    lan = LifxLAN()

    processor = ScreenProcessor()

    prev_l = 1
    prev_s = 1

    while(True):
        # Set random seed to avoid "noisy" color changes when there are no changes on the screen
        # Same seed means that kmeans will perform the same way in every iteration for the same input screen image
        np.random.seed(seed=1337)

        im = processor.get_downsampled_screenshot()
        hls = processor.get_accent_color(im)
        if not hls:
            continue
        h, l, s = hls

        # Smooth luminance, otherwise we will get some "shakey" light effects
        l = prev_l * .80 + l*.20
        prev_l = l

        lan.set_color_all_lights(
            [65535*h, 65535*s, 65535*l, 3500], duration=400, rapid=True)
        print("done")
        # time.sleep(0.1)
