import requests
import pandas as pd
import os
import numpy as np

def fetch_market_data(api_key, symbol):
    """
    Fetch market data from Alpha Vantage and save to a CSV file.
    """
    base_url = "https://www.alphavantage.co/query"
    params = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': symbol,
        'apikey': api_key,
        'outputsize': 'full'
    }
    response = requests.get(base_url, params=params)
    data = response.json()

    if 'Time Series (Daily)' not in data:
        raise ValueError("Error fetching data from API. Please check the API key and symbol.")

    time_series = data['Time Series (Daily)']
    df = pd.DataFrame.from_dict(time_series, orient='index')
    df.columns = ['open', 'high', 'low', 'close', 'volume']
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()

    # Add dummy data for option pricing
    np.random.seed(0)  # For reproducibility
    num_records = len(df)
    df['strike_price'] = np.random.choice(np.arange(100, 150, 5), num_records)
    df['time_to_expiry'] = np.random.choice(np.arange(30, 365, 30), num_records)
    df['volatility'] = np.random.uniform(0.1, 0.5, num_records)
    df['risk_free_rate'] = 0.01  # Assume a constant risk-free rate
    df['option_type'] = np.random.choice(['call', 'put'], num_records)

     # Define the absolute path to the data directory
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
    data_dir = os.path.join(script_dir, '..', '..', 'data')  # Adjust the path as per your project structure
    
    # Ensure the data directory exists
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"Created directory: {data_dir}")

    # Construct the absolute path to the CSV file
    csv_path = os.path.join(data_dir, f'{symbol}_market_data.csv')
    print(f"Saving market data to {csv_path}")
    
    try:
        df.to_csv(csv_path)
        print(f"Market data successfully saved to {csv_path}")
    except PermissionError as e:
        print(f"Permission error: {e}")


    
    return csv_path
