import time
from datetime import datetime, timedelta
from logger import get_logger
from exchange_connector import ExchangeConnector
from strategy import TradingStrategy
from config import (
    TRADING_PAIRS, INITIAL_BALANCE, TARGET_BALANCE,
    TIME_LIMIT_MINUTES, POSITION_SIZE_MULTIPLIER, MAX_POSITIONS
)

logger = get_logger(__name__)

class AccumulatorBot:
    def __init__(self):
        self.exchange = ExchangeConnector()
        self.strategy = TradingStrategy()
        self.initial_balance = INITIAL_BALANCE
        self.target_balance = TARGET_BALANCE
        self.start_time = datetime.now()
        self.end_time = self.start_time + timedelta(minutes=TIME_LIMIT_MINUTES)
        self.active_trades = {}
        self.completed_trades = []
        self.profit_log = []
        
    def get_time_remaining(self):
        """Get remaining time in seconds"""
        return (self.end_time - datetime.now()).total_seconds()

    def is_time_remaining(self):
        """Check if trading time remains"""
        return self.get_time_remaining() > 0

    def get_current_balance(self):
        """Get current account balance"""
        balance = self.exchange.get_balance()
        return balance

    def calculate_roi(self):
        """Calculate current ROI"""
        current_balance = self.get_current_balance()
        roi = ((current_balance - self.initial_balance) / self.initial_balance) * 100
        return roi, current_balance

    def log_trade_status(self):
        """Log current trading status"""
        roi, current_balance = self.calculate_roi()
        time_remaining = self.get_time_remaining() / 60
        
        logger.info(f"""
        ===== ACCUMULATOR STATUS =====
        Current Balance: ${current_balance:.2f}
        ROI: {roi:.2f}%
        Target: ${self.target_balance:.2f}
        Time Remaining: {time_remaining:.1f} minutes
        Active Trades: {len(self.active_trades)}
        Completed Trades: {len(self.completed_trades)}
        ==============================
        """)

    def execute_trade(self, symbol):
        """Execute a single trade on a symbol"""
        try:
            # Get latest price data
            ohlcv = self.exchange.get_ohlcv(symbol, '1m', limit=100)
            if not ohlcv:
                logger.warning(f"No OHLCV data for {symbol}")
                return False
            
            ticker = self.exchange.get_ticker(symbol)
            if not ticker:
                logger.warning(f"No ticker data for {symbol}")
                return False
            
            current_price = ticker['last']
            
            # Check buy signal
            should_buy, confidence = self.strategy.should_buy(symbol, ohlcv, current_price)
            
            if not should_buy:
                return False
            
            # Get current balance
            balance = self.get_current_balance()
            
            # Calculate position size
            position_size = self.strategy.calculate_position_size(
                balance, current_price, symbol
            )
            
            if position_size <= 0:
                logger.warning(f"Invalid position size for {symbol}")
                return False
            
            # Set leverage if needed
            if self.exchange.exchange.has['margin']:
                self.exchange.set_leverage(symbol, 5)
            
            # Place market buy order
            order = self.exchange.place_market_order(symbol, 'buy', position_size)
            
            if order:
                trade_id = order.get('id')
                self.active_trades[trade_id] = {
                    'symbol': symbol,
                    'entry_price': current_price,
                    'position_size': position_size,
                    'entry_time': datetime.now(),
                    'order_id': trade_id,
                    'status': 'open',
                    'confidence': confidence
                }
                logger.info(f"Trade opened: {symbol} {position_size} @ ${current_price}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error executing trade on {symbol}: {e}")
            return False

    def manage_active_trades(self):
        """Manage and monitor active trades"""
        trades_to_close = []
        
        for trade_id, trade_info in self.active_trades.items():
            try:
                symbol = trade_info['symbol']
                entry_price = trade_info['entry_price']
                
                ticker = self.exchange.get_ticker(symbol)
                if not ticker:
                    continue
                
                current_price = ticker['last']
                
                # Check exit conditions
                should_sell, reason = self.strategy.should_sell(
                    symbol, entry_price, current_price
                )
                
                if should_sell:
                    trades_to_close.append((trade_id, symbol, current_price, reason))
                    
            except Exception as e:
                logger.error(f"Error managing trade {trade_id}: {e}")
        
        # Close trades
        for trade_id, symbol, current_price, reason in trades_to_close:
            try:
                position_size = self.active_trades[trade_id]['position_size']
                entry_price = self.active_trades[trade_id]['entry_price']
                
                # Place sell order
                order = self.exchange.place_market_order(symbol, 'sell', position_size)
                
                if order:
                    profit = (current_price - entry_price) * position_size
                    profit_pct = ((current_price - entry_price) / entry_price) * 100
                    
                    self.completed_trades.append({
                        'symbol': symbol,
                        'entry': entry_price,
                        'exit': current_price,
                        'profit': profit,
                        'profit_pct': profit_pct,
                        'reason': reason
                    })
                    
                    logger.info(f"Trade closed: {symbol} Profit: ${profit:.2f} ({profit_pct:.2f}%) - {reason}")
                    
                    del self.active_trades[trade_id]
                    
            except Exception as e:
                logger.error(f"Error closing trade {trade_id}: {e}")

    def select_best_pairs(self):
        """Select the best trading pairs based on volatility"""
        pair_scores = []
        
        for symbol in TRADING_PAIRS:
            try:
                ohlcv = self.exchange.get_ohlcv(symbol, '1m', limit=100)
                if ohlcv:
                    volatility = self.strategy.calculate_volatility(ohlcv)
                    rsi = self.strategy.calculate_rsi(ohlcv)
                    
                    # Score based on volatility and RSI
                    score = volatility * 0.6 + (100 - abs(50 - rsi)) * 0.4
                    pair_scores.append((symbol, score, volatility, rsi))
                    
            except Exception as e:
                logger.debug(f"Error analyzing {symbol}: {e}")
        
        # Sort by score and return top pairs
        pair_scores.sort(key=lambda x: x[1], reverse=True)
        best_pairs = [p[0] for p in pair_scores[:MAX_POSITIONS]]
        
        logger.info(f"Best pairs: {best_pairs}")
        for symbol, score, vol, rsi in pair_scores[:5]:
            logger.info(f"  {symbol}: Score={score:.2f}, Vol={vol:.2f}%, RSI={rsi:.1f}")
        
        return best_pairs

    def run(self):
        """Main bot execution loop"""
        logger.info(f"""
        ========== ACCUMULATOR BOT STARTED ==========
        Initial Balance: ${self.initial_balance:.2f}
        Target Balance: ${self.target_balance:.2f}
        Time Limit: {TIME_LIMIT_MINUTES} minutes
        Trading Pairs: {', '.join(TRADING_PAIRS)}
        ==========================================
        """)
        
        iteration = 0
        
        while self.is_time_remaining():
            iteration += 1
            logger.info(f"\n--- Iteration {iteration} ---")
            
            try:
                # Log current status
                self.log_trade_status()
                
                # Check if target reached
                _, current_balance = self.calculate_roi()
                if current_balance >= self.target_balance:
                    logger.info(f"🎉 TARGET REACHED! Balance: ${current_balance:.2f}")
                    break
                
                # Select best pairs
                best_pairs = self.select_best_pairs()
                
                # Execute trades on best pairs (if slots available)
                for symbol in best_pairs:
                    if len(self.active_trades) < MAX_POSITIONS:
                        self.execute_trade(symbol)
                
                # Manage active trades
                self.manage_active_trades()
                
                # Sleep before next iteration
                time.sleep(5)
                
            except KeyboardInterrupt:
                logger.info("Bot stopped by user")
                break
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                time.sleep(5)
        
        # Final report
        self.print_final_report()

    def print_final_report(self):
        """Print final trading report"""
        roi, final_balance = self.calculate_roi()
        
        logger.info(f"""
        ========== FINAL REPORT ==========
        Final Balance: ${final_balance:.2f}
        Initial Balance: ${self.initial_balance:.2f}
        Total Profit: ${final_balance - self.initial_balance:.2f}
        ROI: {roi:.2f}%
        Target Balance: ${self.target_balance:.2f}
        Completed Trades: {len(self.completed_trades)}
        Active Trades: {len(self.active_trades)}
        
        === Trade Summary ===
        """)
        
        total_profit = 0
        winning_trades = 0
        
        for trade in self.completed_trades:
            logger.info(
                f"{trade['symbol']}: {trade['profit_pct']:+.2f}% "
                f"(${trade['profit']:+.2f}) - {trade['reason']}"
            )
            total_profit += trade['profit']
            if trade['profit'] > 0:
                winning_trades += 1
        
        if self.completed_trades:
            win_rate = (winning_trades / len(self.completed_trades)) * 100
            logger.info(f"\nWin Rate: {win_rate:.1f}% ({winning_trades}/{len(self.completed_trades)})")
            logger.info(f"Total Trade Profit: ${total_profit:.2f}")
        
        logger.info("================================\n")

if __name__ == "__main__":
    bot = AccumulatorBot()
    bot.run()
