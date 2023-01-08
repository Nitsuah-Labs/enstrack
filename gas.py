import requests
import json
import os
from dotenv import load_dotenv
# automatic detection
from ens.auto import ns

load_dotenv()

API_KEY = os.getenv('ETHERSCAN_API_KEY')
ENS_NAME = os.getenv('ENS_NAME')
print(ENS_NAME)

# Use the web3.eth.ens API to resolve the name to an address
eth_address = ns.address('{ENS_NAME}')
# Print the address
print(f"The address for {ENS_NAME} is {eth_address}")