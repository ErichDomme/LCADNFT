import clr
clr.AddReference("System")
from System import Uri
from System.Net import WebClient
import json

def get_ethereum_price():
    client = WebClient()
    url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
    response = client.DownloadString(Uri(url))
    data = json.loads(response)
    return data['ethereum']['usd']

def get_gas_price():
    client = WebClient()
    url = "https://api.etherscan.io/api?module=proxy&action=eth_gasPrice&apikey=23FFET6VUG68K6YVED9RF6P79BAU8KV4ZV"
    response = client.DownloadString(Uri(url))
    data = json.loads(response)
    gas_price_wei = int(data['result'], 16)
    gas_price_gwei = gas_price_wei / 1e9
    return gas_price_gwei

if __name__ == "__main__":
    eth_price = get_ethereum_price()
    gas_price = get_gas_price()

    print "Current Ethereum Price: $%s" % eth_price
    print "Gas Price: %s Gwei" % gas_price
