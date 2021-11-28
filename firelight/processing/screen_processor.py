import numpy as np
import scipy
import scipy.cluster
from mss import mss
from firelight.interfaces.color import RGBColor
from firelight.processing.image import colorfulness


NUM_CLUSTERS = 16
FILTER_LOW_OCCURRENCE_COLORS = True


class ScreenProcessor():
    def __init__(
            self,
            monitor=1,
            num_clusters=NUM_CLUSTERS,
            filter_low_occurrence_colors=FILTER_LOW_OCCURRENCE_COLORS):
        self._num_clusters = num_clusters
        self._filter_low_occurrence_colors = filter_low_occurrence_colors
        self._sct = mss()
        self._monitor = self._sct.monitors[1]

    def get_downsampled_screenshot(self):
        """Compute a downsampled 2D array representing a screenshot.

        :return: Pixel values.
        :rtype: numpy array

        """
        im = np.array(self._sct.grab(self._monitor))
        im = im[::35, ::40, :3][:, :, ::-1]
        shape = im.shape
        im = im.reshape(np.product(shape[:2]), shape[2]).astype(float)
        return im

    def _get_dominant_colors(self, im):
        # Get clusters
        #   codes = centroids (i.e. color groups)
        codes, dist = scipy.cluster.vq.kmeans(im, self._num_clusters)
        vecs, dist = scipy.cluster.vq.vq(im, codes)  # assign codes
        counts, bins = np.histogram(vecs, len(codes))    # count occurrences

        if self._filter_low_occurrence_colors and len(codes) >= 8:
            indexes_max = np.argpartition(counts, -8)[8:]
            peaks = codes[indexes_max]
        else:
            peaks = codes

        return peaks, codes

    def get_accent_color(self, im):
        peaks, codes = self._get_dominant_colors(im)
        rgbs = [RGBColor(*color) for color in np.around(peaks).astype(int)]
        hlss = [color.to_hls() for color in rgbs]

        if not hlss:
            return

        colorfulness_values = np.array([colorfulness(x) for x in hlss])
        hls = hlss[np.argmax(colorfulness_values)]

        return hls.values()
