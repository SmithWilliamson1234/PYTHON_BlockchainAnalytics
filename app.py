import streamlit as st
import requests
import pandas as pd

# Set the app layout to full width
st.set_page_config(layout="wide")
# CoinMarketCap API parameters
API_KEY = 'YOUR_API_KEY_HERE'
API_BASE_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
PARAMS = {
    'start': 1,
    'limit': 50,
    'convert': 'USD',
    'sort': 'market_cap',
    'sort_dir': 'desc',
    'CMC_PRO_API_KEY': API_KEY,
}

# CoinMarketCap API parameters for new cryptocurrencies
NEW_COINS_PARAMS = {
    'start': 51,
    'limit': 50,
    'convert': 'USD',
    'sort': 'date_added',
    'sort_dir': 'desc',
    'CMC_PRO_API_KEY': API_KEY,
}

# CoinMarketCap API parameters for top trending cryptocurrencies
TRENDING_COINS_PARAMS = {
    'start': 101,
    'limit': 50,
    'convert': 'USD',
    'sort': 'percent_change_24h',
    'sort_dir': 'desc',
    'CMC_PRO_API_KEY': API_KEY,
}

# Streamlit app title
st.title('Cryptocurrency Dashboard')

# Create columns for layout
col1, col2, col3 = st.columns(3)

# Fetch data from CoinMarketCap API
response = requests.get(API_BASE_URL, params=PARAMS)
data = response.json()

new_coins_response = requests.get(API_BASE_URL, params=NEW_COINS_PARAMS)
new_coins_data = new_coins_response.json()

trending_coins_response = requests.get(API_BASE_URL, params=TRENDING_COINS_PARAMS)
trending_coins_data = trending_coins_response.json()

if 'data' in data and 'data' in new_coins_data and 'data' in trending_coins_data:
    top_50_data = data['data']
    new_coins_data = new_coins_data['data']
    trending_coins_data = trending_coins_data['data']

    # Create DataFrames from the API responses
    crypto_data = pd.DataFrame({
        'Name': [crypto['name'] for crypto in top_50_data],
        'Symbol': [crypto['symbol'] for crypto in top_50_data],
        'Price (USD)': [crypto['quote']['USD']['price'] for crypto in top_50_data],
        'Market Cap (USD)': [crypto['quote']['USD']['market_cap'] for crypto in top_50_data],
        '24h Trading Volume (USD)': [crypto['quote']['USD']['volume_24h'] for crypto in top_50_data],
        '1d Change (%)': [crypto['quote']['USD']['percent_change_24h'] for crypto in top_50_data],
        '7d Change (%)': [crypto['quote']['USD']['percent_change_7d'] for crypto in top_50_data],
        '1m Change (%)': [crypto['quote']['USD']['percent_change_30d'] for crypto in top_50_data],
    })

    new_coins_df = pd.DataFrame({
        'Name': [crypto['name'] for crypto in new_coins_data],
        'Symbol': [crypto['symbol'] for crypto in new_coins_data],
        'Price (USD)': [crypto['quote']['USD']['price'] for crypto in new_coins_data],
        '1d Change (%)': [crypto['quote']['USD']['percent_change_24h'] for crypto in new_coins_data],
        '7d Change (%)': [crypto['quote']['USD']['percent_change_7d'] for crypto in new_coins_data],
        '1m Change (%)': [crypto['quote']['USD']['percent_change_30d'] for crypto in new_coins_data],
    })

    trending_coins_df = pd.DataFrame({
        'Name': [crypto['name'] for crypto in trending_coins_data],
        'Symbol': [crypto['symbol'] for crypto in trending_coins_data],
        'Price (USD)': [crypto['quote']['USD']['price'] for crypto in trending_coins_data],
        '1d Change (%)': [crypto['quote']['USD']['percent_change_24h'] for crypto in trending_coins_data],
        '7d Change (%)': [crypto['quote']['USD']['percent_change_7d'] for crypto in trending_coins_data],
        '1m Change (%)': [crypto['quote']['USD']['percent_change_30d'] for crypto in trending_coins_data],

    })

    # Display top 50 cryptocurrencies in the first column
    col1.title('Top 50 Cryptocurrencies')
    col1.dataframe(crypto_data.set_index('Name'))

    # Display new cryptocurrencies in the second column
    col2.title('New Cryptocurrencies')
    col2.dataframe(new_coins_df.set_index('Name'))

    # Display top trending cryptocurrencies in the third column
    col3.title('Top Trending Cryptocurrencies')
    col3.dataframe(trending_coins_df.set_index('Name'))

else:
    st.error('Failed to retrieve data from CoinMarketCap API.')
