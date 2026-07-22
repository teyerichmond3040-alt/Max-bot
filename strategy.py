import numpy as np
import pandas as pd
from logger import get_logger
from config import (
    STOP_LOSS_PERCENT, TAKE_PROFIT_PERCENT, 
    MIN_VOLATILITY, RISK_PER_TRADE, USE_LEVERAGE
)

logger = get_logger(__name__)

class TradingStrategy:
    def __init__(self):
        self.positions = {}
        self.trade_history = []

    def calculate_volatility(self, ohlcv):
        """Calculate volatility from OHLCV data"""
        if len(ohlcv) < 2:
            return 0
        
        closes = np.array([candle[4] for candle in ohlcv])
        returns = np.diff(closes) / closes[:-1]
        volatility = np.std(returns) * 100
        return volatility

    def calculate_rsi(self, ohlcv, period=14):
        """Calculate Relative Strength Index"""
        if len(ohlcv) < period:
            return 50
        
        closes = np.array([candle[4] for candle in ohlcv])
        deltas = np.diff(closes)
        
        seed = deltas[:period+1]
        up = seed[seed >= 0].sum() / period
        down = -seed[seed < 0].sum() / period
        
        rs = up / down if down != 0 else 0
        rsi = 100 - (100 / (1 + rs))
        
        for i in range(period, len(deltas)):
            delta = deltas[i]
            if delta > 0:
                up = (up * (period - 1) + delta) / period
                down = (down * (period - 1)) / period
            else:
                up = (up * (period - 1)) / period
                down = (down * (period - 1) - delta) / period
            
            rs = up / down if down != 0 else 0
            rsi = 100 - (100 / (1 + rs))
        
        return rsi

    def calculate_macd(self, ohlcv):
        """Calculate MACD"""
        if len(ohlcv) < 26:
            return 0, 0, 0
        
        closes = np.array([candle[4] for candle in ohlcv])
        
        # Calculate EMAs
        ema_12 = pd.Series(closes).ewm(span=12).mean().iloc[-1]
        ema_26 = pd.Series(closes).ewm(span=26).mean().iloc[-1]
        
        macd = ema_12 - ema_26
        signal = pd.Series(closes).ewm(span=9).mean().iloc[-1]
        histogram = macd - signal
        
        return macd, signal, histogram

    def should_buy(self, symbol, ohlcv, current_price):
        """Determine if we should BUY"""
        if len(ohlcv) < 26:
            return False, 0
        
        # Check volatility
        volatility = self.calculate_volatility(ohlcv)
        if volatility < MIN_VOLATILITY:
            logger.debug(f"{symbol} volatility too low: {volatility:.2f}%")
            return False, 0
        
        # Check RSI (oversold)
        rsi = self.calculate_rsi(ohlcv)
        if rsi > 70:  # Overbought
            return False, 0
        
        # Check MACD
        macd, signal, histogram = self.calculate_macd(ohlcv)
        macd_bullish = histogram > 0
        
        # RSI bullish signal
        rsi_bullish = rsi < 30 or (rsi < 50 and rsi > 40)
        
        # Price action
        closes = np.array([candle[4] for candle in ohlcv[-5:]])
        price_bullish = closes[-1] > np.mean(closes[:-1])
        
        confidence = (
            (macd_bullish * 0.4) +
            (rsi_bullish * 0.3) +
            (price_bullish * 0.3)
        )
        
        should_buy = confidence > 0.5
        
        if should_buy:
            logger.info(f"{symbol} BUY signal - RSI: {rsi:.1f}, MACD: {macd:.6f}, Vol: {volatility:.2f}%")
        
        return should_buy, confidence

    def should_sell(self, symbol, entry_price, current_price):
        """Determine if we should SELL"""
        price_change = ((current_price - entry_price) / entry_price) * 100
        
        # Stop loss
        if price_change <= -STOP_LOSS_PERCENT:
            logger.info(f"{symbol} HIT STOP LOSS at {price_change:.2f}%")
            return True, "stop_loss"
        
        # Take profit
        if price_change >= TAKE_PROFIT_PERCENT:
            logger.info(f"{symbol} TAKE PROFIT at {price_change:.2f}%")
            return True, "take_profit"
        
        return False, None

    def calculate_position_size(self, balance, current_price, symbol):
        """Calculate aggressive position size"""
        # Risk per trade in USD
        risk_amount = balance * RISK_PER_TRADE / 100
        
        # With leverage
        position_size = (risk_amount * USE_LEVERAGE) / current_price
        
        return position_size

    def get_entry_price(self, symbol, ohlcv, current_price):
        """Get optimal entry price (slightly below current)"""
        volatility = self.calculate_volatility(ohlcv)
        # Enter at a small dip
        entry_price = current_price * (1 - (volatility / 500))
        return entry_price

    def get_exit_price(self, symbol, entry_price, tp_percent=None):
        """Calculate exit price"""
        tp = tp_percent if tp_percent else TAKE_PROFIT_PERCENT
        return entry_price * (1 + (tp / 100))
