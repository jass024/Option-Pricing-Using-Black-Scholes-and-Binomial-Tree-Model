import numpy as np
import pandas as pd
from scipy.interpolate import griddata

def calculate_implied_volatility(option_data):
    volatilities = []
    for _, row in option_data.iterrows():
        vol = np.sqrt(2 * abs((np.log(row['underlying_price'] / row['strike_price']) + (row['risk_free_rate'] + row['volatility']**2 / 2) * row['time_to_expiry']) / row['time_to_expiry']))
        volatilities.append(vol)
    option_data['implied_volatility'] = volatilities
    return option_data

def generate_volatility_surface(option_data):
    strikes = option_data['strike_price']
    expiries = option_data['time_to_expiry']
    volatilities = option_data['implied_volatility']

    grid_x, grid_y = np.mgrid[min(strikes):max(strikes):100j, min(expiries):max(expiries):100j]
    grid_z = griddata((strikes, expiries), volatilities, (grid_x, grid_y), method='cubic')

    return grid_x, grid_y, grid_z
