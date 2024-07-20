# Option-Pricing-Using-Black-Scholes-and-Binomial-Tree-Model 🎯
Comparison of Black-Scholes model and the Binomial Tree model in terms of option pricing.


## Overview 📈

This project implements an option pricing model in Python, utilizing financial data to calculate option prices, Greeks, and generate a volatility surface. As a student of Financial Engineering, I built this project to practically implement the Black-Scholes model and Binomial Tree model for option pricing. This project leverages financial and mathematical theories to provide a comprehensive analysis of option pricing strategies using these two models. 


## Features 🌟

- **API Integration:** Fetch market data from Alpha Vantage using an API key.
- **Data Processing:** Load and preprocess option data for analysis.
- **Pricing Models:** Calculate option prices using the Black-Scholes and Binomial Tree models.
- **Risk Metrics:** Compute Greeks (Delta, Gamma, Theta, Vega, Rho) and Implied Volatility.
- **Visualization:** Generate interactive visualizations of option prices and volatility surfaces using Bokeh.

## Prerequisites 📋

Ensure you have the following installed:
- Python 3.x
- Obtain an API key from Alpha Vantage and replace `api_key` in `main.py` with your key.


## Usage 🚀

1. **Run the option pricing model:**

    ```bash
    python main.py
    ```

2. The program fetches market data, processes option data, computes prices, Greeks, and implied volatility, and generates interactive visualizations using Bokeh.

## Directory Structure 📂

- **data/**: Contains CSV files for market and processed option data.
- **src/**: Python source code files:
  - **black_scholes.py**: Black-Scholes pricing model implementation.
  - **binomial_tree.py**: Binomial Tree pricing model implementation.
  - **utils.py**: Utility functions for data processing and calculations.
  - **volatility_surface.py**: Generates the volatility surface.
  - **api_integration.py**: Handles API requests for market data.
    

## Files 📄

- **main.py**: Main script for running the option pricing model.
- **README.md**: This file, providing an overview and instructions for the project.

## Accomplishments 🏆

Through this project, we accomplished the following:

1. **Price Calculation:**
   - Calculated option prices using two models:
     - **Black-Scholes Model**
     - **Binomial Tree Model**
   - Observed the differences in option pricing between these models. For example, in our data, the average difference between the Black-Scholes price and the Binomial Tree price was `0.18%`. The difference suggests that, while both models provide very close estimates, they are not identical due to their differing assumptions and methods.

2. **Risk Metrics:**
   - Computed key risk metrics (Greeks) such as Delta, Gamma, Theta, Vega, and Rho.
   - These metrics help in understanding the sensitivity of the option price to various factors.

3. **Implied Volatility:**
   - Calculated implied volatility for the options, providing insights into the market's expectations of future volatility.

4. **Volatility Surface:**
   - Generated a volatility surface to visualize how implied volatility changes with different strike prices and times to expiry.

### Insights from Pricing Models 💡

- **Black-Scholes Model:**
  - Assumes a constant volatility and provides a closed-form solution for European options.
  - Useful for its simplicity and quick calculations.

- **Binomial Tree Model:**
  - More flexible as it can handle American options and varying volatility.
  - Provides a step-by-step approach to option pricing, which can be more accurate for certain types of options.

### Benefits of Using These Models 📊

- **Black-Scholes Model:**
  - Helps in quickly determining theoretical prices of European options.
  - Useful for initial estimations and comparisons.

- **Binomial Tree Model:**
  - Offers more detailed insights, especially for American options or options with varying conditions.
  - Allows for more accurate pricing under different scenarios.

## Contributing 🤝

Contributions are welcome! Follow these steps:
- Fork the repository, create a new branch for your changes.
- Make your modifications and submit a pull request with a clear description.

## License 📄

This project is licensed under the [GNU GPL-3.0](https://www.gnu.org/licenses/) License. See the LICENSE file for details.

## Contact 📬

For questions or feedback, contact:
- [ Email ](jasswindersingh024@gmail.com)
- [ LinkedIn ](https://www.linkedin.com/in/jasswindersingh024)
