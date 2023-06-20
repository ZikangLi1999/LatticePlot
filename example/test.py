# from ..HexLattice import *

import os
import sys
package_path = os.path.dirname(os.getcwd())
sys.path.append(package_path)

from HexLattice import *

CASE = 5

if CASE == 1:
    point = CubeCoordinate(value=(-1, +2, -1))
    print(point)
    point_off = point.to_offset()
    print(point_off)
    point_cube = point_off.to_cube()
    print(point_cube)
    point_ring = point.to_ring()
    print(point_ring)
    print(point_ring.to_cube())

    print("\nNeighbours:")
    for neighbour in point.get_all_neighbours():
        print(neighbour)

    print("\nRing:")
    for k in point.get_ring():
        print(k)

    # point_invalid = CubeCoordinate(x=1, y=1, z=0)

elif CASE == 2:
    point = HexCell(
        positon = CubeCoordinate(value=(+1, 0, -1)),
        pitch = 1.0
    )
    print(point)
    print("Central point:", point.central_point)
    print("Surrounding points:")
    for p in point.surround_points:
        print(p)

elif CASE == 3:
    lattice = HexLattice(ring=5, pitch=1.0)
    lattice.genertate_lattice()
    for r, ring in enumerate(lattice.lattice):
        for k, point in enumerate(ring):
            print(f"({r+1}, {k+1}): {point}")
    
    lattice.plot()

elif CASE == 4:
    lattice = HexLattice(ring=2, pitch=1.0)
    lattice.genertate_lattice()
    ring_to_axial, axial_to_ring = lattice.generate_ring_axial_hash()

    print(ring_to_axial)
    print(axial_to_ring)

    ring_coor = (1, 3)
    axial_coor = (2, 0)
    print(ring_to_axial[ring_coor])
    print(axial_to_ring[axial_coor])

elif CASE == 5:
    lattice = HexLattice(ring=3, pitch=1.0)
    lattice.genertate_lattice()
    appender = RowAppender(lattice=lattice)

    for i in range(appender.cell_num):
        appender.append(key='id', value=i+3.14)
    
    lattice.plot(key='id', text_size=16, max_ring_idx=2)
