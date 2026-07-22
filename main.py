#!/usr/bin/env python3
"""
Accumulator Bot - Grow $1 to $10,000+ in 3 hours
Multi-pair trading with aggressive accumulation strategy
"""

import sys
from accumulator import AccumulatorBot
from logger import get_logger

logger = get_logger(__name__)

def main():
    try:
        bot = AccumulatorBot()
        bot.run()
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
