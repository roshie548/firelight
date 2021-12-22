from __future__ import annotations
import numpy as np
from heapq import heappop, heappush, heapify


class Tree():
    def __init__(self, image):
        root = Node(image, 1)

        height, width = image.shape
        self._classes = np.ones((height, width))
        self._num_classes = 1

        # Use max heap?
        # self._queue =
        pass

    def find_dominant_colors(self):
        pass


class Node():
    def __init__(
            self,
            colors,
            class_id: int):
        self._colors = colors
        self._mean = colors.mean(axis=0)
        self._cov = np.cov(colors.T)
        self._class_id = class_id

    def get_statistics(self):
        u, s, vh = np.linalg.svd(self._colors)
        singular_value = s[0]
        principal_axis = vh[0]
        score = u[:, 0] @ singular_value
        return singular_value, principal_axis, score

    def partition(self, next_id):
        _, principal_axis, score = self.get_statistics()
        threshold = self._mean @ principal_axis
        rightColors = self._colors[score > threshold]
        leftColors = self._colors[score <= threshold]
        rightNode = Node(rightColors, next_id)
        leftNode = Node(leftColors, self._class_id)
        return leftNode, rightNode
