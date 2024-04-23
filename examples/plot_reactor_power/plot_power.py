import os
import sys

package_path = os.getcwd()
sys.path.append(package_path)
from HexLattice import *
from power_data import *

lattice = HexLattice(ring=CORE_RING, pitch=2 * LATTICE_PITCH)
lattice.generate_lattice()
appender = RowAppender(lattice=lattice)

max_relerr : list[float] = [0. for _ in range(1 + MAX_ANISO_ORDER)]
max_postive_err : float = 0.
max_negative_err : float = 0.

# #################################################################
#                    Add data into lattice
# #################################################################
r : int = CORE_RING - 1
print("Processing data ...")
for c in range(appender.cell_num):
    for i in range(1 + MAX_ANISO_ORDER):
        # Append power of Pi into lattice
        appender.append(key = f'P{i}', value = power_p[i][c])

        # Append power of reference into lattice
        relerr: float = (power_p[i][c] - power_ref[c]) \
            / power_ref[c] if power_ref[c] > 0. else 0.
        appender.append(
            key = f'relerr{i}',
            value = relerr
        )

        # Record the maximum relative error
        if abs(relerr) > max_relerr[i]:
            max_relerr[i] = abs(relerr)
        if relerr > max_postive_err: max_postive_err = relerr
        if relerr < max_negative_err: max_negative_err = relerr


for i in range(1 + MAX_ANISO_ORDER):
    print(f"Maximum relative error of P{i} is {max_relerr[i]}")


plot_directory = os.path.join(os.getcwd(), 'plot')
if not os.path.exists(plot_directory):
    os.mkdir(plot_directory)

# #################################################################
#                              Plot
# #################################################################
for i in range(1 + MAX_ANISO_ORDER):
    print(f"Plotting P{i} case ...")
    lattice.plot(
        keys = f'P{i}',
        color_map = 'jet',
        save_path = os.path.join(plot_directory, f'power_p{i}.png'),
        figsize = (11, 8),
        text_size = 8,
        dpi = 600,
        max_ring_idx = 7,
        data_fmt = 'E'
    )
    lattice.plot(
        keys = f'relerr{i}',
        color_map = 'jet',
        save_path = os.path.join(plot_directory, f'power_relerr{i}.png'),
        figsize = (11, 8),
        text_size = 8,
        dpi = 600,
        max_ring_idx = 7,
        clim = (max_negative_err, max_postive_err),
        data_fmt = '%'
    )

lattice.plot(
    keys = f'ref',
    color_map = 'jet',
    save_path = os.path.join(plot_directory, f'power_ref.png'),
    figsize = (11, 8),
    text_size = 8,
    dpi = 600,
    max_ring_idx = 7
)

# Plot core configuration
print(f"Plotting core configuration ...")
lattice.plot(
    keys = f'core_config',
    color_map = 'jet',
    save_path = os.path.join(plot_directory, f'plot/core_config.png'),
    figsize = (11, 8),
    text_size = 8,
    dpi = 600
)

print("Done.")
