from . import writer
from . import data_array

import functools
import numpy as np


class VTKFile:
    """Generic VTK file"""

    def __init__(self, filename, filetype):
        self.filetype = filetype
        self.filename = filename
        self.writer = writer.Writer(filetype)

        # Center piece
        self.piece = self.writer.registerPiece()

        # Registering data elements
        self.point_data = self.piece.register('PointData')
        self.cell_data = self.piece.register('CellData')

    def addPointData(self, data_array):
        self.point_data.registerDataArray(data_array)

    def addCellData(self, data_array):
        self.cell_data.registerDataArray(data_array)

    def write(self):
        self.writer.registerAppend()
        self.writer.write(self.filename)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.write()


class ImageData(VTKFile):
    """VTK Image data (coordinates given by a range and constant spacing)"""

    def __init__(self, filename, ranges, points):
        VTKFile.__init__(self, filename, 'ImageData')

        # Computing spacings
        spacings = [(x[1] - x[0]) / (n - 1) for x, n in zip(ranges, points)]

        # Filling in missing coordinates
        for _ in range(len(points), 3):
            points.append(1)

        # Setting extents, spacing and origin
        extent = functools.reduce(
            lambda x, y: x + "0 {} ".format(y-1), points, "")
        spacings = functools.reduce(
            lambda x, y: x + "{} ".format(y), spacings, "")
        origins = functools.reduce(
            lambda x, y: x + "{} ".format(y[0]), ranges, "")

        self.writer.setDataNodeAttributes({
            'WholeExtent': extent,
            'Spacing': spacings,
            'Origin': origins
        })

        self.piece.setAttributes({
            "Extent": extent
        })


class RectilinearGrid(VTKFile):
    """VTK Rectilinear grid (coordinates are given by 3 seperate ranges)"""

    def __init__(self, filename, coordinates, offsets=None):
        VTKFile.__init__(self, filename, 'RectilinearGrid')

        # Checking that we actually have a list or tuple
        if type(coordinates).__name__ == 'ndarray':
            coordinates = [coordinates]

        self.coordinates = list(coordinates)

        # Filling in missing coordinates
        for _ in range(len(self.coordinates), 3):
            self.coordinates.append(np.array([0.]))

        # Setting data extent
        extent = []

        for coord in self.coordinates:
            if coord.ndim != 1:
                raise Exception(
                    'Coordinate array should have only one dimension'
                    + ' (has {})'.format(coord.ndim))
            extent.append(coord.size-1)

        if offsets is None:
            offsets = [0] * len(extent)
        elif len(offsets) == len(coordinates):
            offsets = list(offsets)
            offsets += [0] * (len(extent) - len(offsets))
        else:
            raise Exception(
                'Size of offsets should '
                'match domain dimension {}'.format(len(coordinates)))

        def fold_extent(acc, couple):
            offset, extent = couple

            if offset != 0:
                offset -= 1
            return acc + "{} {} ".format(offset, offset+extent)

        # Create extent string with offsets
        self.extent = functools.reduce(fold_extent, zip(offsets, extent), "")

        self.writer.setDataNodeAttributes({
            "WholeExtent": self.extent
        })

        self.piece.setAttributes({
            "Extent": self.extent
        })

        # Registering coordinates
        coordinate_component = self.piece.register('Coordinates')

        for coord, prefix in zip(self.coordinates, ('x', 'y', 'z')):
            array = data_array.DataArray(coord, [0], prefix + '_coordinates')
            coordinate_component.registerDataArray(array)


class StructuredGrid(VTKFile):
    """VTK Structured grid (coordinates given by a single array of points)"""

    def __init__(self, filename, points, shape):
        VTKFile.__init__(self, filename, 'StructuredGrid')

        if points.ndim != 2:
            raise 'Points should be a 2D array'

        # Completing the missing coordinates
        points_3d = np.zeros((points.shape[0], 3))
        for i in range(points.shape[1]):
            points_3d[:, i] = points[:, i]

        extent = [n - 1 for n in shape]
        for i in range(len(extent), 3):
            extent.append(0)

        extent = functools.reduce(
            lambda x, y: x + "0 {} ".format(y), extent, "")
        self.writer.setDataNodeAttributes({
            "WholeExtent": extent
        })

        self.piece.setAttributes({
            "Extent": extent
        })

        points_component = self.piece.register('Points')
        points_component.registerDataArray(
            data_array.DataArray(points_3d, [0], 'points'))
