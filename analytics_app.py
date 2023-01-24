import asyncio

import streamlit as st
from utils import retrieve_data_from_cg, make_grid
from asset_lists import syncracy_assets_coingecko, syncracy_opportunistic_assets_coingecko, \
    smart_contract_platforms_coingecko, web3_infra_coingecko, metaverse_coingecko, defi_coingecko, \
    currencies_coingecko, cross_chain_coingecko, layer_2_coingecko, cex_coingecko, meme_coingecko

# App configuration
st.set_page_config(
    page_title="The Eye of Syncracy",
    page_icon="chart_with_upwards_trend",
    layout="wide",
)

# App description markdown
markdown = """<h1 style='font-family: Calibri; text-align: center;'>The Eye of <img 
src="https://images.squarespace-cdn.com/content/v1/63857484f91d71181b02f971/9943adcc-5e69-489f-b4a8-158f20fe0619
/Snycracy_WebLogo.png?format=250w" alt="logo"/></h1> <p style='font-family: Calibri; text-align: center;'><i>The Eye 
of Syncracy, a constant watchful gaze upon the crypto markets. It sees all, the rise and fall of coins, the ebb and 
flow of trading. <br> Beware its all-seeing presence, for it knows the secrets of the market, but reveals them only 
to the select few</i></p> """

st.markdown(markdown, unsafe_allow_html=True)

# App tabs
crypto_tab, tradfi_tab = st.tabs(['Crypto Markets ₿', 'Traditional Markets 📈'])

# Collect data from CoinGecko API
asset_sectors = [syncracy_assets_coingecko, syncracy_opportunistic_assets_coingecko, smart_contract_platforms_coingecko,
                 web3_infra_coingecko, metaverse_coingecko, defi_coingecko, currencies_coingecko, cross_chain_coingecko,
                 layer_2_coingecko, cex_coingecko, meme_coingecko]

st.spinner('Loading data from CoinGecko API...')
asset_dfs = asyncio.run(retrieve_data_from_cg(asset_sectors))

# Sector titles
sector_names = ['Core Portfolio Universe', 'Opportunistic Universe', 'Smart Contract Platforms', 'Web3 Infrastructure',
                'Metaverse', 'DeFi', 'Currencies', 'Cross-Chain', 'Layer 2', 'CEX', 'Meme']

# Crypto tab
with crypto_tab:
    # Make a grid of Streamlit elements
    sector_grid = make_grid(4, 3)
    sector_grid = sum(sector_grid, [])

    # Display data
    for asset_df, sector, sector_grid in zip(asset_dfs, sector_names, sector_grid):
        with sector_grid:
            st.subheader(sector)
            st.dataframe(asset_df, width=1000)
