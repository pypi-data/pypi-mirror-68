import numpy as np
from numpy import cos, sin

from ._jit import jit


@jit
def circular_velocity(k, a):
    r"""Compute circular velocity for a given body given thegravitational parameter and the semimajor axis.

    .. math::

       v = \sqrt{\frac{\mu}{a}}

    Parameters
    ----------

    k : float
        Gravitational Parameter
    a : float
        Semimajor Axis

    """
    return np.sqrt(k / a)


@jit
def rotation_matrix(angle, axis):
    c = cos(angle)
    s = sin(angle)
    if axis == 0:
        return np.array([[1.0, 0.0, 0.0], [0.0, c, -s], [0.0, s, c]])
    elif axis == 1:
        return np.array([[c, 0.0, s], [0.0, 1.0, 0.0], [s, 0.0, c]])
    elif axis == 2:
        return np.array([[c, -s, 0.0], [s, c, 0.0], [0.0, 0.0, 1.0]])
    else:
        raise ValueError("Invalid axis: must be one of 'x', 'y' or 'z'")


@jit
def alinspace(start, stop=None, num=50, endpoint=True):
    """Return increasing, evenly spaced angular values over a specified interval.

    """
    if stop is None:
        stop = start + 2 * np.pi
    elif stop <= start:
        stop += 2 * np.pi

    if endpoint:
        return np.linspace(start, stop, num)
    else:
        return np.linspace(start, stop, num + 1)[:-1]
