"""Classes representing lattices of points.

TODO tidy: dataclasses? get rid of micron?
"""
import itertools
from typing import Tuple, Sequence, TypeVar, Generic
import numpy as np
from .geometry import find_2d_grid_crossings

class Lattice:
    """Two-dimensional lattice of points, not necessarily regularly spaced.

    The points are indexed by 2D indices.
    """

    def __init__(self, point_area: float):
        self.point_area = point_area

    def calc_point(self, i1, i2):
        """Calculate lattice point.

        Args:
            i1, i2: Mutually broadcastable arrays/numerics of type int.

        Returns:
            tuple: x and y values.
        """
        raise NotImplementedError()

    def calc_fractional_indices(self, x, y):
        """Calculate indices corresponding to given coordinates.

        Args:
            x, y (numeric): Coordinates.

        Returns:
            tuple: pair of point indices.
        """
        raise NotImplementedError()

    def calc_indices(self, x, y):
        """Calculate indices corresponding to coordinates.

        Args:
            x, y: Coordinates.

        Returns:
            2-tuple of integers: x and y indices.
        """
        i1, i2 = self.calc_fractional_indices(x, y)
        # Use np.round to ensure that returned type is numpy array or scalar.
        nx = np.round(i1).astype(int)
        ny = np.round(i2).astype(int)
        return nx, ny

    def scale(self, sx: float, sy: float = None):
        """Return scaled version of self."""
        raise NotImplementedError()

    def calc_offsets(self, x, y):
        i1, i2 = self.calc_indices(x, y)
        xc, yc = self.calc_point(i1, i2)
        return x - xc, y - yc

    def split_point(self, x, y):
        i1, i2 = self.calc_indices(x, y)
        xc, yc = self.calc_point(i1, i2)
        return (i1, i2), (xc, yc)

class FiniteCenteredRectangleLattice(Lattice):
    """Finite lattice with rectangular symmetry."""
    def __init__(self, finest_pitch_x: float, finest_pitch_y:float, side_length_x:float, side_length_y:float, size_x:int, size_y:int):
        Lattice.__init__(self, finest_pitch_x*finest_pitch_y)
        self.finest_pitch_x = finest_pitch_x
        self.finest_pitch_y = finest_pitch_y
        self.side_length_x = side_length_x
        self.side_length_y = side_length_y
        self.size_x = size_x
        self.size_y = size_y

class FiniteSquareLattice(Lattice):
    """Finite lattice with square symmetry."""
    def __init__(self, finest_pitch: float, side_length: float, size: int):
        Lattice.__init__(self, finest_pitch ** 2)
        self.finest_pitch = finest_pitch
        self.side_length = side_length
        self.size = size

    def points(self):
        for ix, iy in itertools.product(range(self.size), repeat=2):
            yield self.calc_point(ix, iy)

    def partition_along_line(self, origin: Tuple[float, float], vector: Tuple[float, float]) -> Sequence[
        Tuple[Tuple[float, float], Tuple[float, float]]]:
        """Divide a line into partitions, with each partition within one fine pitch of a point.

        Args:
            origin: Origin of line.
            vector: One unit of the line.

        Returns:
            list of (ix, iy), (d1, d2): For all entries, d2 > d1.
        """
        raise NotImplementedError()


class MarginFiniteSquareLattice(FiniteSquareLattice):
    def __init__(self, lattice: FiniteSquareLattice, margin: int):
        FiniteSquareLattice.__init__(self, lattice.finest_pitch, lattice.side_length - 2*margin*lattice.finest_pitch,
                                     lattice.size - 2*margin)
        self.lattice = lattice
        self.margin = margin

    def __repr__(self):
        return '%s(lattice=%r, margin=%r)'%(type(self).__name__, self.lattice, self.margin)

    def calc_point(self, ix, iy):
        ixp = ix + self.margin
        iyp = iy + self.margin
        return self.lattice.calc_point(ixp, iyp)

    def calc_fractional_indices(self, x, y):
        ixp, iyp = self.lattice.calc_fractional_indices(x, y)
        ix = ixp - self.margin
        iy = iyp - self.margin
        return ix, iy

    def scale(self, sx: float, sy: float = None) -> 'Lattice':
        """Return scaled version of self."""
        if sy is None:
            sy = sx
        assert sx == sy, 'Rectangular scaling not implemented yet.'
        return MarginFiniteSquareLattice(self.lattice.scale(sx, sy), self.margin)

    def partition_along_line(self, origin: Tuple[float, float], vector: Tuple[float, float]) -> Sequence[Tuple[Tuple[float, float], Tuple[float, float]]]:
        """Divide a line into partitions, with each partition within one fine pitch of a point.

        Args:
            origin: Origin of line.
            vector: One unit of the line.

        Returns:
            list of (ix, iy), (d1, d2): For all entries, d2 > d1.
        """
        all_partitions = self.lattice.partition_along_line(origin, vector)
        partitions = []
        for (ix, iy), ds in all_partitions:
            ixp = ix - self.margin
            iyp = iy - self.margin
            if (0 <= ixp < self.size) and (0 <= iyp  < self.size):
                partitions.append(((ixp, iyp), ds))
        return partitions


class RegularFiniteSquareLattice(FiniteSquareLattice):
    """Finite centered square lattice.

    The points are at
        x_n = (n - (size-1)/2)*pitch
    and likewise for y.

    Args:
        pitch (scalar): Pitch.
        size (int): Number of points to a side.
    """

    def __init__(self, pitch, size):
        FiniteSquareLattice.__init__(self, pitch, pitch*size, size)
        self.pitch = pitch

        # self.parameter_strings = ('regular square lattice', 'pitch %.3f micron'%(self.pitch*1e6), 'size %dx%d'%(self.size, self.size))

    def __repr__(self):
        return 'RegularSquareLattice(pitch=%g micron, size=%d)'%(self.pitch*1e6, self.size)

    def __str__(self):
        return 'RegularSquareLattice(pitch=%g micron, size=%d)'%(self.pitch*1e6, self.size)

    def calc_ordinate(self, index):
        index = np.asarray(index)
        return (index - (self.size - 1)/2)*self.pitch

    def calc_fractional_index(self, s):
        s = np.asarray(s)
        return s/self.pitch + (self.size - 1)/2

    def calc_point(self, ix, iy) -> tuple:
        """Calculate lattice point.

        Args:
            ix, iy: Mutually broadcastable arrays/numerics of type int.

        Returns:
            x and y values.
        """
        x = self.calc_ordinate(ix)
        y = self.calc_ordinate(iy)
        return x, y

    def calc_fractional_indices(self, x, y):
        ix = self.calc_fractional_index(x)
        iy = self.calc_fractional_index(y)
        return ix, iy

    def partition_along_line(self, origin: Tuple[float, float], vector: Tuple[float, float]) -> Sequence[Tuple[Tuple[float, float], Tuple[float, float]]]:
        """Divide a line into partitions, with each partition within one fine pitch of a point.

        Args:
            origin: Origin of line.
            vector: One unit of the line.

        Returns:
            list of (ix, iy), (d1, d2): For each entry, d2 > d1.
        """
        origin = np.asarray(origin)
        vector = np.asarray(vector)
        origin_rel = (origin - self.calc_point(-0.5, -0.5))/self.pitch
        d_crossings = mathx.find_2d_grid_crossings(self.size, self.size, *origin_rel, *(vector/self.pitch))
        d0s = d_crossings[:-1]
        d1s = d_crossings[1:]
        assert (d1s > d0s).all()
        d_midpoints = (d0s + d1s)/2
        ixs, iys = self.calc_indices(*(origin[:, None] + d_midpoints*vector[:, None]))
        return list(zip(zip(ixs, iys), zip(d0s, d1s)))

    def scale(self, sx: float, sy: float = None) -> 'RegularFiniteSquareLattice':
        """Return scaled version of self."""
        if sy is None:
            sy = sx
        assert sx == sy, 'Rectangular scaling not implemented yet.'
        return RegularFiniteSquareLattice(self.pitch*sx, self.size)

class RegularFiniteCenteredRectangleLattice(FiniteCenteredRectangleLattice):
    """Finite square lattice.

    The points are at
        x_n = (n - (shape[0]-1)/2)*pitches[0]
    and likewise for y.

    Args:
        pitches (pair of scalar): Pitch.
        shape (pair of int): Number of points to a side.
    """

    def __init__(self, pitch_x: float, pitch_y:float, size_x:int, size_y:int):
        FiniteCenteredRectangleLattice.__init__(self, pitch_x, pitch_y, size_x*pitch_x, size_y*pitch_y, size_x, size_y)
        self.pitch_x = pitch_x
        self.pitch_y = pitch_y

        # self.parameter_strings = ('regular square lattice', 'pitch %.3f micron'%(self.pitch*1e6), 'size %dx%d'%(self.size, self.size))

    def __repr__(self):
        return f'{self.__class__.__name__}({self.pitch_x}, {self.pitch_y}, {self.size_x}, {self.size_y})'

    # def calc_ordinate(self, index):
    #     index = np.asarray(index)
    #     return (index - (self.size - 1)/2)*self.pitch
    #
    # def calc_fractional_index(self, s):
    #     s = np.asarray(s)
    #     return s/self.pitch + (self.size - 1)/2

    def calc_point(self, ix, iy):
        """Calculate lattice point.

        Args:
            ix, iy: Mutually broadcastable arrays/numerics of type int.

        Returns:
            tuple: x and y values.
        """
        x = (ix - (self.size_x - 1)/2)*self.pitch_x
        y = (iy - (self.size_y - 1)/2)*self.pitch_y
        return x, y

    def calc_fractional_indices(self, x, y):
        ix = x/self.pitch_x + (self.size_x - 1)/2
        iy = y/self.pitch_y + (self.size_y - 1)/2
        return ix, iy

    def points(self):
        for ix in range(self.size_x):
            for iy in range(self.size_y):
                yield self.calc_point(ix, iy)

    # def partition_along_line(self, origin: Tuple[float, float], vector: Tuple[float, float]) -> Sequence[Tuple[Tuple[float, float], Tuple[float, float]]]:
    #     """Divide a line into partitions, with each partition within one fine pitch of a point.
    #
    #     Args:
    #         origin: Origin of line.
    #         vector: One unit of the line.
    #
    #     Returns:
    #         list of (ix, iy), (d1, d2): For each entry, d2 > d1.
    #     """
    #     origin = np.asarray(origin)
    #     vector = np.asarray(vector)
    #     origin_rel = (origin - self.calc_point(-0.5, -0.5))/self.pitch
    #     d_crossings = mathx.find_2d_grid_crossings(self.size, self.size, *origin_rel, *(vector/self.pitch))
    #     d0s = d_crossings[:-1]
    #     d1s = d_crossings[1:]
    #     assert (d1s > d0s).all()
    #     d_midpoints = (d0s + d1s)/2
    #     ixs, iys = self.calc_indices(*(origin[:, None] + d_midpoints*vector[:, None]))
    #     return list(zip(zip(ixs, iys), zip(d0s, d1s)))
    #
    def scale(self, sx: float, sy: float = None):
        """Return scaled version of self."""
        if sy is None:
            sy = sx
        return RegularFiniteCenteredRectangleLattice(self.pitch_x*sx, self.pitch_y*sy, self.size_x, self.size_y)

class FiniteSquareLatticeLattice(FiniteSquareLattice):
    def __init__(self, coarse_lattice: FiniteSquareLattice, fine_lattice: FiniteSquareLattice):
        FiniteSquareLattice.__init__(self, fine_lattice.finest_pitch, coarse_lattice.side_length,
                                     coarse_lattice.size*fine_lattice.size)
        self.coarse_lattice = coarse_lattice
        self.fine_lattice = fine_lattice

    def split_indices(self, ix, iy):
        cix = np.floor(ix/self.fine_lattice.size).astype(int)
        ciy = np.floor(iy/self.fine_lattice.size).astype(int)
        fix = ix - cix*self.fine_lattice.size
        fiy = iy - ciy*self.fine_lattice.size
        return cix, ciy, fix, fiy

    def combine_indices(self, cix, ciy, fix, fiy):
        """Inverse function of split indices."""
        ix = cix*self.fine_lattice.size + fix
        iy = ciy*self.fine_lattice.size + fiy
        return ix, iy

    def calc_point(self, ix, iy):
        ix = np.asarray(ix)
        iy = np.asarray(iy)
        cix, ciy, fix, fiy = self.split_indices(ix, iy)
        xc, yc = self.coarse_lattice.calc_point(cix, ciy)
        xo, yo = self.fine_lattice.calc_point(fix, fiy)
        return xc + xo, yc + yo

    def calc_fractional_indices(self, x, y):
        x = np.asarray(x)
        y = np.asarray(y)
        cix, ciy = self.coarse_lattice.calc_indices(x, y)
        xc, yc = self.coarse_lattice.calc_point(cix, ciy)
        xo = x - xc
        yo = y - yc
        fix, fiy = self.fine_lattice.calc_fractional_indices(xo, yo)
        ix, iy = self.combine_indices(cix, ciy, fix, fiy)
        return ix, iy

    def scale(self, sx: float, sy: float = None) -> 'FiniteSquareLatticeLattice':
        """Return scaled version of self."""
        if sy is None:
            sy = sx
        assert sx == sy, 'Rectangular scaling not implemented yet.'
        return FiniteSquareLatticeLattice(self.coarse_lattice.scale(sx, sy), self.fine_lattice.scale(sx, sy))

    def partition_along_line(self, origin: Tuple[float, float], vector: Tuple[float, float]) -> Sequence[
        Tuple[Tuple[float, float], Tuple[float, float]]]:
        """Divide a line into partitions, with each partition within one fine pitch of a point.

        Args:
            origin: Origin of line.
            vector: One unit of the line.

        Returns:
            list of (ix, iy), (d1, d2): For all entries, d2 > d1.
        """
        origin = np.asarray(origin)
        vector = np.asarray(vector)
        coarse_partitions = self.coarse_lattice.partition_along_line(origin, vector)
        partitions = []
        for (cix, ciy), _ in coarse_partitions:
            xc, yc = self.coarse_lattice.calc_point(cix, ciy)
            fine_partitions = self.fine_lattice.partition_along_line(origin - (xc, yc), vector)
            for (fix, fiy), ds in fine_partitions:
                assert ds[1] > ds[0]
                partitions.append((self.combine_indices(cix, ciy, fix, fiy), ds))
        return partitions

class RegularOffsetHexLattice(Lattice):
    def __init__(self, pitch, offset_ix, offset_iu):
        point_area = pitch**2*3**0.5/2 # Dane's logbook 3 p56.
        Lattice.__init__(self, point_area)
        self.pitch = pitch
        self.offset_ix = offset_ix
        self.offset_iu = offset_iu

    def calc_point(self, ix, iu):
        ixp = ix + self.offset_ix
        iup = iu + self.offset_iu
        x = (ixp + iup*0.5)*self.pitch
        y = iup*self.pitch*3**0.5/2
        return x, y