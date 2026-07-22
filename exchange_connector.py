import ccxt
from logger import get_logger
from config import EXCHANGE_ID, API_KEY, API_SECRET

logger = get_logger(__name__)

class ExchangeConnector:
    def __init__(self):
        try:
            exchange_class = getattr(ccxt, EXCHANGE_ID)
            self.exchange = exchange_class({
                'apiKey': API_KEY,
                'secret': API_SECRET,
                'enableRateLimit': True,
                'options': {
                    'defaultType': 'future',  # Use futures for leverage
                }
            })
            logger.info(f"Connected to {EXCHANGE_ID}")
        except Exception as e:
            logger.error(f"Failed to connect to exchange: {e}")
            raise

    def get_balance(self):
        """Get current account balance"""
        try:
            balance = self.exchange.fetch_balance()
            usdt_balance = balance.get('USDT', {}).get('free', 0)
            logger.info(f"Current balance: ${usdt_balance:.2f}")
            return usdt_balance
        except Exception as e:
            logger.error(f"Error fetching balance: {e}")
            return 0

    def get_ohlcv(self, symbol, timeframe='1m', limit=100):
        """Fetch OHLCV data"""
        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            return ohlcv
        except Exception as e:
            logger.error(f"Error fetching OHLCV for {symbol}: {e}")
            return []

    def get_ticker(self, symbol):
        """Get current ticker data"""
        try:
            ticker = self.exchange.fetch_ticker(symbol)
            return ticker
        except Exception as e:
            logger.error(f"Error fetching ticker for {symbol}: {e}")
            return None

    def place_market_order(self, symbol, side, amount):
        """Place market order"""
        try:
            order = self.exchange.create_market_order(symbol, side, amount)
            logger.info(f"Market order placed: {symbol} {side} {amount}")
            return order
        except Exception as e:
            logger.error(f"Error placing market order: {e}")
            return None

    def place_limit_order(self, symbol, side, amount, price, params={}):
        """Place limit order with optional take-profit"""
        try:
            order = self.exchange.create_limit_order(
                symbol, side, amount, price, params
            )
            logger.info(f"Limit order placed: {symbol} {side} {amount} @ {price}")
            return order
        except Exception as e:
            logger.error(f"Error placing limit order: {e}")
            return None

    def cancel_order(self, order_id, symbol):
        """Cancel an order"""
        try:
            self.exchange.cancel_order(order_id, symbol)
            logger.info(f"Order {order_id} cancelled")
            return True
        except Exception as e:
            logger.error(f"Error cancelling order: {e}")
            return False

    def set_leverage(self, symbol, leverage):
        """Set leverage for futures trading"""
        try:
            if hasattr(self.exchange, 'set_leverage'):
                self.exchange.set_leverage(leverage, symbol)
                logger.info(f"Leverage set to {leverage}x for {symbol}")
            return True
        except Exception as e:
            logger.warning(f"Could not set leverage: {e}")
            return False

    def get_open_positions(self):
        """Get all open positions"""
        try:
            positions = self.exchange.fetch_positions()
            return positions
        except Exception as e:
            logger.error(f"Error fetching positions: {e}")
            return []
