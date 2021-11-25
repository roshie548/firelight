from __future__ import print_function
import binascii
import numpy as np
import scipy
import scipy.cluster
from lifxlan import LifxLAN
from mss import mss
from colorsys import rgb_to_hls
import cv2
import time

import matplotlib.pyplot as plt

NUM_CLUSTERS = 16
FILTER_LOW_OCCURENCE_COLORS = True

sct = mss()
# sct.compression_level = 9

# Heuristic - In many cases, instead of just the most common color (for example gray/black)
#   we'd want an "accent" color. Accent colors usually aren't the majority of the screen,
#   but they take draw your eyes. We want to use this as our light color in many cases.
#   The heuristic we use to determine accent colors is to see which colors are "colorful",
#   which for our purposes, we try to calculate by multiplying saturation and luminance
# colorfulness = lambda x: x[2] * x[1]


def colorfulness(x):
    if x[1] <= 0.25:
        return 0
    return x[2] * x[1]

# TODO: CONSIDER BLURRING IMAGE (CONVOLVING WITH A GUASSIAN KERNEL) TO GET BETTER COLORS? LESS VARIANCE?


lan = LifxLAN()

prev_l = 1
prev_s = 1

while(True):
    # Set random seed to avoid "noisy" color changes when there are no changes on the screen
    # Same seed means that kmeans will perform the same way in every iteration for the same input screen image
    np.random.seed(seed=1337)

    # Grab screen and drop "alpha" value
    im = np.array(sct.grab(sct.monitors[1]))[::35, ::40, :3][:, :, ::-1]

    shape = im.shape
    print(shape)
    im = im.reshape(np.product(shape[:2]), shape[2]).astype(float)

    # Get clusters
    #   codes = centroids (i.e. color groups)
    codes, dist = scipy.cluster.vq.kmeans(im, NUM_CLUSTERS)

    vecs, dist = scipy.cluster.vq.vq(im, codes)    # assign codes
    counts, bins = np.histogram(vecs, len(codes))    # count occurrences

    if FILTER_LOW_OCCURENCE_COLORS and len(codes) >= 8:
        indexes_max = np.argpartition(counts, -8)[8:]
        peaks = codes[indexes_max]
    else:
        peaks = codes

    rgbs = np.around(peaks).astype(int)
    hlss = [rgb_to_hls(rgb[0]/255., rgb[1]/255., rgb[2]/255.) for rgb in rgbs]

    palette = np.array(rgbs)[np.newaxis, :, :]
    print(palette.shape)
    # plt.imshow(palette)
    # plt.axis('off')
    # plt.show()

    if not hlss:
        continue

    colorfulness_values = np.array([colorfulness(x) for x in hlss])
    peak = codes[np.argmax(colorfulness_values)]

    # colour = binascii.hexlify(bytearray(int(c) for c in peak)).decode('ascii')

    print("CHOSEN COLOR: %s", rgbs[np.argmax(colorfulness_values)])

    # rgb = hex_to_rgb(colour)
    # hls = rgb_to_hls(rgb[0]/255., rgb[1]/255., rgb[2]/255.)
    hls = hlss[np.argmax(colorfulness_values)]

    for p in codes:
        print("HEX: %s", binascii.hexlify(bytearray(int(c)
                                                    for c in p)).decode('ascii'))

    print("setting colors")

    h, l, s = hls

    # Smooth luminance, otherwise we will get some "shakey" light effects
    l = prev_l * .80 + l*.20
    prev_l = l

    lan.set_color_all_lights(
        [65535*h, 65535*s, 65535*l, 3500], duration=400, rapid=True)
    print("done")
    # time.sleep(0.1)
