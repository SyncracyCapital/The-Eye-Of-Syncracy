import asyncio
import time

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

# App styling
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# App description markdown
markdown = """<h1 style='font-family: Calibri; text-align: center;'>The Eye of <img 
src="https://images.squarespace-cdn.com/content/v1/63857484f91d71181b02f971/9943adcc-5e69-489f-b4a8-158f20fe0619
/Snycracy_WebLogo.png?format=250w" alt="logo"/></h1> <p style='font-family: Calibri; text-align: center;'><i>The Eye 
of Syncracy, a constant watchful gaze upon the crypto markets. It sees all, the rise and fall of coins, the ebb and 
flow of trading. <br> Beware its all-seeing presence, for it knows the secrets of the market, but reveals them only 
to the select few</i></p>"""

st.markdown(markdown, unsafe_allow_html=True)

# App tabs
crypto_tab, tradfi_tab = st.tabs(['Crypto Markets ₿', 'Traditional Markets 📈'])

crypto_placeholder = st.empty()

with crypto_tab:
    for refresh in range(1_000_000):
        # Collect data from CoinGecko API
        asset_sectors = [syncracy_assets_coingecko, syncracy_opportunistic_assets_coingecko, smart_contract_platforms_coingecko,
                         web3_infra_coingecko, metaverse_coingecko, defi_coingecko, currencies_coingecko, cross_chain_coingecko,
                         layer_2_coingecko, cex_coingecko, meme_coingecko]

        asset_dfs = asyncio.run(retrieve_data_from_cg(asset_sectors))

        # Sector titles
        sector_names = ['Core Portfolio Universe', 'Opportunistic Universe', 'Smart Contract Platforms', 'Web3 Infrastructure',
                        'Metaverse', 'DeFi', 'Currencies', 'Cross-Chain', 'Layer 2', 'CEX', 'Meme']

        # Crypto tab
        with crypto_placeholder.container():
            current_time = time.strftime("%I:%M:%S %p")
            st.write(f'Last updated: {current_time}')
            st.subheader('Sector Performance Summary (24h %)')
            metric_grid = make_grid(4, 3)
            metric_grid = sum(metric_grid, [])
            for metric_df, sector, metric_grid in zip(asset_dfs, sector_names, metric_grid):
                total_sector_market_cap = metric_df.data['MCAP'].sum()
                sector_mcap_weights = metric_df.data['MCAP'] / total_sector_market_cap
                sector_mcap_weighted_24returns = round(sector_mcap_weights.dot(metric_df.data['24h %']), 2)
                sector_mcap_weighted_24returns_color = 'green' if sector_mcap_weighted_24returns > 0 else 'red'
                metric_markdown = f"""<p style='font-family: source code pro; font-size:15px; text-align: left;'>{sector}</p>
                <p style='font-family: source code pro; font-size:40px; text-align: left; color: {sector_mcap_weighted_24returns_color};'> 
                <b>{sector_mcap_weighted_24returns}%</b></p>"""
                with metric_grid:
                    st.markdown(metric_markdown, unsafe_allow_html=True)

            # Make a grid of Streamlit elements for sector data
            sector_grid = make_grid(4, 3)
            sector_grid = sum(sector_grid, [])
            # Display data
            for asset_df, sector, sector_grid in zip(asset_dfs, sector_names, sector_grid):
                with sector_grid:
                    st.subheader(sector)
                    st.dataframe(asset_df, width=1000)
        time.sleep(60*3)
