import numpy as np
import scipy
import scipy.cluster
from mss import mss
from firelight.interfaces.color import RGBColor
from firelight.processing.image import colorfulness
from firelight.processing.quantizer import Tree
# from matplotlib import pyplot as PLT


FILTER_LOW_OCCURRENCE_COLORS = True
DOWNSAMPLED_SCREENSHOT_NUM_PIXELS = 20000


class ScreenProcessor():
    def __init__(
            self,
            monitor=1,
            filter_low_occurrence_colors=FILTER_LOW_OCCURRENCE_COLORS):
        self._filter_low_occurrence_colors = filter_low_occurrence_colors
        self._sct = mss()
        self._monitor = self._sct.monitors[1]
        self._r = None

    def get_downsampled_screenshot(self):
        """Compute a downsampled 2D array representing a screenshot.

        :return: Pixel values.
        :rtype: numpy array

        """
        im = np.array(self._sct.grab(self._monitor))  # shape: h * w * 3

        # Want an image size of ~20,000 pixels (experimentally determined)
        # Let size of the original screenshot (im) be w_0 x h_0
        # Let w, h be the size of the downsampled screenshot
        # Constraints:
        # (1) w * h = 2000
        # (2) w_0 = r * w, h_0 = r * h
        # Solving for r:
        # r = sqt((w_o * h_0) / 20,000)
        if not self._r:
            h_0, w_0, _ = im.shape
            r = np.rint(
                np.sqrt(h_0 * w_0 / DOWNSAMPLED_SCREENSHOT_NUM_PIXELS)).astype(int)
        else:
            r = self._r

        im = np.flip(im[::r, ::r, :3], 2)
        shape = im.shape
        im = im.reshape(np.product(shape[:2]), shape[2]).astype(float)
        return im

    def _get_dominant_colors(self, im):
        """Return the dominant colors of the image.

        :param im: 2D numpy array representing the screenshot.
        :return: A k x 3 array of k centroids, where the ith element represents
                 the coordinates for the ith centroid.
        :rtype: 2D array

        """
        # Get clusters
        tree = Tree(im)
        centroids = tree.find_dominant_colors()
        codes, dist = scipy.cluster.vq.kmeans(im, centroids)
        vecs, dist = scipy.cluster.vq.vq(im, codes)  # assign codes
        counts, bins = np.histogram(vecs, len(codes))    # count occurrences

        if self._filter_low_occurrence_colors and len(codes) >= 5:
            indexes_max = np.argpartition(counts, -5)[5:]
            peaks = codes[indexes_max]
        else:
            peaks = codes

        return peaks

    def get_accent_color(self, im):
        """Return the main accent color of the screenshot.

        :param im: 2D numpy array representing the screenshot.
        :return: Main accent color
        :rtype: HLSColor

        """
        peaks = self._get_dominant_colors(im)
        rgbs = [RGBColor(*color) for color in np.around(peaks).astype(int)]
        hlss = [color.to_hls() for color in rgbs]

        if not hlss:
            return

        colorfulness_values = np.array([colorfulness(x) for x in hlss])
        hls = hlss[np.argmax(colorfulness_values)]

        return hls
