import telebot
import moralis_test

# Αρχικοποίηση του bot με το προσωπικό σας token
bot = telebot.TeleBot('XXXXX')

# Λεξικό με τις διαθέσιμες επιλογές δικτύου
network_options = {
    'ETH': 'Ethereum',
    'BSC': 'Binance Smart Chain',
    'POLY': 'Polygon (Matic)',
    'SOL': 'Solana'
}

# Λεξικό για την αποθήκευση των επιλογών δικτύου ανά χρήστη
user_data = {}

# Λειτουργία για την εντολή /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "To search for tokens, type /search followed by the network code (e.g., /search ETH).\n\n"
                                      "Available networks:\n"
                                      "ETH - Ethereum\n"
                                      "BSC - Binance Smart Chain\n"
                                      "POLY - Polygon (Matic)\n"
                                      "SOL - Solana\n")

# Λειτουργία για την εντολή /help
@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, "To search for tokens, type /search followed by the network code (e.g., /search ETH).\n\n"
                                      "Available networks:\n"
                                      "ETH - Ethereum\n"
                                      "BSC - Binance Smart Chain\n"
                                      "POLY - Polygon (Matic)\n"
                                      "SOL - Solana\n")

# Λειτουργία για την εντολή /search
@bot.message_handler(commands=['search'])
def handle_search(message):
    command_parts = message.text.split()
    if len(command_parts) != 2 or command_parts[1].upper() not in network_options.keys():
        bot.send_message(message.chat.id, "Invalid command. Please use /search followed by the network code (e.g., /search ETH).\n\n"
                                          "Available networks:\n"
                                          "ETH - Ethereum\n"
                                          "BSC - Binance Smart Chain\n"
                                          "POLY - Polygon (Matic)\n"
                                          "SOL - Solana\n")
        return
    
    selected_network = network_options[command_parts[1].upper()]
    user_data[message.chat.id] = {'selected_network': selected_network}
    bot.send_message(message.chat.id, f"You have selected {selected_network}. Now please enter your wallet addresses, each on a new line.")
    bot.register_next_step_handler(message, process_wallets)

# Λειτουργία για την επεξεργασία των διευθύνσεων πορτοφολιού
def process_wallets(message):
    wallets = message.text.splitlines()
    selected_network = user_data[message.chat.id]['selected_network']
    reply_text = f"Searching for wallets on {selected_network}:\n"
    common_tokens = moralis_test.find_common_tokens(wallets)
    
    if common_tokens:
        reply_text+= "Common Tokens:\n"
        for token_address in common_tokens:
            reply_text+= f"Token Address: {token_address}\n"
            for wallet in wallets:
                reply_text+= moralis_test.print_token_info(wallet, token_address)
    
    bot.send_message(message.chat.id, reply_text)

# Ξεκινήστε το bot
bot.polling()
