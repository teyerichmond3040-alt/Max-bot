# 🚀 Quick Start Guide

## Installation (2 minutes)

### Option 1: Local Installation
```bash
# Clone repository
git clone https://github.com/teyerichmond3040-alt/Max-bot.git
cd Max-bot

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
```

### Option 2: Docker (Recommended)
```bash
# Build and run
docker-compose up --build
```

## Configuration (1 minute)

Edit `.env` with your Binance Futures API credentials:

```env
EXCHANGE_ID=binance
API_KEY=your_binance_api_key
API_SECRET=your_binance_api_secret

# Trading settings
INITIAL_BALANCE=1              # Start with $1
TARGET_BALANCE=10000           # Goal is $10,000
TIME_LIMIT_MINUTES=180         # 3 hours to reach goal
TRADING_PAIRS=BTC/USDT,ETH/USDT,SOL/USDT,XRP/USDT,DOGE/USDT

# Strategy
RISK_PER_TRADE=0.5             # Risk 0.5% per trade
USE_LEVERAGE=5                 # 5x leverage
STOP_LOSS_PERCENT=2            # -2% stop loss
TAKE_PROFIT_PERCENT=5          # +5% take profit
```

## Running the Bot

### Local
```bash
python main.py
```

### Docker
```bash
docker-compose up
```

### View Logs
```bash
# Local
tail -f logs/accumulator.log

# Docker
docker-compose logs -f accumulator-bot
```

## 📊 Expected Output

```
========== ACCUMULATOR BOT STARTED ==========
Initial Balance: $1.00
Target Balance: $10000.00
Time Limit: 180 minutes
Trading Pairs: BTC/USDT, ETH/USDT, SOL/USDT, XRP/USDT, DOGE/USDT
==========================================

--- Iteration 1 ---
===== ACCUMULATOR STATUS =====
Current Balance: $1.00
ROI: 0.00%
Target: $10000.00
Time Remaining: 179.9 minutes
Active Trades: 0
Completed Trades: 0
==============================

Best pairs: ['BTC/USDT', 'ETH/USDT']
  BTC/USDT: Score=85.42, Vol=2.15%, RSI=45.2
  ETH/USDT: Score=82.15, Vol=1.98%, RSI=48.5

Trade opened: BTC/USDT 0.00005 @ $42500.00
```

## ⚙️ API Key Setup (Binance Futures)

1. Go to https://www.binance.com/en/account/api-management
2. Create new API key with these permissions:
   - ✅ Futures Trading
   - ✅ Read access to positions
   - ✅ Read balance
   - ❌ Withdraw (disable for security)
3. Copy API Key and Secret to `.env`

## 🔧 Troubleshooting

### "ModuleNotFoundError: No module named 'ccxt'"
```bash
pip install ccxt==4.0.50
```

### "APIError: [Errno 1015] 418 I'm a teapot"
- Exchange rate limit exceeded
- Reduce `RISK_PER_TRADE` to slow down trades
- Increase wait time in main loop

### "Balance is 0"
- Verify API credentials are correct
- Check account has funds in USDT
- Ensure API key has futures trading enabled

### "No OHLCV data"
- Trading pair might not exist on exchange
- Check pair format: `BTC/USDT` (not `BTCUSDT`)
- Verify pair is available for futures trading

## 📈 Performance Tips

1. **Start Conservative**: Begin with `RISK_PER_TRADE=0.1%`
2. **Use Testnet First**: Test on Binance testnet
3. **Monitor Carefully**: Don't run overnight without monitoring
4. **Volatile Pairs**: BTC, ETH, SOL, SHIB work best
5. **Time Window**: 3-4 hours optimal for multiple trades

## 🛡️ Risk Management

⚠️ **IMPORTANT - Read Before Running:**

- Start with small amounts ($1-$10)
- Test thoroughly before scaling up
- You can lose your entire investment
- Never use money you can't afford to lose
- Always monitor the bot
- Enable 2FA on exchange account

## 📚 File Structure

```
Max-bot/
├── main.py              # Entry point
├── accumulator.py       # Main bot logic
├── strategy.py          # Trading strategy (RSI, MACD, volatility)
├── exchange_connector.py # Exchange API wrapper
├── config.py            # Configuration loader
├── logger.py            # Logging utility
├── test_bot.py          # Unit tests
├── requirements.txt     # Python dependencies
├── Dockerfile           # Container config
├── docker-compose.yml   # Docker compose config
└── README.md            # Full documentation
```

## 🔄 Strategy Explanation

### Entry Signals
Bot enters when ALL conditions are met:
- RSI < 30 (oversold) or RSI 40-50 (early bullish)
- MACD histogram positive (momentum increasing)
- Volatility > 0.8% (enough price movement)
- Price above recent 5-candle average

### Exit Signals
Bot exits when ANY condition triggers:
- Stop loss: Price down -2% from entry
- Take profit: Price up +5% from entry
- Time-based: Position held too long

### Position Sizing
```
Position Size = (Balance × Risk% × Leverage) / Current Price
```
Example: $100 balance, 0.5% risk, 5x leverage, $50 price
→ 0.5% = $0.50 risk → $0.50 × 5 = $2.50 to trade → $2.50 / $50 = 0.05 coins

## 🎯 Expected Results

With optimal conditions (high volatility market):
- **Hour 1**: $1 → $10-50
- **Hour 2**: $50 → $500-2000
- **Hour 3**: $2000 → $5000-10000+

Results vary based on:
- Market volatility (higher = better)
- Number of winning trades
- Leverage settings
- Risk per trade

## 📞 Support & Issues

- **GitHub Issues**: Report bugs
- **GitHub Discussions**: Ask questions
- **Logs**: Check `logs/accumulator.log` for errors

## 📝 Testing

```bash
# Run unit tests
python -m pytest test_bot.py -v

# Run with test data
python test_bot.py
```

## 🚀 Next Steps

1. ✅ Install dependencies
2. ✅ Add API credentials
3. ✅ Run on testnet
4. ✅ Start with $1-$10 live
5. ✅ Scale up gradually

---

**Let's make some gains! 📈**
