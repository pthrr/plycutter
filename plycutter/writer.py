#
# plycutter - generate finger-jointed laser cutter templates from 3D objects
# Copyright (C) 2020 Tuomas J. Lukka
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import ezdxf
import numpy as np

# XXX
from .geometry.aabb import AABB


def write_dxf(filename, geom2ds):
    dwg = ezdxf.new('AC1015')
    modelspace = dwg.modelspace()

    # Trivial nesting horizontally
    x = 0
    for name, geom in geom2ds.items():
        print(name)

        aabb = AABB()

        for polygon in geom.polygons():
            coords = np.array(polygon.spwhs[0].outer)
            for pt in coords:
                aabb.include_point(pt)

        margin = 3
        x_offset = x - aabb.lower[0] + margin
        y_offset = 0 - aabb.lower[1]
        x += aabb.upper[0] - aabb.lower[0] + margin

        def draw_coords(coords):
            coords = list(coords)
            coords = np.array(coords + coords[0:1])  # Loop
            coords = coords + [x_offset, y_offset]
            modelspace.add_lwpolyline(coords.tolist())

        for polygon in geom.polygons():
            draw_coords(polygon.spwhs[0].outer)
            for hole in polygon.spwhs[0].holes:
                draw_coords(hole)

    dwg.saveas(filename)
