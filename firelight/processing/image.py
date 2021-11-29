from firelight.interfaces.color import HLSColor


def colorfulness(color: HLSColor):
    """
    We define a colorfulness heuristic as luminance * saturation. In many
    cases, the most common color in an image could be an uninteresting color,
    such as gray or black. By using a luminance heuristic, we can select an
    "accent" color - one which draws our eyes more.

    :param HLSColor color: HSL Color to get the colorfulness of.
    :return: Colorfulness value.
    :rtype: float

    """
    h, l, s = color.values()
    if l <= 0.25:
        return 0
    return s * l
