from pyrevit import forms
import requests

# Define function to fetch Ethereum info
def get_ethereum_info():
    API_KEY = "23FFET6VUG68K6YVED9RF6P79BAU8KV4ZV"
    ETH_PRICE_URL = (
        f"https://api.etherscan.io/api?module=stats&action=ethprice&apikey={API_KEY}"
    )
    GAS_PRICE_URL = f"https://api.etherscan.io/api?module=proxy&action=eth_gasPrice&apikey={API_KEY}"

    eth_price_response = requests.get(ETH_PRICE_URL).json()
    gas_price_response = requests.get(GAS_PRICE_URL).json()

    eth_price = float(eth_price_response["result"]["ethusd"])
    gas_price_wei = int(gas_price_response["result"], 16)  # Convert hex to int
    gas_price_gwei = gas_price_wei / 10 ** 9  # Convert wei to gwei

    return eth_price, gas_price_gwei


# Fetch the info
eth_price, gas_price = get_ethereum_info()

# Display the results
message = f"Ethereum Price: ${eth_price}\nGas Price: {gas_price} Gwei"
forms.alert(message, title="Ethereum Info", ok=True, warn_icon=True)
