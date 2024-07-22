import numpy as np
import pandas as pd
from scipy.optimize import minimize_scalar
from scipy.stats import norm
import os

def load_option_data(symbol):
    """
    Load option data from CSV file.
    """
    file_path = os.path.join('data', f'{symbol}_market_data.csv')
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    df = pd.read_csv(file_path, index_col=0, parse_dates=True)

    required_columns = ['close', 'strike_price', 'time_to_expiry', 'volatility', 'risk_free_rate', 'option_type']
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"Missing required column: {col}")

    return df

def calculate_greeks(option_data):
    """
    Calculate option Greeks and add them to the DataFrame.
    """
    def black_scholes_greeks(S, K, T, r, sigma, option_type):
        """
        Calculate Black-Scholes Greeks for a given option.
        """
        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        if option_type == 'call':
            delta = norm.cdf(d1)
            gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
            theta = (-S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) - r * K * np.exp(-r * T) * norm.cdf(d2)
            vega = S * norm.pdf(d1) * np.sqrt(T)
            rho = K * T * np.exp(-r * T) * norm.cdf(d2)
        elif option_type == 'put':
            delta = norm.cdf(d1) - 1
            gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
            theta = (-S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) + r * K * np.exp(-r * T) * norm.cdf(-d2)
            vega = S * norm.pdf(d1) * np.sqrt(T)
            rho = -K * T * np.exp(-r * T) * norm.cdf(-d2)
        else:
            raise ValueError("Invalid option type. Must be 'call' or 'put'.")
        return delta, gamma, theta, vega, rho

    greeks = option_data.apply(lambda row: black_scholes_greeks(
        S=row['close'],
        K=row['strike_price'],
        T=row['time_to_expiry'],
        r=row['risk_free_rate'],
        sigma=row['volatility'],
        option_type=row['option_type']
    ), axis=1)

    option_data[['delta', 'gamma', 'theta', 'vega', 'rho']] = pd.DataFrame(greeks.tolist(), index=option_data.index)

    return option_data

def calculate_implied_volatility(option_data):
    """
    Calculate implied volatility and add it to the DataFrame.
    """
    def implied_volatility(option_price, S, K, T, r, option_type):
        """
        Calculate the implied volatility for a given option price using numerical methods.
        """
        def objective_function(sigma):
            if option_type == 'call':
                price = black_scholes_call_price(S, K, T, r, sigma)
            else:
                price = black_scholes_put_price(S, K, T, r, sigma)
            return (price - option_price) ** 2

        result = minimize_scalar(objective_function, bounds=(0.01, 5.0), method='bounded')
        return result.x

    option_data['implied_volatility'] = option_data.apply(
        lambda row: implied_volatility(
            option_price=row['BS_Price'],  # Assuming BS_Price is already calculated
            S=row['close'],
            K=row['strike_price'],
            T=row['time_to_expiry'],
            r=row['risk_free_rate'],
            option_type=row['option_type']
        ), axis=1
    )

    return option_data

def black_scholes_call_price(S, K, T, r, sigma):
    """
    Calculate the Black-Scholes price for a call option.
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

def black_scholes_put_price(S, K, T, r, sigma):
    """
    Calculate the Black-Scholes price for a put option.
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
