"""
Hexagonal Lattice
Data Structure of Hexagonal Lattice

@Author: LZK
@Date: 2023-5-31
"""
import os
from os import PathLike
from typing import Any

from .coordinates import *
import math
# import matplotlib.pyplot as plt
from collections import OrderedDict

class HexCell:

    def __init__(
            self,
            positon: CubeCoordinate,
            pitch: float,
            orientation: float = 0.
        ) -> None:
        """
        Point in hexagonal lattice

        Input
        -----
        position: CubeCoordinate, the position number of point in lattice
        pitch: float, the pitch (distance between central points of adjacent cells) of lattice
        """
        self._position = positon
        self._pitch = pitch
        self._value = dict()
        self._orientation = orientation
    
    @property
    def central_point(self) -> tuple:
        position_ring_coor = self._position.to_ring()
        return self.rk2xy(
            r = position_ring_coor.r,
            k = position_ring_coor.k if position_ring_coor.k > 0 else 6 * position_ring_coor.r,
            pitch=self._pitch
        )
    
    @property
    def surround_points(self) -> tuple:
        central_point = self.central_point
        vertex_half_distance = self._pitch / math.sqrt(3)  # Distance between two farest vertex points
        res = list()
        for k in range(6):
            angle = (2 * k + 1) * math.pi / 6 + self._orientation
            x = central_point[0] + vertex_half_distance * math.cos(angle)
            y = central_point[1] + vertex_half_distance * math.sin(angle)
            res.append((x, y))
        return res

    def rk2xy(self, r: int, k: int, pitch: float = 1.0) -> tuple:
        """
        Convert the (ring,clock) coordinate to (x,y) Cartesian coordinate

        Input
        -----
        r: int, the ring coordinate
        k: int, the clock coordinate
        pitch: float, the pitch of core lattice
        """
        # Check input
        if type(r) is not int or type(k) is not int:
            raise TypeError("Input coordinate is not type int.")
        
        # Handle the innest ring (single assembly)
        if r == 0:
            assert k == 0
            return (0., 0.)

        # Determine which sector is (r,k)
        sector = k // r
        # Determine which seat is (r,k) in this sector.
        seat = k % r

        # This first seat in sector (clockwise)
        degree = (1 - sector) * math.pi / 3
        radius = r * pitch
        x = radius * math.cos(degree)
        y = radius * math.sin(degree)

        # Move to the target seat
        degree -= 2 * math.pi / 3
        distance = seat * pitch
        x += distance * math.cos(degree)
        y += distance * math.sin(degree)

        return (x, y)

    def __str__(self) -> str:
        return f"HexCell({self._position})"
    
    @property
    def position(self) -> CubeCoordinate:
        return self._position
    
    @property
    def pitch(self) -> float:
        return self._pitch
    
    @property
    def coordinate(self) -> tuple:
        ring_coordinate = self._position.to_ring()
        return ring_coordinate.r, ring_coordinate.k
    
    @property
    def value(self) -> dict:
        return self._value.copy()
    
    @property
    def orientation(self) -> float:
        return self._orientation
    
    @orientation.setter
    def orientation(self, value):
        self._orientation = value
    
    def __setitem__(self, key, value):
        self._value[key] = value
    
    def __getitem__(self, key):
        return self._value[key]


class HexLattice:

    def __init__(self, ring: int, pitch: float) -> None:
        self._ring = ring
        self._pitch = pitch
        self._lattice = list()
        self._figure = None # Matplotlib.figure, created in HexLattice.plot()
        self._axes = None
    
    def generate_lattice(self) -> list:
        for r in range(self._ring):
            start_point = CubeCoordinate(x=+r, y=0, z=-r)
            ring_points = list()
            for point_k in start_point.get_ring():
                cell_k = HexCell(positon=point_k, pitch=self._pitch)
                ring_points.append(cell_k)
            self._lattice.append(ring_points)
        
        return self._lattice
    
    def plot(
            self,
            keys           : str      = 'position',               # Plot multiple keys using `keys = 'key1&key2`
            text_size      : float    = 8,
            save_path      : PathLike = 'plot/HexLattice.svg',
            color_map      : str      = None,
            offset_factor  : float    = 0.,
            max_ring_idx   : int      = -1,
            show_wireframe : bool     = True,
            show_colorbar  : bool     = True,
            show_axis      : bool     = False,
            colorbar_format: str      = "{x:.2f}",
            **kwargs
        ):
        if not self._lattice:
            raise SyntaxError("Lattice has not been genderated yet.")
        
        try:
            import matplotlib.pyplot as plt
            plt.rc('font', family='Times New Roman')
        except ImportError:
            raise ImportError("Matplotlib could not be imported.")
        
        # if color_map:
        try:
            import numpy as np
            from matplotlib.patches import Polygon, Circle
            from matplotlib.collections import PatchCollection
            from matplotlib.colors import TABLEAU_COLORS
        except ImportError:
            raise ImportError("Numpy or Matplotlib.[patches,collections] could not be imported.")
        patches = list()
        colors = list()
        # color = None
        has_color = False

        if max_ring_idx < 0:
            max_ring_idx = self._ring

        if 'linewidth' in kwargs:
            linewidth = kwargs['linewidth']
        else:
            linewidth = 1

        if 'figsize' in kwargs:
            figsize = kwargs['figsize']
        else:
            figsize = (4, 4)
        if 'dpi' in kwargs:
            dpi = kwargs['dpi']
        else:
            dpi = 400
        self._figure, self._axes = plt.subplots(figsize=figsize, dpi=dpi)

        data_fmt : str = 'default'
        if 'data_fmt' in kwargs:
            data_fmt = kwargs['data_fmt']

        for ring_idx, ring in enumerate(self._lattice):
            if ring_idx >= max_ring_idx: continue
            for cell_idx, cell in enumerate(ring):
                # plt.scatter(*cell.central_point, c='k')
                text_x = cell.central_point[0] - cell.pitch * offset_factor
                text_y = cell.central_point[1]
                r, k = cell.coordinate

                for key in keys.split('&'):

                    # The text value to be showed
                    if key == 'position':
                        text_to_print = "Cell({:d},{:d})".format(r, k)
                        color = None
                    elif key == 'position-brief':
                        text_to_print = "({:d},{:d})".format(r, k)
                        color = None
                    else:
                        try:
                            cell_info   = self._lattice[r][k][key]
                            value       = cell_info['value']
                            cell_shape  = cell_info['shape']
                            cell_radius = cell_info['radius']
                            offset      = cell_info['offset']
                            zorder      = cell_info['zorder']
                            color       = cell_info['color']
                            orientation = cell_info['orientation']
                        except KeyError:
                            print("Key not found: self._lattice[{}][{}][{}]".format(r, k, key))
                            continue
                            # raise KeyError("self._lattice[{}][{}][{}]".format(r, k, key))
                        
                        if value is None:
                            text_to_print = ''
                        elif isinstance(value, float):
                            if data_fmt == '%':
                                text_to_print = "{:.2%}".format(value)
                            elif data_fmt in ('F', 'f'):
                                text_to_print = "{:.2f}".format(value)
                            elif data_fmt in ('E', 'e'):
                                text_to_print = "{:.2E}".format(value)
                            else:
                                if abs(value) >= 100. or (abs(value) <= 1E-2 and abs(value) > 1E-15):
                                    text_to_print = "{:.2E}".format(value)
                                else:
                                    text_to_print = "{:.2f}".format(value)
                        elif not isinstance(value, str):
                            text_to_print = str(round(value, 2))
                        else:
                            text_to_print = value

                    surround_points = cell.surround_points
                    start_point = surround_points[-1]

                    # Prepare the fillment of cell
                    if color_map or color:
                        if cell_shape == 'hex':
                            if not cell_radius:
                                xy = np.vstack(surround_points)
                            else:
                                hex_cell = HexCell(
                                    positon = cell.position,
                                    pitch = cell_radius,
                                    orientation = orientation
                                )
                                xy = np.vstack(
                                    hex_cell.surround_points
                                )
                            if color is None:
                                hexagon = Polygon(xy=xy, closed=True, zorder=zorder)
                                patches.append(hexagon)
                                if value is None:
                                    colors.append(0.0)
                                else:
                                    colors.append(value)
                            else:
                                has_color = True
                                if not color.startswith('#'):
                                    color = TABLEAU_COLORS[f'tab:{color}']
                                hexagon = Polygon(xy=xy, closed=True, zorder=zorder, color=color)
                                # print(color, hexagon, hexagon.get_visible())
                                patches.append(hexagon)
                                colors.append(color)
                        elif cell_shape == 'circ':
                            central_point = cell.central_point[:2]
                            circle_center = np.array(central_point) + np.array(offset)
                            if color is None:
                                circle = Circle(xy=circle_center, radius=cell_radius, zorder=zorder)
                                patches.append(circle)
                                if value is None:
                                    colors.append(0.0)
                                else:
                                    colors.append(value)
                            else:
                                if not color.startswith('#'):
                                    color = TABLEAU_COLORS[f'tab:{color}']
                                circle = Circle(xy=circle_center, radius=cell_radius, zorder=zorder, color=color)
                                patches.append(circle)
                                colors.append(color)
                    
                    # Plot the wireframe of hexagon
                    if show_wireframe:
                        for point in surround_points:
                            # plt.scatter(point[0], point[1], c='k')
                            plt.plot(
                                *list(zip(start_point, point)),
                                c = 'k',
                                zorder = 2,
                                linewidth = linewidth
                            )
                            start_point = point
                    # else:
                    #     core_radius = max_ring_idx * self._pitch
                    #     plt.xlim([-core_radius, +core_radius])
                    #     plt.ylim([-core_radius, +core_radius])
                    
                    # Cell value
                    plt.text(
                        x = text_x,
                        y = text_y,
                        s = text_to_print,
                        fontdict = {
                            'family': 'Times New Roman',
                            'size': text_size,
                            # 'fontweight': 'bold'
                        },
                        horizontalalignment = 'center',
                        verticalalignment = 'center',
                        zorder = 3
                    )
        
        if 'clim' in kwargs:
            cmin, cmax = kwargs['clim']
            colors.append(cmin)
            colors.append(cmax)

        # Plot all the hexagons
        if color_map:
            if not has_color:
                p = PatchCollection(patches=patches, alpha=0.7)
                p.set_array(np.array(colors))
                p.set_cmap(color_map)
            else:
                p = PatchCollection(patches=patches)             # Solid color if given color
                p.set_color(colors)
            self._axes.add_collection(p)
            if show_colorbar:
                plt.rc('font', size=16)
                self._figure.colorbar(
                    p,
                    ax=self._axes,
                    format=colorbar_format
                )
        
        if not show_wireframe:
            core_radius = max_ring_idx * self._pitch
            plt.xlim([-core_radius, +core_radius])
            plt.ylim([-core_radius, +core_radius])
        
        if 'xlim' in kwargs:
            plt.xlim(kwargs['xlim'])
        if 'ylim' in kwargs:
            plt.ylim(kwargs['ylim'])
        
        if not show_axis:
            plt.axis('off')

        if save_path is None:
            plt.show()
        elif save_path == '--supress':
            pass
        else:
            if not os.path.exists(save_path):
                save_path = os.path.join(os.getcwd(), save_path)
            dir_path = os.path.dirname(save_path)
            if not os.path.exists(dir_path):
                os.mkdir(dir_path)
            
            plt.savefig(save_path)

    # def append_data_by_row(self, key: str, value: Any):
    #     """
    #     Append data into lattice row-by-row

    #     Example
    #     -------
    #     ```python
    #     ```

    #     Return
    #     ------
    #     A generator
    #     """
    #     idx = 0
    #     _, axial_to_ring = self.generate_ring_axial_hash()
    #     print(axial_to_ring)

    #     for idx, ring_coor in enumerate(axial_to_ring):
    #         r, k = ring_coor
    #         self._lattice[r][k][key] = value
    #         print(idx, r, k, value)

    def generate_ring_axial_hash(self) -> tuple[OrderedDict, OrderedDict]:
        """
        Generate the Ring-Axial Conversion Hash Table

        Returns
        -------
        tuple(ring_to_axial: OrderedDict, axial_to_ring: OrderedDict)

        Example
        -------
        ```python
        >>> ring_to_axial, axial_to_ring = HexLattice.generate_ring_axial_hash()
        >>> ring_to_axial[(1,3)]
        (2,0)
        >>> axial_to_ring[(2,0)]
        (1,3)
        ```

        Illustration
        ------------
        ```
           (1,5)   (1,0)               (0,0)   (0,1)
        (1,4)  (0,0)  (1,1)    =>   (1,0)  (1,1)  (1,2)
           (1,3)   (1,2)               (2,0)   (2,1)
        """
        ring_to_axial = OrderedDict()
        axial_to_ring = OrderedDict()

        try:
            import numpy as np
        except ImportError as e:
            print("Numpy could not be imported.")

        # Traverse the core row-by-row
        #     l: row    r: ring    k: clockwise order
        for l in range(2*self._ring - 1):
            dis2centerLine = abs(self._ring - 1 - l)
            s = -1

            # Go from outer ring to inner ring (120 ~ 240 degree)
            for j in range(self._ring - 1 - dis2centerLine):
                r = (self._ring - 1) - j
                k = 5 * r + j - l
                s += 1
                ring_to_axial[(r,k)] = (l,s)
                axial_to_ring[(l,s)] = (r,k)
                # print("0 Ring({},{}) == Axial({},{})".format(r, k, l, s))
            
            # Go through the the inneset ring in current row (60 ~ 120 & 240 ~ 300 degree)
            r = dis2centerLine
            kCenterLine = 4 * r if r > 0 else 1
            for j in range(dis2centerLine):
                k = kCenterLine + (r + j) * int(np.sign(self._ring - 1 - l))
                s += 1
                ring_to_axial[(r,k)] = (l,s)
                axial_to_ring[(l,s)] = (r,k)
            
            # The assembly in line of 60 & 300 degree
            k = 2 * dis2centerLine if self._ring - 1 - l < 0 else 0
            s += 1
            ring_to_axial[(r,k)] = (l,s)
            axial_to_ring[(l,s)] = (r,k)

            # Go from the inner ring to outer ring (300 ~ 60 degree)
            for j in range(self._ring - 1 - dis2centerLine):
                r = 1 + j + dis2centerLine
                k = l + r + 1 - self._ring
                s += 1
                ring_to_axial[(r,k)] = (l,s)
                axial_to_ring[(l,s)] = (r,k)
        
        return ring_to_axial, axial_to_ring

    @property
    def lattice(self) -> list:
        return self._lattice

    def get_matplotlib_figure(self):
        return self._figure
    
    def get_matplotlib_axes(self):
        return self._axes



class RowAppender:

    def __init__(self, lattice: HexLattice) -> None:
        self._idx = dict()
        self._lattice = lattice
        self._axial_to_ring = tuple(lattice.generate_ring_axial_hash()[1].items())
    
    def append(
            self,
            key          : str,
            value        : Any                 = None,
            cell_shape   : str                 = 'hex',     # 'hex': hexagonal, 'circ': circular
            cell_radius  : float               = 0.,        # The radius of circle if cell_shape = 'circ'
            offset       : tuple[float, float] = (0, 0),    # Offset from the cell center
            zorder       : int                 = 1,         # Plot layor priority, same as matplotlib
            color        : str                 = None,
            orientation  : float               = 0.
        ) -> None:        
        current_cell = self.get_current_cell(key=key)
        current_cell[key] = {
            'value'      : value,
            'shape'      : cell_shape,
            'radius'     : cell_radius,
            'offset'     : offset,
            'zorder'     : zorder,
            'color'      : color,
            'orientation': orientation
        }
        self._idx[key] += 1

        # if orientation:
        #     self._lattice.lattice[r][k].orientation = orientation
    
    @property
    def cell_num(self) -> int:
        return len(self._axial_to_ring)

    def get_current_cell(self, key) -> HexCell:
        # Count total number for every single key
        if key not in self._idx:
            self._idx[key] = 0
        try:
            aixal_coor, ring_coor = self._axial_to_ring[self._idx[key]]
        except IndexError:
            raise IndexError("Index {} out of range {}".format(
                self._idx[key], len(self._axial_to_ring)
            ))
        
        r, k = ring_coor
        return self._lattice.lattice[r][k]
