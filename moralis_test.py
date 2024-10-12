import requests

api_key = "XXXX"  # Αντικαταστήστε με το API key σας από το Moralis

def get_eth_tokens(address):
    url = f"https://deep-index.moralis.io/api/v2/{address}/erc20"
    headers = {
        'X-API-Key': api_key,
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return response.status_code, response.text

def convert_balance(balance, decimals):
    return balance / (10 ** decimals)

def find_common_tokens(addresses):
    all_tokens = {}
    common_tokens = None
    
    for address in addresses:
        tokens = get_eth_tokens(address)
        
        if isinstance(tokens, list):
            token_addresses = {token['token_address'] for token in tokens}
            all_tokens[address] = token_addresses
            
            if common_tokens is None:
                common_tokens = token_addresses
            else:
                common_tokens = common_tokens.intersection(token_addresses)
        else:
            print(f"Error fetching tokens for address {address}: {tokens[0]} - {tokens[1]}")
            return None
    
    return common_tokens

def print_token_info(address, token_address):
    tokens = get_eth_tokens(address)
    for token in tokens:
        if token['token_address'] == token_address:
            name = token.get('name') if token.get('name') is not None else 'N/A'
            symbol = token.get('symbol') if token.get('symbol') is not None else 'N/A'
            raw_balance = int(token.get('balance', 0))

            decimals = token.get('decimals', 0)
            if decimals is None:
                decimals = 0
            else:
                decimals = int(decimals)

            converted_balance = convert_balance(raw_balance, decimals)
            returning_text = ""
            returning_text+= f"Address: {address}\n"
            returning_text+= f"Token Name: {name}\n"
            returning_text+= f"Token Symbol: {symbol}\n"
            returning_text+= f"Token Balance: {converted_balance:.18f}\n"  # Εμφανίζει μέχρι 18 δεκαδικά ψηφία
            returning_text+= f"Token Address: {token['token_address']}\n"
            
            return returning_text

# Παράδειγμα χρήσης
addresses = [
    "0x54Da1B4e482Ba53A01eF3cC67B57C75c99F14669",  # Αντικαταστήστε με τη διεύθυνση Ethereum
    "0x6982508145454Ce325dDbE47a25d4ec3d2311933"   # Αντικαταστήστε με άλλη διεύθυνση Ethereum
]