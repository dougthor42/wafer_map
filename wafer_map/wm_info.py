# -*- coding: utf-8 -*-
"""
The :class:`wafer_map.wm_info.WaferInfo` class.
"""

class WaferInfo(object):
    """
    Contains the wafer information.

    Parameters
    ----------
    die_size : tuple
        The die size in mm as a ``(width, height)`` tuple.
    center_xy : tuple
        The center grid coordinate as a ``(x_grid, y_grid)`` tuple.
    dia : float, optional
        The wafer diameter in mm. Defaults to `150`.
    edge_excl : float, optional
        The distance in mm from the edge of the wafer that should be
        considered bad die. Defaults to 5mm.
    flat_excl : float, optional
        The distance in mm from the wafer flat that should be
        considered bad die. Defaults to 5mm.
    """

    def __init__(self, die_size, center_xy, dia=150, edge_excl=5, flat_excl=5):
        self.die_size = die_size
        self.center_xy = center_xy
        self.dia = dia
        self.edge_excl = edge_excl
        self.flat_excl = flat_excl

    def __str__(self):
        string = """
Wafer Dia: {}mm
Die Size: {}
Grid Center XY: {}
Edge Excl: {}
Flat Excl: {}
"""
        return string.format(self.dia,
                             self.die_size,
                             self.center_xy,
                             self.edge_excl,
                             self.flat_excl,
                             )


def main():
    """Run when called as a module."""
    raise RuntimeError("This module is not meant to be run by itself.")


if __name__ == "__main__":
    main()
