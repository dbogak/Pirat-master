import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_URL = os.getenv("URL_MONGO")
CHAT_ID = os.getenv("CHAT_ID")
ADMINS = os.getenv("ADMINS")
ADMIN_CHANNEL = os.getenv("ADMIN_CHANNEL")
ME = os.getenv("ME")
BLOCKCYPHER = os.getenv("BLOCKCYPHER")
WALLET_BTC = os.getenv("WALLET_BTC")
WALLET_USDT = os.getenv("WALLET_USDT")
API_KEY=os.getenv("API_KEY")
COINBASE_API_KEY=os.getenv("COINBASE_API_KEY")
COINBASE_API_SECRET=os.getenv("COINBASE_API_SECRET")
REQUEST_LINK='bitcoin:{address}?'\
    'amount={amount}'
BINANCE_API_SECRET=os.getenv("BINANCE_API_SECRET")
BINANCE_API_KEY=os.getenv("BINANCE_API_KEY")
MAIN_PHOTO=os.getenv("MAIN_PHOTO")
TRAF_PHOTO=os.getenv("TRAF_PHOTO")
