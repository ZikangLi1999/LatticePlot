"""
Get power data from Excel file 'reactor_result.xlsx'

@Author: LI Zikang
@Date; 2023-11-1
"""
import os
import numpy as np
import pandas as pd
from typing import Union

MAX_ANISO_ORDER = 3
CORE_RING = 6
LATTICE_PITCH = 5.8877

def normalize(data: Union[list[float], np.ndarray]) -> list[float]:
    data_ : np.ndarray = np.array(data)
    data_ = data_ / sum(data_)
    assert round(sum(data_), 0) == 1.
    data = data_.tolist()
    return data


file = os.path.join(os.getcwd(), 'examples', 'plot_reactor_power', 'reactor_result.xlsx')

# Reference power
power : pd.DataFrame = pd.read_excel(file, sheet_name='power', dtype=float)
power_ref : np.ndarray = power['ref']
power_ref = normalize(power_ref)

# SARAX power
power_p : np.ndarray = np.zeros(shape=(1 + MAX_ANISO_ORDER, len(power_ref)))
for i in range(1 + MAX_ANISO_ORDER):
    power_p[i] = normalize(power[f'P{i}'])
    print(f"Power data of P{i} case gotten.")
