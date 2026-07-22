import os
from dotenv import load_dotenv

load_dotenv()

# Exchange Settings
EXCHANGE_ID = os.getenv('EXCHANGE_ID', 'binance')
API_KEY = os.getenv('API_KEY', '')
API_SECRET = os.getenv('API_SECRET', '')

# Trading Settings
INITIAL_BALANCE = float(os.getenv('INITIAL_BALANCE', '1'))
TARGET_BALANCE = float(os.getenv('TARGET_BALANCE', '10000'))
TRADING_PAIRS = os.getenv('TRADING_PAIRS', 'BTC/USDT,ETH/USDT,SOL/USDT').split(',')
TIME_LIMIT_MINUTES = int(os.getenv('TIME_LIMIT_MINUTES', '180'))

# Strategy Settings
RISK_PER_TRADE = float(os.getenv('RISK_PER_TRADE', '0.5'))
USE_LEVERAGE = int(os.getenv('USE_LEVERAGE', '5'))
STOP_LOSS_PERCENT = float(os.getenv('STOP_LOSS_PERCENT', '2'))
TAKE_PROFIT_PERCENT = float(os.getenv('TAKE_PROFIT_PERCENT', '5'))
MIN_VOLATILITY = float(os.getenv('MIN_VOLATILITY', '0.8'))

# Logging
DEBUG = os.getenv('DEBUG', 'True') == 'True'
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# Derived Settings
POSITION_SIZE_MULTIPLIER = 2.0  # Aggressive positioning
MAX_POSITIONS = 5  # Max concurrent trades
REBALANCE_THRESHOLD = 0.1  # Rebalance at 10% gains
