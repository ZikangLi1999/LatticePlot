import os
import sys
import pathlib

package_path = os.getcwd()
sys.path.append(package_path)
from HexLattice import *


MAX_ANISO_ORDER = 3
CORE_RING = 15
LATTICE_PITCH = 5.8877

lattice = HexLattice(ring=CORE_RING, pitch=2 * LATTICE_PITCH)
lattice.generate_lattice()

lattice.lattice


# Plot core configuration
print(f"Plotting core configuration ...")
lattice.plot(
    keys = f'core_config',
    color_map = 'jet',
    save_path = pathlib.Path(os.getcwd()).parent / f'gallery/ebr_core_config.png',
    figsize = (11, 8),
    text_size = 8,
    dpi = 600
)

print("Done.")
