from typing import List

import pandas as pd
from pycoingecko import CoinGeckoAPI
import asyncio

import streamlit as st
import requests


def big_number_formatter(x):
    """The two args are the value and tick position."""
    formatter_thresholds = 1_000_000_000
    if x < formatter_thresholds:
        return '${:1.1f}M'.format(x * 1e-6)
    else:
        return '${:1.1f}B'.format(x * 1e-9)


def convert_cg_resp_to_df(resp):
    """
    Convert CoinGecko response to pandas dataframe
    :param resp: CoinGecko response
    :return: pandas dataframe Styler
    """
    cols_to_keep = ['symbol', 'current_price', 'total_volume', 'market_cap', 'fully_diluted_valuation',
                    'price_change_percentage_24h_in_currency', 'price_change_percentage_7d_in_currency',
                    'price_change_percentage_30d_in_currency']
    col_names = ['Symbol', 'Price', '24h Vol', 'MCAP', 'FDV', '24h %', '7d %', '30d %']
    asset_df = pd.DataFrame(resp)
    asset_df = asset_df[cols_to_keep]
    asset_df.columns = col_names
    asset_df['Symbol'] = asset_df['Symbol'].str.upper()
    asset_df.set_index('Symbol', inplace=True)
    return asset_df.style.format({'Price': '${:,.2f}',
                                  '24h Vol': big_number_formatter,
                                  'MCAP': big_number_formatter,
                                  'FDV': big_number_formatter,
                                  '24h %': '{:.2f}%',
                                  '7d %': '{:.2f}%',
                                  '30d %': '{:.2f}%'}, na_rep='MISS').applymap(highlight_percent_returns,
                                                                               subset=['24h %', '7d %', '30d %'])


async def fetch_cg_data(assets):
    """
    Fetch data from CoinGecko API sorted by market cap
    :param assets: list of strings with CoinGecko IDs
    :return: Coingecko response
    """
    MARKETS_BASE_URL = 'https://pro-api.coingecko.com/api/v3/coins/markets'
    payload = {'ids': ','.join(assets),
               'vs_currency': 'USD',
               'order': 'market_cap_desc',
               'price_change_percentage': '24h,7d,30d',
               'x_cg_pro_api_key': st.secrets['COINGECKO_API_KEY']}
    asset_info_resp = requests.get(MARKETS_BASE_URL, params=payload).json()
    return asset_info_resp


async def retrieve_data_from_cg(coingecko_asset_lists: List):
    """
    Retrieve data from CoinGecko API
    :param coingecko_asset_lists: list of lists of CoinGecko IDs
    :return: list of pandas dataframes
    """
    tasks = [fetch_cg_data(cg_ids) for cg_ids in coingecko_asset_lists]
    asset_info_resp = await asyncio.gather(*tasks)

    asset_dfs = [convert_cg_resp_to_df(resp) for resp in asset_info_resp]
    return asset_dfs


def highlight_percent_returns(cell):
    """
    Highlight negative values as red and positive values as green
    """
    if type(cell) != str and cell < 0:
        return 'color: red'
    else:
        return 'color: green'


def make_grid(cols, rows):
    """
    Make a grid of Streamlit elements
    :param cols: number of columns
    :param rows: number of rows
    :return: list of Streamlit elements
    """
    grid = [0] * cols
    for i in range(cols):
        with st.container():
            grid[i] = st.columns(rows)
    return grid
