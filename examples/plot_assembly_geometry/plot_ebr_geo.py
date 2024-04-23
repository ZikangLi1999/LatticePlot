"""
Plot the geomery of assembly in EBR-II
@Author: LZK
@Date: 2023-6-20
"""
import os
import sys
package_path = os.path.dirname(os.getcwd())
sys.path.append(package_path)

import numpy as np
from HexLattice import *

FUEL_DIAMETER = 0.3302
GAP_DIAMETER  = FUEL_DIAMETER + 2 * 0.0254
CLAD_DIAMETER = 0.4420
WIRE_DIAMETER = 0.1245
WIRE_OFFSET   = 0.5 * (CLAD_DIAMETER + WIRE_DIAMETER)
TUBE_DIAMETER = 5.8166
THICKNESS     = 0.1016
IN_TUBE_DIAMETER = 4.8260

POISON_SLUG_DIAMETER  = 1.3754
POISON_GAP            = 0.01715
POISON_GAP_DIAMETER   = POISON_SLUG_DIAMETER + 2 * POISON_GAP
POISON_CLAD_DIAMETER  = 1.5875
POISON_WIRE_DIAMETER  = 0.0762
POISON_WIRE_OFFSET    = 0.5 * (POISON_CLAD_DIAMETER + POISON_WIRE_DIAMETER)

orientation = - math.pi / 6

def plot_driver():
    lattice = HexLattice(ring=6, pitch=0.5665)
    lattice.generate_lattice()
    appender = RowAppender(lattice=lattice)

    color = dict()
    radius = dict()

    # Driver assmebly
    for idx in range(91):
        appender.append(
            key = 'clad',
            # value = 30.,
            cell_shape = 'circ',
            cell_radius = 0.5 * CLAD_DIAMETER,
            zorder = 3,
            color = 'cyan'
        )
        appender.append(
            key = 'gap',
            cell_shape = 'circ',
            cell_radius = 0.5 * GAP_DIAMETER,
            zorder = 4,
            color = 'gray'
        )
        appender.append(
            key = 'fuel',
            # value = 100.,
            cell_shape = 'circ',
            cell_radius = 0.5 * FUEL_DIAMETER,
            zorder = 5,
            color = 'red'
        )
        appender.append(
            key = 'wire',
            cell_shape = 'circ',
            cell_radius = 0.25 * WIRE_DIAMETER,
            offset = WIRE_OFFSET * np.array([0.5*np.sqrt(3), 0.5]),
            zorder = 4,
            color = 'orange'
        )
        if idx == 45:
            color['tube'] = 'cyan'
            color['coolant'] = 'gray'
            zorder = 2
            radius['tube'] = TUBE_DIAMETER
            radius['coolant'] = TUBE_DIAMETER - 2 * THICKNESS
        else:
            color['tube'] = '#FFFFFF'
            color['coolant'] = '#FFFFFF'
            zorder = 1
            radius['tube'] = 1E-24
            radius['coolant'] = 1E-24
        for key in color.keys():
            appender.append(
                key = key,
                cell_shape = 'hex',
                cell_radius = radius[key],
                zorder = zorder,
                color = color[key],
                orientation = orientation
            )

    lattice.plot(
        keys = 'tube&coolant&clad&gap&fuel&wire',
        save_path = 'plot/EBR-II/geo_driver.png',
        color_map = 'jet',
        show_wireframe = False,
        show_axis = False,
        show_colorbar = False,
        dpi = 400
    )

def plot_half_worth_driver():
    lattice = HexLattice(ring=6, pitch=0.5665)
    lattice.generate_lattice()
    appender = RowAppender(lattice=lattice)

    color = dict()
    radius = dict()

    # Driver assmebly
    for idx in range(91):
        if idx % 2 == 1:
            color['fuel'] = 'cyan'
        else:
            color['fuel'] = 'red'
        appender.append(
            key = 'clad',
            # value = 30.,
            cell_shape = 'circ',
            cell_radius = 0.5 * CLAD_DIAMETER,
            zorder = 3,
            color = 'cyan'
        )
        appender.append(
            key = 'gap',
            cell_shape = 'circ',
            cell_radius = 0.5 * GAP_DIAMETER,
            zorder = 4,
            color = 'gray'
        )
        appender.append(
            key = 'fuel',
            # value = 100.,
            cell_shape = 'circ',
            cell_radius = 0.5 * FUEL_DIAMETER,
            zorder = 5,
            color = color['fuel']
        )
        appender.append(
            key = 'wire',
            cell_shape = 'circ',
            cell_radius = 0.25 * WIRE_DIAMETER,
            offset = WIRE_OFFSET * np.array([0.5*np.sqrt(3), -0.5]),
            zorder = 4,
            color = 'orange'
        )
        if idx == 45:
            color['tube'] = 'cyan'
            color['coolant'] = 'gray'
            zorder = 2
            radius['tube'] = TUBE_DIAMETER
            radius['coolant'] = TUBE_DIAMETER - 2 * THICKNESS
        else:
            color['tube'] = '#FFFFFF'
            color['coolant'] = '#FFFFFF'
            zorder = 1
            radius['tube'] = 1E-24
            radius['coolant'] = 1E-24
        for key in radius.keys():
            appender.append(
                key = key,
                cell_shape = 'hex',
                cell_radius = radius[key],
                zorder = zorder,
                color = color[key],
                orientation = orientation
            )

    lattice.plot(
        keys = 'tube&coolant&clad&gap&fuel&wire',
        save_path = 'plot/EBR-II/geo_half_worth_driver.png',
        color_map = 'jet',
        show_wireframe = False,
        show_axis = False,
        show_colorbar = False,
        dpi = 400
    )

def plot_control():
    lattice = HexLattice(ring=5, pitch=0.5665)
    lattice.generate_lattice()
    appender = RowAppender(lattice=lattice)

    color = dict()
    radius = dict()

    # Driver assmebly
    for idx in range(61):
        appender.append(
            key = 'clad',
            # value = 30.,
            cell_shape = 'circ',
            cell_radius = 0.5 * CLAD_DIAMETER,
            zorder = 3,
            color = 'cyan'
        )
        appender.append(
            key = 'gap',
            cell_shape = 'circ',
            cell_radius = 0.5 * GAP_DIAMETER,
            zorder = 4,
            color = 'gray'
        )
        appender.append(
            key = 'fuel',
            # value = 100.,
            cell_shape = 'circ',
            cell_radius = 0.5 * FUEL_DIAMETER,
            zorder = 5,
            color = 'red'
        )
        appender.append(
            key = 'wire',
            cell_shape = 'circ',
            cell_radius = 0.25 * WIRE_DIAMETER,
            offset = WIRE_OFFSET * np.array([0.5*np.sqrt(3), 0.5]),
            zorder = 4,
            color = 'orange'
        )
        if idx == 30:
            color['tube'] = 'cyan'
            color['coolant'] = 'gray'
            color['tube-inner'] = 'cyan'
            color['coolant-inner'] = 'gray'
            color['blank'] = '#FFFFFF'
            zorder = 2
            radius['tube'] = TUBE_DIAMETER
            radius['coolant'] = TUBE_DIAMETER - 2 * THICKNESS
            radius['tube-inner'] = IN_TUBE_DIAMETER
            radius['coolant-inner'] = IN_TUBE_DIAMETER - 2 * THICKNESS
            radius['blank'] = TUBE_DIAMETER + 6 * THICKNESS
        else:
            color['tube'] = '#FFFFFF'
            color['coolant'] = '#FFFFFF'
            color['tube-inner'] = '#FFFFFF'
            color['coolant-inner'] = '#FFFFFF'
            color['blank'] = '#FFFFFF'
            zorder = 1
            radius['tube'] = 1E-24
            radius['coolant'] = 1E-24
            radius['tube-inner'] = 1E-24
            radius['coolant-inner'] = 1E-24
            radius['blank'] = 1E-24
        for key in color.keys():
            appender.append(
                key = key,
                cell_shape = 'hex',
                cell_radius = radius[key],
                zorder = zorder,
                color = color[key],
                orientation = orientation
            )

    lattice.plot(
        keys = 'blank&tube&coolant&tube-inner&coolant-inner&clad&gap&fuel&wire',
        save_path = 'plot/EBR-II/geo_control.png',
        color_map = 'jet',
        show_wireframe = False,
        show_axis = False,
        show_colorbar = False,
        xlim = (-3.5, 3.5),
        ylim = (-3.5, 3.5),
        figsize = (9, 9),
        dpi = 400
    )

def plot_poison():
    lattice = HexLattice(ring=2, pitch=1.664)
    lattice.generate_lattice()
    appender = RowAppender(lattice=lattice)

    color = dict()
    radius = dict()

    # Driver assmebly
    for idx in range(7):
        appender.append(
            key = 'clad',
            # value = 30.,
            cell_shape = 'circ',
            cell_radius = 0.5 * POISON_CLAD_DIAMETER,
            zorder = 3,
            color = 'cyan'
        )
        appender.append(
            key = 'gap',
            cell_shape = 'circ',
            cell_radius = 0.5 * POISON_GAP_DIAMETER,
            zorder = 4,
            color = 'gray'
        )
        appender.append(
            key = 'fuel',
            # value = 100.,
            cell_shape = 'circ',
            cell_radius = 0.5 * POISON_SLUG_DIAMETER,
            zorder = 5,
            color = 'purple'
        )
        appender.append(
            key = 'wire',
            cell_shape = 'circ',
            cell_radius = 0.25 * POISON_WIRE_DIAMETER,
            offset = POISON_WIRE_OFFSET * np.array([0.5*np.sqrt(3), 0.5]),
            zorder = 4,
            color = 'orange'
        )
        if idx == 3:
            color['tube'] = 'cyan'
            color['coolant'] = 'gray'
            color['tube-inner'] = 'cyan'
            color['coolant-inner'] = 'gray'
            # color['blank'] = '#FFFFFF'
            zorder = 2
            radius['tube'] = TUBE_DIAMETER
            radius['coolant'] = TUBE_DIAMETER - 2 * THICKNESS
            radius['tube-inner'] = IN_TUBE_DIAMETER
            radius['coolant-inner'] = IN_TUBE_DIAMETER - 2 * THICKNESS
            # radius['blank'] = TUBE_DIAMETER + 6 * THICKNESS
        else:
            color['tube'] = '#FFFFFF'
            color['coolant'] = '#FFFFFF'
            color['tube-inner'] = '#FFFFFF'
            color['coolant-inner'] = '#FFFFFF'
            # color['blank'] = '#FFFFFF'
            zorder = 1
            radius['tube'] = 1E-24
            radius['coolant'] = 1E-24
            radius['tube-inner'] = 1E-24
            radius['coolant-inner'] = 1E-24
            # radius['blank'] = 1E-24
        for key in color.keys():
            appender.append(
                key = key,
                cell_shape = 'hex',
                cell_radius = radius[key],
                zorder = zorder,
                color = color[key],
                orientation = orientation
            )

    lattice.plot(
        keys = 'tube&coolant&tube-inner&coolant-inner&clad&gap&fuel&wire',
        save_path = 'plot/EBR-II/geo_poison.png',
        color_map = 'jet',
        show_wireframe = False,
        show_axis = False,
        show_colorbar = False,
        xlim = (-3.5, 3.5),
        ylim = (-3.5, 3.5),
        figsize = (9, 9),
        dpi = 400
    )

def plot_1D_eq():
    lattice = HexLattice(ring=1, pitch=1.664)
    lattice.generate_lattice()
    appender = RowAppender(lattice=lattice)

    color = dict()
    radius = dict()

    # Driver assmebly
    for ring in range(6):
        appender.append(
            key = 'clad',
            # value = 30.,
            cell_shape = 'circ',
            cell_radius = 0.5 * POISON_CLAD_DIAMETER,
            zorder = 3,
            color = 'cyan'
        )
        appender.append(
            key = 'gap',
            cell_shape = 'circ',
            cell_radius = 0.5 * POISON_GAP_DIAMETER,
            zorder = 4,
            color = 'gray'
        )
        appender.append(
            key = 'fuel',
            # value = 100.,
            cell_shape = 'circ',
            cell_radius = 0.5 * POISON_SLUG_DIAMETER,
            zorder = 5,
            color = 'purple'
        )
        appender.append(
            key = 'wire',
            cell_shape = 'circ',
            cell_radius = 0.25 * POISON_WIRE_DIAMETER,
            offset = POISON_WIRE_OFFSET * np.array([0.5*np.sqrt(3), 0.5]),
            zorder = 4,
            color = 'orange'
        )

    # color['tube'] = 'cyan'
    # color['coolant'] = 'gray'
    # color['tube-inner'] = 'cyan'
    # color['coolant-inner'] = 'gray'
    # # color['blank'] = '#FFFFFF'
    # zorder = 2
    # radius['tube'] = TUBE_DIAMETER
    # radius['coolant'] = TUBE_DIAMETER - 2 * THICKNESS
    # radius['tube-inner'] = IN_TUBE_DIAMETER
    # radius['coolant-inner'] = IN_TUBE_DIAMETER - 2 * THICKNESS
    # # radius['blank'] = TUBE_DIAMETER + 6 * THICKNESS

    # for key in color.keys():
    #     appender.append(
    #         key = key,
    #         cell_shape = 'hex',
    #         cell_radius = radius[key],
    #         zorder = zorder,
    #         color = color[key],
    #         orientation = orientation
    #     )

    lattice.plot(
        keys = 'tube&coolant&tube-inner&coolant-inner&clad&gap&fuel&wire',
        save_path = 'plot/EBR-II/geo_poison.png',
        color_map = 'jet',
        show_wireframe = False,
        show_axis = False,
        show_colorbar = False,
        xlim = (-3.5, 3.5),
        ylim = (-3.5, 3.5),
        figsize = (9, 9),
        dpi = 400
    )



if __name__ == '__main__':
    plot_driver()
    # plot_half_worth_driver()
    # plot_control()
    # plot_poison()
