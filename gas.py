import requests
import json

def generate_transaction_table(ens_address):
    # Resolve the ENS address to a regular Ethereum address
    ens_url = f"https://api.etherscan.io/api?module=ens&action=getAddress&name={ens_address}&apikey=YourApiKeyToken"
    ens_response = requests.get(ens_url)
    address = ens_response.json()["result"]

    # Get the latest block number
    block_number_url = "https://api.etherscan.io/api?module=proxy&action=eth_blockNumber&apikey=YourApiKeyToken"
    block_number_response = requests.get(block_number_url)
    block_number = int(block_number_response.json()["result"], 16)

    # Initialize a list to store the transactions
    transactions = []

    # Iterate over the blocks in reverse order (latest to earliest)
    for i in range(block_number, block_number - 10000, -1):
        # Get the block information
        block_url = f"https://api.etherscan.io/api?module=block&action=getblockreward&blockno={i}&apikey=YourApiKeyToken"
        block_response = requests.get(block_url)
        block_data = block_response.json()["result"]

        # Check if the block has any transactions
        if "transactions" in block_data:
            # Iterate over the transactions in the block
            for transaction in block_data["transactions"]:
                # Check if the transaction was sent to the given address
                if transaction["to"] == address:
                    # Get the transaction details
                    transaction_url = f"https://api.etherscan.io/api?module=proxy&action=eth_getTransactionByHash&txhash={transaction['hash']}&apikey=YourApiKeyToken"
                    transaction_response = requests.get(transaction_url)
                    transaction_data = transaction_response.json()["result"]

                    # Calculate the gas price in US dollars
                    gas_price = int(transaction_data["gasPrice"], 16) / 10**18 * float(transaction_data["price"])

                    # Add the transaction to the list
                    transactions.append({
                        "transaction_id": transaction_data["hash"],
                        "gas_price": gas_price
                    })

    # Print the table header
    print("Transaction ID\tGas Price (USD)")

    # Print the transactions
    for transaction in transactions:
        print(f"{transaction['transaction_id']}\t{transaction['gas_price']:.2f}")

# Test the function
generate_transaction_table("my-name.eth")