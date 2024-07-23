import os
import sys
import requests
import pandas as pd
import numpy as np
from bokeh.plotting import figure, output_file, show, save
from bokeh.layouts import gridplot
from bokeh.models import HoverTool, ColorBar, LinearColorMapper, ColumnDataSource
from bokeh.io import output_notebook

# Set the PYTHONPATH to the root directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.black_scholes import black_scholes_price
from src.binomial_tree import binomial_tree_price
from src.utils import load_option_data, calculate_greeks, calculate_implied_volatility
from src.volatility_surface import generate_volatility_surface
from src.api_integration import fetch_market_data

# Provide your API key and the stock symbol
api_key = 'O759BZZDY3HB5UMN'
symbol = 'AAPL'

# Ensure the data directory exists
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, 'data')
if not os.path.exists(data_dir):
    os.makedirs(data_dir)
    print(f"Created directory: {data_dir}")
else:
    print(f"Directory already exists: {data_dir}")

# Fetch market data and save to CSV
csv_path = fetch_market_data(api_key, symbol)
print(f"Market data saved to {csv_path}")

# Load and preprocess option data
option_data = load_option_data(symbol)
print(f"Option data loaded: {option_data.head()}")  # Print the first few rows to check

# Calculate option prices
option_data['BS_Price'] = option_data.apply(
    lambda row: black_scholes_price(
        S=row['close'],
        K=row['strike_price'],
        T=row['time_to_expiry'],
        r=row['risk_free_rate'],
        sigma=row['volatility'],
        option_type=row['option_type']
    ), axis=1
)

# Ensure BS_Price column is calculated
print(f"BS_Price column added: {option_data[['BS_Price']].head()}")

# Calculate option prices using Binomial Tree model
option_data['BT_Price'] = option_data.apply(
    lambda row: binomial_tree_price(
        S=row['close'],
        K=row['strike_price'],
        T=row['time_to_expiry'],
        r=row['risk_free_rate'],
        sigma=row['volatility'],
        option_type=row['option_type']
    ), axis=1
)

# Ensure BT_Price column is calculated
print(f"BT_Price column added: {option_data[['BT_Price']].head()}")

# Calculate Greeks and Implied Volatility
option_data = calculate_greeks(option_data)
option_data = calculate_implied_volatility(option_data)

# Ensure Greeks and Implied Volatility are calculated
print(f"Option data with Greeks and Implied Volatility: {option_data[['implied_volatility', 'delta', 'gamma', 'theta', 'vega', 'rho']].head()}")

# Generate volatility surface
grid_x, grid_y, grid_z = generate_volatility_surface(option_data)

# Calculate the absolute percentage difference between BS_Price and BT_Price
option_data['Price_Difference_Percent'] = abs((option_data['BS_Price'] - option_data['BT_Price']) / option_data['BS_Price']) * 100

# Calculate the average percentage difference
average_difference_percent = option_data['Price_Difference_Percent'].mean()

print(f"The average difference between the Black-Scholes price and the Binomial Tree price is {average_difference_percent:.2f}%")

# Save the processed data for future use
output_path = os.path.join(data_dir, f'{symbol}_processed_option_data.csv')
print(f"Saving processed option data to {output_path}")

try:
    option_data.to_csv(output_path, index=False)
    print("Processed option data saved successfully.")
except PermissionError as e:
    print(f"Permission error: {e}")

# Interactive plot with Bokeh

# Option Prices Comparison Plot
source1 = ColumnDataSource(data=dict(
    index=option_data.index,
    BS_Price=option_data['BS_Price'],
    BT_Price=option_data['BT_Price']
))

hover1 = HoverTool(tooltips=[
    ("Index", "@index"),
    ("Black-Scholes Price", "@BS_Price"),
    ("Binomial Tree Price", "@BT_Price")
])

p1 = figure(plot_width=800, plot_height=400, title=f'{symbol} Option Prices Comparison', tools=[hover1, "pan", "wheel_zoom", "box_zoom", "reset", "save"])
p1.line('index', 'BS_Price', source=source1, legend_label='Black-Scholes Price', line_width=2)
p1.circle('index', 'BS_Price', source=source1, size=5)
p1.line('index', 'BT_Price', source=source1, legend_label='Binomial Tree Price', line_width=2, line_dash='dashed', color='red')
p1.circle('index', 'BT_Price', source=source1, size=5, color='red')
p1.xaxis.axis_label = "Date"
p1.yaxis.axis_label = "Option Price"
p1.legend.location = "top_left"

# Volatility Surface Plot
hover2 = HoverTool(tooltips=[
    ("Strike Price", "$x"),
    ("Time to Expiry", "$y"),
    ("Volatility", "@image")
])

mapper = LinearColorMapper(palette="Viridis256", low=np.min(grid_z), high=np.max(grid_z))

p2 = figure(plot_width=800, plot_height=400, title=f'{symbol} Volatility Surface', tools=[hover2, "pan", "wheel_zoom", "box_zoom", "reset", "save"])
p2.image(image=[grid_z], x=min(grid_x.flatten()), y=min(grid_y.flatten()), dw=abs(max(grid_x.flatten()) - min(grid_x.flatten())), dh=abs(max(grid_y.flatten()) - min(grid_y.flatten())), color_mapper=mapper)
p2.xaxis.axis_label = "Strike Price"
p2.yaxis.axis_label = "Time to Expiry"
color_bar = ColorBar(color_mapper=mapper, location=(0, 0))
p2.add_layout(color_bar, 'right')

# Price Difference Percentage Plot
source3 = ColumnDataSource(data=dict(
    index=option_data.index,
    Price_Difference_Percent=option_data['Price_Difference_Percent']
))

hover3 = HoverTool(tooltips=[
    ("Index", "@index"),
    ("Price Difference Percentage", "@Price_Difference_Percent%")
])

p3 = figure(plot_width=800, plot_height=400, title=f'{symbol} Price Difference Percentage (Black-Scholes vs Binomial Tree)', tools=[hover3, "pan", "wheel_zoom", "box_zoom", "reset", "save"])
p3.line('index', 'Price_Difference_Percent', source=source3, legend_label='Price Difference Percentage', line_width=2, color='green')
p3.circle('index', 'Price_Difference_Percent', source=source3, size=5, color='green')
p3.xaxis.axis_label = "Date"
p3.yaxis.axis_label = "Price Difference Percentage (%)"
p3.legend.location = "top_left"

# Arrange plots in a grid
grid = gridplot([[p1], [p2], [p3]])

# Save and show the plots
output_file(os.path.join(data_dir, f'{symbol}_interactive_plots.html'))
save(grid)
show(grid)