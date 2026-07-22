#!/usr/bin/env python3
"""
Test suite for Accumulator Bot
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta

from strategy import TradingStrategy
from config import STOP_LOSS_PERCENT, TAKE_PROFIT_PERCENT
import numpy as np

class TestTradingStrategy(unittest.TestCase):
    """Test trading strategy calculations"""
    
    def setUp(self):
        self.strategy = TradingStrategy()
    
    def test_volatility_calculation(self):
        """Test volatility calculation"""
        # Mock OHLCV data with known volatility
        ohlcv = [
            [1622534400000, 100, 110, 90, 105, 1000],
            [1622534460000, 105, 115, 100, 110, 1000],
            [1622534520000, 110, 120, 105, 115, 1000],
        ]
        
        volatility = self.strategy.calculate_volatility(ohlcv)
        self.assertGreater(volatility, 0)
        self.assertLess(volatility, 100)
    
    def test_rsi_calculation(self):
        """Test RSI calculation"""
        # Mock OHLCV data
        closes = np.linspace(100, 110, 30)
        ohlcv = [[i*60000, c*0.9, c*1.1, c*0.9, c, 1000] for i, c in enumerate(closes)]
        
        rsi = self.strategy.calculate_rsi(ohlcv)
        self.assertGreaterEqual(rsi, 0)
        self.assertLessEqual(rsi, 100)
    
    def test_macd_calculation(self):
        """Test MACD calculation"""
        closes = np.linspace(100, 120, 30)
        ohlcv = [[i*60000, c*0.9, c*1.1, c*0.9, c, 1000] for i, c in enumerate(closes)]
        
        macd, signal, histogram = self.strategy.calculate_macd(ohlcv)
        self.assertIsInstance(macd, (int, float))
        self.assertIsInstance(signal, (int, float))
        self.assertIsInstance(histogram, (int, float))
    
    def test_position_size_calculation(self):
        """Test position size calculation"""
        balance = 100
        price = 50
        symbol = "BTC/USDT"
        
        position_size = self.strategy.calculate_position_size(balance, price, symbol)
        self.assertGreater(position_size, 0)
    
    def test_sell_stop_loss(self):
        """Test stop loss exit"""
        entry_price = 100
        current_price = 98  # -2%
        
        should_sell, reason = self.strategy.should_sell("BTC/USDT", entry_price, current_price)
        self.assertTrue(should_sell)
        self.assertEqual(reason, "stop_loss")
    
    def test_sell_take_profit(self):
        """Test take profit exit"""
        entry_price = 100
        current_price = 105  # +5%
        
        should_sell, reason = self.strategy.should_sell("BTC/USDT", entry_price, current_price)
        self.assertTrue(should_sell)
        self.assertEqual(reason, "take_profit")
    
    def test_no_sell_signal(self):
        """Test no sell signal"""
        entry_price = 100
        current_price = 102  # +2% (between SL and TP)
        
        should_sell, reason = self.strategy.should_sell("BTC/USDT", entry_price, current_price)
        self.assertFalse(should_sell)
        self.assertIsNone(reason)

class TestAccumulatorBot(unittest.TestCase):
    """Test accumulator bot functionality"""
    
    @patch('accumulator.ExchangeConnector')
    def setUp(self, mock_exchange):
        """Setup test fixtures"""
        from accumulator import AccumulatorBot
        self.mock_exchange = mock_exchange.return_value
        self.bot = AccumulatorBot()
    
    def test_roi_calculation(self):
        """Test ROI calculation"""
        self.bot.initial_balance = 100
        with patch.object(self.bot, 'get_current_balance', return_value=150):
            roi, balance = self.bot.calculate_roi()
            self.assertEqual(roi, 50.0)
            self.assertEqual(balance, 150)
    
    def test_time_remaining(self):
        """Test time remaining calculation"""
        self.bot.start_time = datetime.now()
        self.bot.end_time = datetime.now() + timedelta(minutes=180)
        
        remaining = self.bot.get_time_remaining()
        self.assertGreater(remaining, 0)
        self.assertLess(remaining, 180 * 60 + 1)
    
    def test_is_time_remaining(self):
        """Test is time remaining check"""
        self.bot.start_time = datetime.now()
        self.bot.end_time = datetime.now() + timedelta(minutes=1)
        
        self.assertTrue(self.bot.is_time_remaining())
        
        self.bot.end_time = datetime.now() - timedelta(minutes=1)
        self.assertFalse(self.bot.is_time_remaining())

class TestConfigValidation(unittest.TestCase):
    """Test configuration validation"""
    
    def test_config_values(self):
        """Test configuration values are valid"""
        from config import (
            INITIAL_BALANCE, TARGET_BALANCE, TIME_LIMIT_MINUTES,
            RISK_PER_TRADE, USE_LEVERAGE, STOP_LOSS_PERCENT, TAKE_PROFIT_PERCENT
        )
        
        self.assertGreater(INITIAL_BALANCE, 0)
        self.assertGreater(TARGET_BALANCE, INITIAL_BALANCE)
        self.assertGreater(TIME_LIMIT_MINUTES, 0)
        self.assertGreater(RISK_PER_TRADE, 0)
        self.assertGreater(USE_LEVERAGE, 1)
        self.assertGreater(STOP_LOSS_PERCENT, 0)
        self.assertGreater(TAKE_PROFIT_PERCENT, 0)

def run_tests():
    """Run all tests"""
    unittest.main(argv=[''], verbosity=2, exit=False)

if __name__ == '__main__':
    run_tests()
