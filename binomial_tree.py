import numpy as np

def binomial_tree_price(S, K, T, r, sigma, option_type='call', steps=100):
    dt = T / steps
    u = np.exp(sigma * np.sqrt(dt))
    d = 1 / u
    p = (np.exp(r * dt) - d) / (u - d)
    
    option_values = np.zeros((steps + 1, steps + 1))
    
    for i in range(steps + 1):
        option_values[i, steps] = max(0, (S * (u**(steps - i)) * (d**i) - K) if option_type == 'call' else (K - S * (u**(steps - i)) * (d**i)))
    
    for j in range(steps - 1, -1, -1):
        for i in range(j + 1):
            option_values[i, j] = np.exp(-r * dt) * (p * option_values[i, j + 1] + (1 - p) * option_values[i + 1, j + 1])
    
    return option_values[0, 0]
