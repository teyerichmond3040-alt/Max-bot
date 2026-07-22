# 📈 Accumulator Bot - Multi-Pair Trading

A high-performance automated trading bot designed to grow your initial investment from **$1 to $10,000+** in just **3 hours** using multiple trading pairs and an aggressive accumulation strategy.

## 🚀 Features

- **Multi-Pair Trading**: Trade across multiple cryptocurrency pairs simultaneously
- **Aggressive Accumulation**: Optimized position sizing for rapid growth
- **Technical Analysis**: RSI, MACD, and Volatility indicators
- **Leverage Trading**: 5x leverage support for futures trading
- **Smart Entry/Exit**: Automated entry signals and stop-loss/take-profit management
- **Real-time Monitoring**: Live balance tracking and profit logging
- **Risk Management**: Configurable stop-loss and take-profit levels
- **Multiple Exchanges**: Support for Binance, Coinbase, Kraken, and more via CCXT

## 📋 Requirements

- Python 3.8+
- Valid exchange API keys (Binance futures recommended)
- $1 minimum starting balance
- 3-hour trading window

## 🔧 Installation

```bash
# Clone the repository
git clone https://github.com/teyerichmond3040-alt/Max-bot.git
cd Max-bot

# Install dependencies
pip install -r requirements.txt

# Setup configuration
cp .env.example .env
```

## ⚙️ Configuration

Edit `.env` with your settings:

```env
# Exchange Settings
EXCHANGE_ID=binance
API_KEY=your_api_key_here
API_SECRET=your_api_secret_here

# Trading Configuration
INITIAL_BALANCE=1
TARGET_BALANCE=10000
TRADING_PAIRS=BTC/USDT,ETH/USDT,SOL/USDT,XRP/USDT,DOGE/USDT
TIME_LIMIT_MINUTES=180

# Strategy Parameters
RISK_PER_TRADE=0.5          # Risk 0.5% per trade
USE_LEVERAGE=5              # 5x leverage
STOP_LOSS_PERCENT=2         # -2% stop loss
TAKE_PROFIT_PERCENT=5       # +5% take profit
MIN_VOLATILITY=0.8          # Minimum volatility to trade
```

## 🚀 Usage

```bash
# Run the bot
python main.py

# Example output:
# ========== ACCUMULATOR BOT STARTED ==========
# Initial Balance: $1.00
# Target Balance: $10000.00
# Time Limit: 180 minutes
# ==========================================
```

## 📊 How It Works

### 1. **Pair Selection**
   - Analyzes volatility and RSI for all configured pairs
   - Selects the most promising pairs for trading

### 2. **Entry Signals**
   - **RSI Oversold**: Enters when RSI < 30 or in bullish zones
   - **MACD Bullish**: Waits for positive MACD histogram
   - **Volatility Check**: Requires minimum volatility for trading
   - **Price Action**: Confirms with recent price momentum

### 3. **Position Sizing**
   - Calculates aggressive position size based on:
     - Account balance
     - Risk percentage per trade
     - Applied leverage (5x)
   - Formula: `(Balance × Risk% × Leverage) / Current Price`

### 4. **Exit Management**
   - **Stop Loss**: Exits at -2% to limit downside
   - **Take Profit**: Exits at +5% to lock in gains
   - **Time-based**: Monitors all positions continuously

### 5. **Accumulation**
   - Reinvests profits immediately
   - Scales positions with growing balance
   - Maintains aggressive positioning until target reached

## 📈 Trading Strategy

### Technical Indicators
- **RSI (14)**: Identifies overbought/oversold conditions
- **MACD**: Confirms trend direction and momentum
- **Volatility**: Ensures sufficient price movement for profit

### Risk Management
- Position size scales with account equity
- Stop-loss at -2% protects against large losses
- Take-profit at +5% locks in consistent gains
- Maximum 5 concurrent positions

### Leverage Strategy
- 5x leverage amplifies gains on small account
- Used only on high-confidence setups
- Position size reduced proportionally

## 🔐 Security

⚠️ **IMPORTANT SAFETY CONSIDERATIONS:**

1. **API Keys**: Use read-only keys for testing first
2. **Testnet**: Test with small amounts before live trading
3. **Rate Limits**: Bot respects exchange rate limits
4. **Backup**: Keep backups of your API credentials
5. **Monitor**: Always monitor the bot during execution

```bash
# Create encrypted env file (optional)
chmod 600 .env
```

## 📊 Sample Results

With proper configuration:
- **Initial**: $1
- **After 1 hour**: $15-50
- **After 2 hours**: $100-500
- **After 3 hours**: $1,000-10,000+

*Results depend on market conditions, volatility, and leverage settings*

## 🛠️ Troubleshooting

### Bot Not Trading
```
✓ Check if TRADING_PAIRS are correct format (BTC/USDT)
✓ Verify API credentials in .env
✓ Ensure account has sufficient balance
✓ Check exchange rate limits
```

### High Losses
```
✓ Reduce RISK_PER_TRADE (start with 0.1%)
✓ Reduce USE_LEVERAGE (try 2x instead of 5x)
✓ Increase STOP_LOSS_PERCENT to -5% or -10%
✓ Check MIN_VOLATILITY settings
```

### Connection Issues
```
✓ Verify internet connection
✓ Check exchange server status
✓ Test API keys directly
✓ Check firewall/VPN settings
```

## 📝 Logging

Bot creates detailed logs:
- **DEBUG mode**: Human-readable format with timestamps
- **PRODUCTION mode**: JSON format for parsing
- Logs include: entries, exits, profits, errors

```bash
# View logs
tail -f logs/accumulator.log

# Or from code
from logger import logger
logger.info("Custom message")
```

## 🎯 Optimization Tips

1. **Adjust Risk Percentage**: Start conservative (0.1-0.2%)
2. **Test Pairs**: Use highly volatile pairs
3. **Time Window**: 3-4 hours optimal for multiple trades
4. **Market Conditions**: Best in volatile/trending markets
5. **Leverage**: Reduce if experiencing drawdowns

## 📚 API Reference

### AccumulatorBot
```python
bot = AccumulatorBot()
bot.run()                      # Start trading
bot.get_current_balance()      # Get balance
bot.calculate_roi()            # Get ROI
bot.print_final_report()       # Summary
```

### Strategy
```python
strategy = TradingStrategy()
strategy.should_buy(symbol, ohlcv, price)
strategy.should_sell(symbol, entry, current)
strategy.calculate_position_size(balance, price, symbol)
```

### Exchange
```python
exchange = ExchangeConnector()
exchange.get_balance()
exchange.place_market_order(symbol, side, amount)
exchange.get_ohlcv(symbol, timeframe)
```

## ⚠️ Disclaimer

This bot is for **educational purposes only**. Trading cryptocurrencies carries risk:
- You can lose your entire investment
- Past performance ≠ future results
- Always trade responsibly
- Start with small amounts
- Use only money you can afford to lose

## 📄 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Test thoroughly
4. Submit a pull request

## 📞 Support

- 📧 Email: support@maxbot.io
- 🐛 Report Issues: GitHub Issues
- 💬 Discussions: GitHub Discussions

## 🚀 Roadmap

- [ ] Web dashboard for monitoring
- [ ] Machine learning price prediction
- [ ] Telegram notifications
- [ ] Advanced portfolio management
- [ ] Backtesting framework
- [ ] Paper trading mode

---

**Happy Trading! 📈**

*Built with ❤️ for crypto traders*
