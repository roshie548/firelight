from __future__ import annotations
import numpy as np
from heapq import heappop, heappush

NUM_CLUSTERS = 12


class Tree():
    def __init__(self, image):
        root = Node(image, 1)

        height, width = image.shape
        self._classes = np.ones((height, width))
        self._num_classes = 1

        # Use a priority queue
        self._queue = []
        heappush(self._queue, (1, root))

    def find_dominant_colors(self):
        keep_going = True
        while keep_going:
            _, node = heappop(self._queue)
            left_child, right_child = node.partition(self._num_classes + 1)

            heappush(self._queue, (-1 * left_child.get_priority(), left_child))
            heappush(self._queue, (-1 * right_child.get_priority(), right_child))

            self._num_classes += 1
            keep_going = True in [
                node.get_priority() > 3000 for priority, node in self._queue] and self._num_classes < NUM_CLUSTERS

        print([node._max_eigenvalue for _, node in self._queue])
        return [node._mean for _, node in self._queue]


class Node():
    def __init__(
            self,
            colors,
            class_id: int):
        self._colors = colors
        self._mean = colors.mean(axis=0)
        self._cov = np.cov(colors.T)
        self._class_id = class_id
        self._max_eigenvalue, self.principal_axis = self.get_statistics()

    def get_statistics(self):
        eig_vals, eig_vecs = np.linalg.eig(self._cov)
        index = eig_vals.argmax()

        return eig_vals[index], eig_vecs[eig_vals.argmax()]

    def partition(self, next_id):
        threshold = self._mean @ self.principal_axis
        score = self._colors @ self.principal_axis

        rightColors = self._colors[score > threshold]
        leftColors = self._colors[score <= threshold]
        rightNode = Node(rightColors, next_id)
        leftNode = Node(leftColors, self._class_id)
        return leftNode, rightNode

    def get_priority(self):
        return self._max_eigenvalue
